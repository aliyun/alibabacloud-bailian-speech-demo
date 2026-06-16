#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import uuid
import threading
import traceback
import json
import base64
import signal
import sys
import time
from typing import Dict, Any, Optional, List
import pyaudio
import dashscope
from dashscope.audio.qwen_omni import *

from B64PCMPlayer import B64PCMPlayer


# ==================== Constants ====================
VOICE = 'Tina'
MODEL = "qwen3.5-omni-plus-realtime"
WS_URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime"
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHUNK_SIZE = 3200
OUTPUT_AUDIO_SAMPLE_RATE = 24000


def init_dashscope_api_key():
    """
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """
    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ[
            'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually


# ==================== Tool Definitions ====================
def get_train_price(src: str, dst: str) -> str:
    """Query train ticket price"""
    return f"Train ticket from {src} to {dst} costs 100~200 RMB."


def get_flight_price(src: str, dst: str) -> str:
    """Query flight ticket price"""
    return f"Flight ticket from {src} to {dst} costs 200~300 USD."


def get_current_weather(location: str) -> str:
    """Query weather for a specified city"""
    return f"Weather in {location} today: haze turning to sunny, temperature 4/-4C, light breeze"


# Unified OpenAI-format tool definitions
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_flight_price",
            "description": "当你想查询飞机票价格时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "src": {
                        "type": "string",
                        "description": "飞机起飞的城市，比如北京市、杭州市等。",
                    },
                    "dst": {
                        "type": "string",
                        "description": "飞机降落的城市，比如北京市、杭州市区等。",
                    },
                },
                "required": ["src", "dst"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_train_price",
            "description": "当你想查询火车票价格时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "src": {
                        "type": "string",
                        "description": "火车出发的城市，比如北京市、杭州市等。",
                    },
                    "dst": {
                        "type": "string",
                        "description": "火车到达的城市，比如北京市、杭州市区等。",
                    },
                },
                "required": ["src", "dst"],
            },
        },
    },
]

# Mapping from tool name to function
TOOL_FUNCTIONS = {
    "get_current_weather": get_current_weather,
    "get_flight_price": get_flight_price,
    "get_train_price": get_train_price,
}


# ==================== Tool Call Handling ====================
def handle_tool_call(tool_call_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle a tool call request
    """
    try:
        function_name = tool_call_response['name']
        tool_call_arguments = json.loads(tool_call_response['arguments'])
        print(f'[Tool Call] Processing: name={function_name}, args={tool_call_arguments}')

        if function_name not in TOOL_FUNCTIONS:
            tool_call_response['output'] = f"Tool not found on client: {function_name}"
            print(f'[Tool Call] Error: tool {function_name} not found')
            return tool_call_response

        func = TOOL_FUNCTIONS[function_name]
        result = func(**tool_call_arguments)
        tool_call_response['output'] = result
        print(f'[Tool Call] Completed: {result}')
        return tool_call_response

    except Exception as e:
        error_msg = f"Tool call failed: {str(e)}"
        tool_call_response['output'] = error_msg
        print(f'[Tool Call] Exception: {error_msg}')
        traceback.print_exc()
        return tool_call_response


def send_tool_call_response(conversation: OmniRealtimeConversation,
                            response: Dict[str, Any]) -> None:
    """Send tool call result to the server"""
    conversation.create_item({
        "id": 'item_' + uuid.uuid4().hex,
        "type": "function_call_output",
        "call_id": response['call_id'],
        "output": response["output"],
    })


# ==================== Audio Manager ====================
class AudioManager:
    """Manages audio input and output resources"""

    def __init__(self):
        self.pya: Optional[pyaudio.PyAudio] = None
        self.mic_stream: Optional[pyaudio.Stream] = None
        self.player: Optional[B64PCMPlayer] = None

    def initialize(self) -> None:
        """Initialize audio devices"""
        print('Initializing audio devices...')
        self.pya = pyaudio.PyAudio()
        self.mic_stream = self.pya.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=AUDIO_SAMPLE_RATE,
            input=True
        )
        self.player = B64PCMPlayer(self.pya, sample_rate=OUTPUT_AUDIO_SAMPLE_RATE)
        print('Audio devices initialized')

    def read_audio_chunk(self) -> Optional[bytes]:
        """Read an audio chunk from microphone"""
        if not self.mic_stream:
            return None
        try:
            return self.mic_stream.read(AUDIO_CHUNK_SIZE, exception_on_overflow=False)
        except Exception as e:
            print(f'[Error] Failed to read audio: {e}')
            return None

    def cleanup(self) -> None:
        """Clean up audio resources"""
        print('Cleaning up audio resources...')
        if self.player:
            self.player.shutdown()
        if self.mic_stream:
            self.mic_stream.close()
        if self.pya:
            self.pya.terminate()
        print('Audio resources cleaned up')


# ==================== Callback Handler ====================
class OmniCallback(OmniRealtimeCallback):
    """Omni real-time conversation callback handler"""

    def __init__(self, audio_manager: AudioManager):
        self.audio_manager = audio_manager
        self.tool_calls: Dict[str, Dict[str, Any]] = {}
        self.all_response_text: str = ''
        self.last_package_time: float = 0
        self.is_first_text: bool = True
        self.is_first_audio: bool = True
        self.conversation: Optional[OmniRealtimeConversation] = None

    def set_conversation(self, conversation: OmniRealtimeConversation) -> None:
        """Set conversation instance reference"""
        self.conversation = conversation

    def on_open(self) -> None:
        """Callback when connection is established"""
        print('Connection established')
        self.audio_manager.initialize()
        self.last_package_time = time.time() * 1000
        self.is_first_text = True
        self.is_first_audio = True
        self.tool_calls = {}
        self.all_response_text = ''

    def on_close(self, close_status_code: int, close_msg: str) -> None:
        """Callback when connection is closed"""
        print(f'Connection closed: code={close_status_code}, msg={close_msg}')
        self.audio_manager.cleanup()
        sys.exit(0)

    def on_event(self, response: Dict[str, Any]) -> None:
        """Handle event callback"""
        try:
            event_type = response.get('type', '')

            # Session created
            if event_type == 'session.created':
                print(f'Session started: {response["session"]["id"]}')

            # Speech-to-text completed
            elif event_type == 'conversation.item.input_audio_transcription.completed':
                print(f'User question: {response.get("transcript", "")}')

            # Text delta response
            elif event_type in ('response.audio_transcript.delta', 'response.text.delta'):
                if self.is_first_text:
                    self.is_first_text = False
                    latency = time.time() * 1000 - self.last_package_time
                    print(f'First text latency (from VAD end): {latency:.0f} ms')
                text = response.get('delta', '')
                self.all_response_text += text

            # Audio delta response
            elif event_type == 'response.audio.delta':
                if self.is_first_audio:
                    self.is_first_audio = False
                    latency = time.time() * 1000 - self.last_package_time
                    print(f'First audio latency (from VAD end): {latency:.0f} ms')

                recv_audio_b64 = response.get('delta', '')
                if self.audio_manager.player:
                    self.audio_manager.player.add_data(recv_audio_b64)

            # VAD detected speech start
            elif event_type == 'input_audio_buffer.speech_started':
                print('====== VAD Speech Start ======')
                if self.audio_manager.player:
                    self.audio_manager.player.cancel_playing()

            # VAD detected speech end
            elif event_type == 'input_audio_buffer.speech_stopped':
                print('====== VAD Speech End ======')
                self.last_package_time = time.time() * 1000
                self.is_first_text = True
                self.is_first_audio = True
                self.tool_calls = {}

            # Function call arguments done
            elif event_type == 'response.function_call_arguments.done':
                print('====== Tool Call Request Received ======')
                call_id = response.get('call_id', '')
                self.tool_calls[call_id] = response.copy()
                self.tool_calls[call_id]['processed'] = False

            # Response done
            elif event_type == 'response.done':
                print('====== Response Done ======')
                print(f'Full response: {self.all_response_text}')

                if self.conversation:
                    response_id = self.conversation.get_last_response_id()
                    text_delay = self.conversation.get_last_first_text_delay()
                    audio_delay = self.conversation.get_last_first_audio_delay()

                    if response_id is not None and text_delay is not None and audio_delay is not None:
                        print(f'[Metric] ResponseID: {response_id}, '
                              f'FirstTextDelay: {text_delay:.0f}ms, '
                              f'FirstAudioDelay: {audio_delay:.0f}ms')
                    else:
                        print('[Metric] Metrics not available (possibly after tool call response)')

                self.all_response_text = ''

        except Exception as e:
            print(f'[Error] Event handling exception: {e}')
            traceback.print_exc()

    def process_pending_tool_calls(self) -> bool:
        """
        Process pending tool calls
        Returns:
            Whether there are new tool calls to respond to
        """
        has_pending = False

        for call_id, tool_call in self.tool_calls.items():
            if not tool_call.get('processed', False):
                has_pending = True
                tool_call['processed'] = True
                result = handle_tool_call(tool_call)
                if self.conversation:
                    send_tool_call_response(self.conversation, result)

        return has_pending


# ==================== Main Program ====================
def main():
    """Main function"""
    print('Initializing Omni real-time conversation...')
    init_dashscope_api_key()

    # Create audio manager
    audio_manager = AudioManager()

    # Create callback handler
    callback = OmniCallback(audio_manager)

    # Create conversation instance
    conversation = OmniRealtimeConversation(
        api_key=dashscope.api_key,
        url=WS_URL,
        model=MODEL,
        callback=callback,
    )

    # Set conversation reference in callback
    callback.set_conversation(conversation)

    # Establish connection
    conversation.connect()

    # Configure session parameters
    omni_output_modalities = [MultiModality.AUDIO, MultiModality.TEXT]

    conversation.update_session(
        output_modalities=omni_output_modalities,
        voice=VOICE,
        input_audio_format=AudioFormat.PCM_16000HZ_MONO_16BIT,
        output_audio_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
        enable_input_audio_transcription=True,
        enable_turn_detection=True,
        turn_detection_type='server_vad',
        tools=TOOLS,
    )

    # Set signal handler
    def signal_handler(sig, frame):
        print('\nReceived Ctrl+C, stopping...')
        conversation.close()
        audio_manager.cleanup()
        print('Omni real-time conversation stopped')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    print("Press Ctrl+C to stop conversation...\n")

    # Main loop: continuously send audio and check for tool calls
    try:
        while True:
            # Process pending tool calls
            has_tool_calls = callback.process_pending_tool_calls()

            if has_tool_calls:
                print("*** Tool calls completed, creating new response ***")
                conversation.create_response(
                    instructions=None,
                    output_modalities=omni_output_modalities
                )
                print('====== Tool call processing completed ======\n')

            # Read and send audio data
            audio_data = audio_manager.read_audio_chunk()
            if audio_data:
                audio_b64 = base64.b64encode(audio_data).decode('ascii')
                conversation.append_audio(audio_b64)
            else:
                break

    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
    except Exception as e:
        print(f'[Error] Main loop exception: {e}')
        traceback.print_exc()
    finally:
        conversation.close()
        audio_manager.cleanup()


if __name__ == '__main__':
    main()
