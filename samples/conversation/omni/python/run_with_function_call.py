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
from dashscope import Client

from B64PCMPlayer import B64PCMPlayer


# ==================== Constants ====================
VOICE = 'Tina'
MODEL = "qwen3.5-omni-plus-realtime"
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHUNK_SIZE = 3200
OUTPUT_AUDIO_SAMPLE_RATE = 24000


session = None


def init_dashscope_api_key():
    """
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        return '<your-dashscope-api-key>'  # set API-key manually


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


def send_tool_call_response(response: Dict[str, Any]) -> None:
    """Send tool call result to the server"""
    global session
    session.create_item({
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


# ==================== Event Handler ====================
class OmniEventHandler:
    """Omni real-time conversation event handler"""

    def __init__(self, audio_manager: AudioManager):
        self.audio_manager = audio_manager
        self.tool_calls: Dict[str, Dict[str, Any]] = {}
        self.tool_calls_lock = threading.Lock()
        self.all_response_text: str = ''
        self.last_package_time: float = 0
        self.is_first_text: bool = True
        self.is_first_audio: bool = True

    def handle_event(self, event: Dict[str, Any]) -> None:
        """Handle a single event"""
        global session
        try:
            event_type = event.get('type', '')

            # Session created
            if event_type == 'session.created':
                print(f'Session started: {event["session"]["id"]}')

            # Speech-to-text completed
            elif event_type == 'conversation.item.input_audio_transcription.completed':
                print(f'User question: {event.get("transcript", "")}')

            # Text delta response
            elif event_type in ('response.audio_transcript.delta', 'response.text.delta'):
                if self.is_first_text:
                    self.is_first_text = False
                    latency = time.time() * 1000 - self.last_package_time
                    print(f'First text latency (from VAD end): {latency:.0f} ms')
                text = event.get('delta', '')
                self.all_response_text += text

            # Audio delta response
            elif event_type == 'response.audio.delta':
                if self.is_first_audio:
                    self.is_first_audio = False
                    latency = time.time() * 1000 - self.last_package_time
                    print(f'First audio latency (from VAD end): {latency:.0f} ms')

                recv_audio_b64 = event.get('delta', '')
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
                with self.tool_calls_lock:
                    self.tool_calls = {}

            # Function call arguments done
            elif event_type == 'response.function_call_arguments.done':
                print('====== Tool Call Request Received ======')
                call_id = event.get('call_id', '')
                with self.tool_calls_lock:
                    self.tool_calls[call_id] = event.copy()
                    self.tool_calls[call_id]['processed'] = False

            # Response done
            elif event_type == 'response.done':
                print('====== Response Done ======')
                print(f'Full response: {self.all_response_text}')

                if session:
                    response_id = session.last_response_id
                    text_delay = session.last_first_text_delay
                    audio_delay = session.last_first_audio_delay

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

        with self.tool_calls_lock:
            pending = list(self.tool_calls.items())

        for call_id, tool_call in pending:
            if not tool_call.get('processed', False):
                has_pending = True
                with self.tool_calls_lock:
                    self.tool_calls[call_id]['processed'] = True
                result = handle_tool_call(tool_call)
                send_tool_call_response(result)

        return has_pending


# ==================== Main Program ====================
def main():
    """Main function"""
    global session

    print('Initializing Omni real-time conversation...')
    api_key = init_dashscope_api_key()

    # Create audio manager
    audio_manager = AudioManager()

    # Create event handler
    event_handler = OmniEventHandler(audio_manager)

    with Client(api_key=api_key) as client:
        with client.audio.realtime.connect(
            model=MODEL,
        ) as session:
            session.update_session(
                output_modalities=["audio", "text"],
                voice=VOICE,
                input_audio_config={"type": "pcm", "sample_rate": 16000},
                output_audio_config={"type": "pcm", "sample_rate": 24000},
                enable_input_audio_transcription=True,
                enable_turn_detection=True,
                turn_detection_type='server_vad',
                tools=TOOLS,
            )

            print('Connection established')
            audio_manager.initialize()
            event_handler.last_package_time = time.time() * 1000

            # start event dispatch thread
            def dispatch_events():
                try:
                    for event in session.events():
                        event_handler.handle_event(event)
                except Exception as e:
                    print(f'[Error] Event dispatch exception: {e}')
                    traceback.print_exc()

            event_thread = threading.Thread(target=dispatch_events, daemon=True)
            event_thread.start()

            # Set signal handler
            def signal_handler(sig, frame):
                print('\nReceived Ctrl+C, stopping...')
                session.close()
                audio_manager.cleanup()
                print('Omni real-time conversation stopped')
                sys.exit(0)

            signal.signal(signal.SIGINT, signal_handler)
            print("Press Ctrl+C to stop conversation...\n")

            # Main loop: continuously send audio and check for tool calls
            try:
                while True:
                    # Process pending tool calls
                    has_tool_calls = event_handler.process_pending_tool_calls()

                    if has_tool_calls:
                        print("*** Tool calls completed, creating new response ***")
                        session.create_response(
                            instructions=None,
                            modalities=["audio", "text"],
                        )
                        print('====== Tool call processing completed ======\n')

                    # Read and send audio data
                    audio_data = audio_manager.read_audio_chunk()
                    if audio_data:
                        session.append_audio(audio_data)
                    else:
                        break

            except KeyboardInterrupt:
                signal_handler(signal.SIGINT, None)
            except Exception as e:
                print(f'[Error] Main loop exception: {e}')
                traceback.print_exc()
            finally:
                session.close()
                audio_manager.cleanup()


if __name__ == '__main__':
    main()
