#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
#  MIT License  (https://opensource.org/licenses/MIT)

import os

import dashscope
from dashscope.audio.asr import (Recognition, RecognitionCallback,
                                 RecognitionResult)


# Real-time speech recognition callback
class MyRecognitionCallback(RecognitionCallback):
    def on_open(self) -> None:
        print('Recognition open')  # recognition open

    def on_complete(self) -> None:
        print('Recognition complete')  # recognition complete

    def on_error(self, result: RecognitionResult) -> None:
        print('RecognitionCallback task_id: ', result.request_id)
        print('RecognitionCallback error: ', result.message)

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if 'text' in sentence:
            print('RecognitionCallback text: ', sentence['text'])
            if RecognitionResult.is_sentence_end(sentence):
                print(
                    'RecognitionCallback sentence end, request_id:%s, usage:%s'
                    % (result.get_request_id(), result.get_usage(sentence)))

    def on_close(self) -> None:
        print('RecognitionCallback close.')


# Create the recognition callback
callback = MyRecognitionCallback()

# Set your DashScope API key. More information: https://help.aliyun.com/document_detail/2712195.html
if 'DASHSCOPE_API_KEY' in os.environ:
    dashscope.api_key = os.environ['DASHSCOPE_API_KEY']
    # in fact,if you have set DASHSCOPE_API_KEY in your environment variable,
    # you can ignore this, and the sdk will automatically get the api_key from the environment variable
else:
    dashscope.api_key = '<your-dashscope-api-key>'
    # if you can not set api_key in your environment variable,
    # you can set it here by code

# Initialize recognition service by async mode
# you can customize the recognition parameters, like model, format, sample_rate
# for more information, please refer to https://help.aliyun.com/document_detail/2712536.html
recognition = Recognition(
    model='paraformer-realtime-v1',
    # 'paraformer-realtime-v1'、'paraformer-realtime-8k-v1'
    format='wav',
    # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
    sample_rate=16000,  # supported 8000、16000
    callback=callback)

# Please replace the path with your audio file path
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, '..', 'sampledata',
                         'hello_world_male_16k_16bit_mono.wav')
print(f'file_path: {file_path}')

# Start recognition with the audio file
recognition.start()
f = open(file_path, 'rb')
while True:
    chunk = f.read(3200)
    if not chunk:
        break
    else:
        recognition.send_audio_frame(chunk)
f.close()
recognition.stop()
