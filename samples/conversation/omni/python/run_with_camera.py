import asyncio
import contextlib
import websockets
import queue
import threading
from io import BytesIO

import os
import base64
import signal
import sys
import time
import pyaudio
import dashscope
from dashscope.audio.qwen_omni import *

from B64PCMPlayer import B64PCMPlayer

voice = 'Chelsie'

pya = None
mic_stream = None
b64_player = None
conversation = None

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


class MyCallback(OmniRealtimeCallback):
    def on_open(self) -> None:
        global pya
        global mic_stream
        global b64_player
        print('connection opened, init microphone')
        pya = pyaudio.PyAudio()
        mic_stream = pya.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True)
        b64_player = B64PCMPlayer(pya)

    def on_close(self, close_status_code, close_msg) -> None:
        print('connection closed with code: {}, msg: {}, destroy microphone'.format(close_status_code, close_msg))
        sys.exit(0)

    def on_event(self, response: str) -> None:
        try:
            global conversation
            global b64_player
            type = response['type']
            if 'session.created' == type:
                print('start session: {}'.format(response['session']['id']))
            if 'conversation.item.input_audio_transcription.completed' == type:
                print('question: {}'.format(response['transcript']))
            if 'response.audio_transcript.delta' == type:
                text = response['delta']
                print("got llm response delta: {}".format(text))
            if 'response.audio.delta' == type:
                recv_audio_b64 = response['delta']
                b64_player.add_data(recv_audio_b64)
            if 'input_audio_buffer.speech_started' == type:
                print('======VAD Speech Start======')
                b64_player.cancel_playing()
            if 'response.done' == type:
                print('======RESPONSE DONE======')
                print('[Metric] response: {}, first text delay: {}, first audio delay: {}'.format(
                                conversation.get_last_response_id(), 
                                conversation.get_last_first_text_delay(), 
                                conversation.get_last_first_audio_delay(),
                                ))
        except Exception as e:
            print('[Error] {}'.format(e))
            return


class ThreadSafeImageB64:
    def __init__(self):
        self.lock = threading.Lock()
        self.image = None
    
    def get(self):
        with self.lock:
            image = self.image
            self.image = None
            return image
    
    def set(self, image):
        with self.lock:
            self.image = image


# 全局队列用于多线程访问采集的图片
latest_image = ThreadSafeImageB64()

def start_receive_image():
    async def handler(websocket, path):
        print('连接到前端摄像头')
        async for message in websocket:
            if isinstance(message, bytes):
                latest_image.set(base64.b64encode(message).decode('ascii'))
        print('前端摄像头连接结束')

    async def run_server():
        async with websockets.serve(handler, "localhost", 5000):
            print("WebSocket server started on ws://localhost:5000/video")
            await asyncio.Future()  # 保持服务运行

    asyncio.run(run_server())



if __name__  == '__main__':
    init_dashscope_api_key()

    # 启动图像处理线程
    threading.Thread(target=start_receive_image).start()

    print('Initializing ...')
    
    record_pcm_file = open('data/record_16khz.pcm', 'wb')

    callback = MyCallback()

    conversation = OmniRealtimeConversation(
        model='qwen-omni-turbo-realtime-latest',
        callback=callback, 
        )

    conversation.connect()

    conversation.update_session(
        output_modalities=[MultiModality.AUDIO, MultiModality.TEXT],
        voice=voice,
        input_audio_format=AudioFormat.PCM_16000HZ_MONO_16BIT,
        output_audio_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
        enable_input_audio_transcription=True,
        input_audio_transcription_model='gummy-realtime-v1',
        enable_turn_detection=True,
        turn_detection_type='server_vad',
    )

    def signal_handler(sig, frame):
        print('Ctrl+C pressed, stop recognition ...')
        # Stop recognition
        conversation.close()
        b64_player.shutdown()
        print('omni realtime stopped.')
        # Forcefully exit the program
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    print("Press 'Ctrl+C' to stop conversation...")

    #模拟多轮交互，在server_vad模式下，服务会自动处理打断，用户可以持续发送静音
    last_photo_time = time.time()*1000
    while True:
        if mic_stream:
            audio_data = mic_stream.read(3200, exception_on_overflow=False)
            record_pcm_file.write(audio_data)
            audio_b64 = base64.b64encode(audio_data).decode('ascii')
            conversation.append_audio(audio_b64)
            with contextlib.suppress(queue.Empty):
                video_frame = latest_image.get()
                if video_frame:
                    conversation.append_video(video_frame)
        else:
            break
