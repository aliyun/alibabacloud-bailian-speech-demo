import os
import base64
import signal
import sys
import threading
import time
import pyaudio
import dashscope
from dashscope.audio.qwen_omni import *

from B64PCMPlayer import B64PCMPlayer

voice = 'Chelsie'

b64_player = None
conversation = None

DO_VIDEO_TEST = False

if DO_VIDEO_TEST:
    fake_video = None
    with open('data/cat_480p.jpg', 'rb') as image_file:
        fake_video = base64.b64encode(image_file.read()).decode('ascii')

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

# 由于omni-realtime下发的音频为base64格式，因此需要decode。
# 这一操作较为耗时，不应该放在callback中或播放前，因此单独使用线程处理。
# 使用B64PCMPlayer播放器可以异步解码并播放。


class MyCallback(OmniRealtimeCallback):
    def __init__(self):
        super().__init__()
        self.complete_event: threading.Event = threading.Event()
    
    def wait_for_complete(self):
        self.complete_event.wait()
        self.complete_event = threading.Event()


    def on_open(self) -> None:
        global b64_player
        print('connection opened, init microphone')
        self.pya = pyaudio.PyAudio()
        b64_player = B64PCMPlayer(self.pya)

    def on_close(self, close_status_code, close_msg) -> None:
        print('connection closed with code: {}, msg: {}, destroy microphone'.format(close_status_code, close_msg))
        sys.exit(0)

    def on_event(self, response: str) -> None:
        global conversation
        global b64_player
        try:
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
            if 'response.done' == type:
                print('======RESPONSE DONE======')
                print('[Metric] response: {}, first text delay: {}, first audio delay: {}'.format(
                                conversation.get_last_response_id(), 
                                conversation.get_last_first_text_delay(), 
                                conversation.get_last_first_audio_delay(),
                                ))
                if self.complete_event:
                    self.complete_event.set()
        except Exception as e:
            print('[Error] {}'.format(e))
            return


if __name__  == '__main__':
    init_dashscope_api_key()

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
        enable_turn_detection=False,
    )

    #模拟两次交互，在非server_vad模式下，需要用户主动发起response create
    # Q1pex
    test_file_path = 'data/q1_16khz.pcm'
    audio_data: bytes = None
    f = open(test_file_path, 'rb')
    last_photo_time = time.time()*1000
    if os.path.getsize(test_file_path):
        while True:
            audio_data = f.read(3200)
            if not audio_data:
                break
            else:
                conversation.append_audio(base64.b64encode(audio_data).decode('ascii'))
                if DO_VIDEO_TEST and time.time()*1000 - last_photo_time > 500:
                    # 每500ms发送一张图片
                    conversation.append_video(fake_video)
                    last_photo_time = time.time()*1000
            time.sleep(0.1)
    conversation.commit()
    conversation.create_response()
    callback.wait_for_complete()
    b64_player.wait_for_complete()
    print('play audio done')

    # Q2
    test_file_path = 'data/q2_16khz.pcm'
    audio_data: bytes = None
    f = open(test_file_path, 'rb')
    last_photo_time = time.time()*1000
    if os.path.getsize(test_file_path):
        while True:
            audio_data = f.read(3200)
            if not audio_data:
                break
            else:
                conversation.append_audio(base64.b64encode(audio_data).decode('ascii'))
                if DO_VIDEO_TEST and time.time()*1000 - last_photo_time > 500:
                    # 每500ms发送一张图片
                    conversation.append_video(fake_video)
                    last_photo_time = time.time()*1000
            time.sleep(0.1)
    conversation.commit()
    conversation.create_response()
    callback.wait_for_complete()
    b64_player.wait_for_complete()
    print('play audio done')

