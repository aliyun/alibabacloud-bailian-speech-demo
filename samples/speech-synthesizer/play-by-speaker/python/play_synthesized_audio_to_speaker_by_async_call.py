#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
# MIT License  (https://opensource.org/licenses/MIT)
import os
import threading

import dashscope
from dashscope.audio.tts_v2 import *
from RealtimeMp3Player import RealtimeMp3Player

# This sample code demonstrates how to decode MP3 audio into PCM format and play it using subprocess and pyaudio.
# Decoding MP3 to PCM before playback is a common approach to audio data handling.
# Alternatively, other libraries can be utilized either to decode MP3 or to play the audio directly.

# Set your DashScope API key. More information: https://help.aliyun.com/document_detail/2712195.html
if 'DASHSCOPE_API_KEY' in os.environ:
    dashscope.api_key = os.environ['DASHSCOPE_API_KEY']
    # in fact,if you have set DASHSCOPE_API_KEY in your environment variable,
    # you can ignore this, and the sdk will automatically get the api_key from the environment variable
else:
    dashscope.api_key = '<your-dashscope-api-key>'
    # if you can not set api_key in your environment variable,
    # you can set it here by code

text_to_synthesize = '欢迎体验阿里云百炼大模型语音合成服务！'


player = RealtimeMp3Player()
# start player
player.start()

complete_event = threading.Event()

# Define a callback to handle the result


class Callback(ResultCallback):
    def on_open(self):
        print('websocket is open.')

    def on_complete(self):
        print('speech synthesis task complete successfully.')
        complete_event.set()

    def on_error(self, message: str):
        print(f'speech synthesis task failed, {message}')

    def on_close(self):
        print('websocket is closed.')

    def on_event(self, message):
        print(f'recv speech synthsis message {message}')

    def on_data(self, data: bytes) -> None:
        # save audio to file
        player.write(data)


# Call the speech synthesizer callback
synthesizer_callback = Callback()

# Initialize the speech synthesizer
# you can customize the synthesis parameters, like voice, format, sample_rate or other parameters
speech_synthesizer = SpeechSynthesizer(
    model='cosyvoice-v1',
    voice='longxiaochun',
    callback=synthesizer_callback)
# Synthesize speech with given text, sync call and return the audio data in result
# for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
result = speech_synthesizer.call(text_to_synthesize,timeout_millis=10*1000)
print('requestId: ', speech_synthesizer.get_last_request_id())
complete_event.wait()
player.stop()