#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
# MIT License  (https://opensource.org/licenses/MIT)
import os

import dashscope
from dashscope.audio.tts_v2 import AudioFormat, SpeechSynthesizer

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
file_to_save = 'result.mp3'

# Initialize the speech synthesizer
# you can customize the synthesis parameters, like voice, format, sample_rate or other parameters
speech_synthesizer = SpeechSynthesizer(
    model='cosyvoice-v1',
    voice='longxiaochun',
    format=AudioFormat.MP3_22050HZ_MONO_256KBPS,
    callback=None)

# Synthesize speech with given text, sync call and return the audio data in result
# for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
result = speech_synthesizer.call(text_to_synthesize)

# Save the synthesized audio to a file
with open(file_to_save, 'wb') as f:
    f.write(result.get_audio_data())

print('Synthesized text %s to file : %s' % (text_to_synthesize, file_to_save))
