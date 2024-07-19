#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
#  MIT License  (https://opensource.org/licenses/MIT)
import json
import os

import dashscope
from dashscope.audio.asr import Recognition

# Set your DashScope API key. More information: https://help.aliyun.com/document_detail/2712195.html
if 'DASHSCOPE_API_KEY' in os.environ:
    dashscope.api_key = os.environ['DASHSCOPE_API_KEY']
    # in fact,if you have set DASHSCOPE_API_KEY in your environment variable,
    # you can ignore this, and the sdk will automatically get the api_key from the environment variable
else:
    dashscope.api_key = '<your-dashscope-api-key>'
    # if you can not set api_key in your environment variable,
    # you can set it here by code

# Initialize recognition service by sync call
# you can customize the recognition parameters, like model, format, sample_rate
# for more information, please refer to https://help.aliyun.com/document_detail/2712536.html
recognition = Recognition(
    model='paraformer-realtime-v2',
    # 'paraformer-realtime-v1'、'paraformer-realtime-8k-v1'
    format='wav',
    # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
    sample_rate=16000,  # supported 8000、16000
    callback=None)

# Please replace the path with your audio file path
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, '../..', 'sampledata',
                         'hello_world_male_16k_16bit_mono.wav')
print('Input file_path is: %s' % file_path)

# Start recognition with the audio file
result = recognition.call(file_path)

# Check the result
print(json.dumps(result, indent=4, ensure_ascii=False))