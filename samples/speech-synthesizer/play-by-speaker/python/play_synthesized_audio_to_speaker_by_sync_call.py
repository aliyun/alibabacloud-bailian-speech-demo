#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
# MIT License  (https://opensource.org/licenses/MIT)
import io
import os

import dashscope
import pyglet  # used to play the audio
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

# Initialize the speech synthesizer
# you can customize the synthesis parameters, like voice, format, sample_rate or other parameters
speech_synthesizer = SpeechSynthesizer(
    model='cosyvoice-v1',
    voice='longxiaochun',
    callback=None)

# Synthesize speech with given text, sync call and return the audio data in result
# for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
result = speech_synthesizer.call(text_to_synthesize)
print('requestId: ', speech_synthesizer.get_last_request_id())
# Check if audio data is available
audio_data = result.get_audio_data()

# codes below are used to play the audio data
if audio_data is not None:
    # Use io.BytesIO to convert the audio data to a file-like object
    audio_buffer = io.BytesIO(audio_data)

    # Load and play the MP3 data using pyglet
    sound = pyglet.media.load('', file=audio_buffer, streaming=False)
    player = pyglet.media.Player()
    player.queue(sound)

    # Register an event handler to be called when playback finishes
    @player.event
    def on_eos():
        print('Playback finished.')
        pyglet.app.exit()  # Exit the pyglet application

    # Start play
    player.play()
    print('Playback started.')
    print('synthesized audio with text %s is playing ...' % text_to_synthesize)

    # This starts the pyglet event loop
    pyglet.app.run()
else:
    print('Failed to obtain audio data.')
# audio play codes over
