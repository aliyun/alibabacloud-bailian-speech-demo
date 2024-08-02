# coding=utf-8
#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import sys
import threading
import dashscope
from dashscope.audio.tts_v2 import *

# add parent directory for utils to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
sys.path.append(parent_dir)

from samples.utils.python.RealtimeMp3Player import RealtimeMp3Player

text_to_synthesize = '欢迎体验阿里云百炼大模型语音合成服务！'

def init_dashscope_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ['DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually

def synthesis_text_to_speech_and_play_by_streaming_mode(text):
    '''
    Synthesize speech with given text by streaming mode, async call and play the synthesized audio in real-time.
    for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
    '''
    player = RealtimeMp3Player()
    # start player
    player.start()

    complete_event = threading.Event()

    # Define a callback to handle the result


    class Callback(ResultCallback):
        def on_open(self):
            self.file = open('result.mp3', 'wb')
            print('websocket is open.')

        def on_complete(self):
            print('speech synthesis task complete successfully.')
            complete_event.set()

        def on_error(self, message: str):
            print(f'speech synthesis task failed, {message}')

        def on_close(self):
            print('websocket is closed.')

        def on_event(self, message):
            # print(f'recv speech synthsis message {message}')
            pass

        def on_data(self, data: bytes) -> None:
            # send to player
            player.write(data)
            # save audio to file
            self.file.write(data)


    # Call the speech synthesizer callback
    synthesizer_callback = Callback()

    # Initialize the speech synthesizer
    # you can customize the synthesis parameters, like voice, format, sample_rate or other parameters
    speech_synthesizer = SpeechSynthesizer(
        model='cosyvoice-v1',
        voice='longxiaochun',
        callback=synthesizer_callback)

    speech_synthesizer.call(text)
    print('Synthesized text: {} requestId: {}'.format(text, speech_synthesizer.get_last_request_id()))
    complete_event.wait()
    player.stop()


# main function
if __name__ == '__main__':
    init_dashscope_api_key()
    synthesis_text_to_speech_and_play_by_streaming_mode(text=text_to_synthesize)