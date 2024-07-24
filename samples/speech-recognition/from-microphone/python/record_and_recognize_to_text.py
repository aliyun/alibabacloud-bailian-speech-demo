#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
#  MIT License  (https://opensource.org/licenses/MIT)
import os
import sys
import time

import dashscope
import sounddevice as sd  # To record audio
from dashscope.audio.asr import (Recognition, RecognitionCallback,
                                 RecognitionResult)
import signal
# To listen for keyboard events by pressing 'Ctrl+C' to stop recording and recognition

# Set recording parameters
sample_rate = 16000  # Sample rate (Hz)
channels = 1  # Mono channel
dtype = 'int16'  # Data type
format_pcm = 'pcm'  # the format of the audio data
block_size = 3200  # Number of frames per buffer

# Set your DashScope API key. More information: https://help.aliyun.com/document_detail/2712195.html
if 'DASHSCOPE_API_KEY' in os.environ:
    dashscope.api_key = os.environ['DASHSCOPE_API_KEY']
    # in fact,if you have set DASHSCOPE_API_KEY in your environment variable,
    # you can ignore this, and the sdk will automatically get the api_key from the environment variable
else:
    dashscope.api_key = '<your-dashscope-api-key>'
    # if you can not set api_key in your environment variable,
    # you can set it here by code


# Audio recording callback
def audio_callback(indata, frames, time, status):
    """Send audio data to the recognition service"""
    if status:
        print(status)
    # Convert the recording data to bytes and send it to the recognition service
    buffer = indata.tobytes()
    recognition.send_audio_frame(buffer)


# Real-time speech recognition callback
class MyRecognitionCallback(RecognitionCallback):
    def on_open(self) -> None:
        print('Recognition open')  # recognition open

        # Start the recording stream when recognition starts
        global stream  # global variable 'stream', used to recording audio
        stream = sd.InputStream(samplerate=sample_rate,
                                channels=channels,
                                dtype=dtype,
                                blocksize=block_size,
                                callback=audio_callback)
        stream.start()

    def on_complete(self) -> None:
        print('Recognition complete')  # recognition complete

    def on_error(self, result: RecognitionResult) -> None:
        print('RecognitionCallback task_id: ', result.request_id)
        print('RecognitionCallback error: ', result.message)
        # Stop the audio stream if it is running
        if 'stream' in globals() and stream.active:
            stream.stop()
            stream.close()
        # Forcefully exit the program
        sys.exit(1)

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if 'text' in sentence:
            print('RecognitionCallback text: ', sentence['text'])
            if RecognitionResult.is_sentence_end(sentence):
                print(
                    'RecognitionCallback sentence end, request_id:%s, usage:%s'
                    % (result.get_request_id(), result.get_usage(sentence)))

    def on_close(self) -> None:
        print('Recognition close')


# Create the recognition callback
callback = MyRecognitionCallback()

# Initialize recognition service by async mode
# you can customize the recognition parameters, like model, format, sample_rate
# for more information, please refer to https://help.aliyun.com/document_detail/2712536.html
recognition = Recognition(
    model='paraformer-realtime-v1',
    # 'paraformer-realtime-v1'、'paraformer-realtime-8k-v1'
    format='pcm',
    # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
    sample_rate=sample_rate,  # supported 8000、16000
    callback=callback)
# Start recognition
recognition.start()
print('Recognition start')


def signal_handler(sig, frame):
    print("Ctrl+C pressed! Performing quit recognition and exit...")
    # 执行任何必要的清理操作
    # Stop recording
    if 'stream' in globals():
        stream.stop()
        stream.close()
    # Stop recording and recognition
    print('Recognition stop')
    recognition.stop()
    # Forcefully exit the program
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
print("Press 'Ctrl+C' to stop recording and recognition.")
# Create a keyboard listener to stop the recording and recognition
# 模拟长时间运行的任务
while True:
    time.sleep(0.1)
