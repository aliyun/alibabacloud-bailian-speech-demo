#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
# MIT License  (https://opensource.org/licenses/MIT)
import os
import time

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

player = RealtimeMp3Player()
# start player
player.start()


# Define a callback to handle the result


class Callback(ResultCallback):
    def on_open(self):
        print('websocket is open.')

    def on_complete(self):
        print('speech synthesis task complete successfully.')

    def on_error(self, message):
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

test_text = [
    '流式文本语音合成SDK，',
    '可以将输入的文本',
    '合成为语音二进制数据，',
    '相比于非流式语音合成，',
    '流式合成的优势在于实时性',
    '更强。用户在输入文本的同时',
    '可以听到接近同步的语音输出，',
    '极大地提升了交互体验，',
    '减少了用户等待时间。',
    '适用于调用大规模',
    '语言模型（LLM），以',
    '流式输入文本的方式',
    '进行语音合成的场景。',
]

# Synthesize speech with given text, sync call and return the audio data in result
# you can customize the synthesis parameters, like model, format, sample_rate or other parameters
# for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
synthesizer = SpeechSynthesizer(
    model='cosyvoice-v1',
    voice='longxiaochun',
    format=AudioFormat.MP3_22050HZ_MONO_256KBPS,
    callback=synthesizer_callback,
)

# Start the synthesizer with streaming in text
for text in test_text:
    synthesizer.streaming_call(text)
    time.sleep(0.1)
synthesizer.streaming_complete()
# stop realtime mp3 player
player.stop()
