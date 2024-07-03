#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
# MIT License  (https://opensource.org/licenses/MIT)
import io
import os
import subprocess
import threading

import dashscope
import pyaudio
from dashscope.api_entities.dashscope_response import SpeechSynthesisResponse
from dashscope.audio.tts import SpeechSynthesisResult
from dashscope.audio.tts_v2 import (AudioFormat, ResultCallback,
                                    SpeechSynthesizer)

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


# Define a callback to handle the result
class Callback(ResultCallback):
    def __init__(self):
        self.ffmpeg_process = None
        self._stream = None
        self._player = None
        self.play_thread = None
        self.stop_event = threading.Event()
        print('Callback is initialized.')

    def on_open(self):
        print('Speech synthesizer is opened.')
        self._player = pyaudio.PyAudio()  # initialize pyaudio to play audio
        self._stream = self._player.open(
            format=pyaudio.paInt16, channels=1, rate=22050,
            output=True)  # initialize pyaudio stream
        self.ffmpeg_process = subprocess.Popen(
            [
                'ffmpeg', '-i', 'pipe:0', '-f', 's16le', '-ar', '22050', '-ac',
                '1', 'pipe:1'
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )  # initialize ffmpeg to decode mp3

    def on_complete(self):
        print('Speech synthesizer data receiving is completed.')
        self.ffmpeg_process.stdin.close()
        self.ffmpeg_process.wait()
        self.play_thread.join()

    def on_error(self, response: SpeechSynthesisResponse):
        print('Speech synthesizer failed, response is %s' % (str(response)))
        self.stop_event.set()
        if self.play_thread is not None:
            self.play_thread.join()

    def on_close(self):
        print('Speech synthesizer is play done.')
        self._stream.stop_stream()
        self._stream.close()
        self._player.terminate()
        if self.ffmpeg_process:
            self.ffmpeg_process.terminate()

    def play_audio(self):
        # play audio with pcm data decode by ffmpeg
        while not self.stop_event.is_set():
            pcm_data = self.ffmpeg_process.stdout.read(1024)
            if pcm_data:
                self._stream.write(pcm_data)
            else:
                break

    def on_event(self, synthesizer_result: SpeechSynthesisResult):
        audio_frame = synthesizer_result.get_audio_frame()
        if audio_frame is not None:
            # use ffmpeg to decode mp3
            self.ffmpeg_process.stdin.write(audio_frame)
            if self.play_thread is None:
                # initialize play thread
                print('start play thread')
                self._stream.start_stream()
                self.play_thread = threading.Thread(target=self.play_audio)
                self.play_thread.start()
                print(
                    f'synthesized audio with text {text_to_synthesize} is playing ...'
                )


# Call the speech synthesizer callback
synthesizer_callback = Callback()

# Initialize the speech synthesizer
# you can customize the synthesis parameters, like voice, format, sample_rate or other parameters
speech_synthesizer = SpeechSynthesizer(
    model='cosyvoice-v1',
    voice='longxiaochun',
    format=AudioFormat.MP3_22050HZ_MONO_256KBPS,
    callback=synthesizer_callback)
# Synthesize speech with given text, sync call and return the audio data in result
# for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
result = speech_synthesizer.call(text_to_synthesize)
print('requestId: ', speech_synthesizer.get_last_request_id())
