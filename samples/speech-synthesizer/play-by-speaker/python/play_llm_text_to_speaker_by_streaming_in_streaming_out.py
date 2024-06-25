#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
# MIT License  (https://opensource.org/licenses/MIT)
import os
from http import HTTPStatus

import dashscope
from dashscope import Generation
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

    def on_error(self, message: str):
        print(f'speech synthesis task failed, {message}')

    def on_close(self):
        print('websocket is closed.')
        self.file.close()

    def on_event(self, message):
        print(f'recv speech synthsis message {message}')

    def on_data(self, data: bytes) -> None:
        # save audio to file
        player.write(data)


# Call the speech synthesizer callback
synthesizer_callback = Callback()

# Synthesize speech with llm streaming output text, sync call and playback of MP3 audio streams.
# you can customize the synthesis parameters, like model, format, sample_rate or other parameters
# for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
synthesizer = SpeechSynthesizer(
    model='cosyvoice-v1',
    voice='longxiaochun',
    format=AudioFormat.MP3_22050HZ_MONO_256KBPS,
    callback=synthesizer_callback,
)

# Prepare for the LLM call
messages = [{'role': 'user', 'content': '请介绍一下你自己'}]
responses = Generation.call(
    model='qwen-turbo',
    messages=messages,
    result_format='message',  # set result format as 'message'
    stream=True,  # enable stream output
    incremental_output=True,  # enable incremental output
)
for response in responses:
    if response.status_code == HTTPStatus.OK:
        print(response.output.choices[0]['message']['content'], end='')
        # send llm result to synthesizer
        synthesizer.streaming_call(
            response.output.choices[0]['message']['content'])
    else:
        print(
            'Request id: %s, Status code: %s, error code: %s, error message: %s'
            % (
                response.request_id,
                response.status_code,
                response.code,
                response.message,
            ))
synthesizer.streaming_complete()
# stop realtime mp3 player
player.stop()
