#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
# MIT License  (https://opensource.org/licenses/MIT)
import os
import queue
import threading
import time

import dashscope
from dashscope.audio.tts_v2 import *
from pcm_player import PcmPlayer

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


class Callback(ResultCallback):
    def __init__(self, player: PcmPlayer):
        self.player = player

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
        self.player.play(data)


class SpeechSynthesisPlayer:
    # Synthesize speech with given text, sync call and return the audio data in result
    # you can customize the synthesis parameters, like model, format, sample_rate or other parameters
    # for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
    def __init__(self):
        print("init synthesizer")
        self.message_queue = queue.Queue()
        self._player = PcmPlayer()
        self.synthesizer_callback = Callback(self._player)
        consumer_thread = threading.Thread(target=self.consumer, args=())
        consumer_thread.start()

    def interrupt(self):
        self._player.cancel_play()

    def consumer(self):
        # Call the speech synthesizer callback
        self.create_synthesizer()
        while True:
            message = self.message_queue.get()
            if message == "complete":
                self.synthesizer.streaming_complete()
                # notify tts player audio complete
                self.streaming_complete()
                break
            else:
                print("streaming synthesizer call with text: ", message)
                self.synthesizer.streaming_call(message)
                self.message_queue.task_done()  # 表示任务已完成

    def create_synthesizer(self):
        self.synthesizer = SpeechSynthesizer(
            model='cosyvoice-v1',
            voice='longxiaochun',
            format=AudioFormat.PCM_24000HZ_MONO_16BIT,
            callback=self.synthesizer_callback)
        # start player
        print("start player")
        self._player.start_play()

    def call_synthesizer(self, text: str):
        # Start the synthesizer with streaming in text
        self.message_queue.put_nowait(text)

    def streaming_complete(self):
        self.message_queue.put_nowait("complete")
