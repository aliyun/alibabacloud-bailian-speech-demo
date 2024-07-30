#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
#  MIT License  (https://opensource.org/licenses/MIT)
import json
import os
from http import HTTPStatus

import dashscope

# Set your DashScope API key. More information: https://help.aliyun.com/document_detail/2712195.html
if 'DASHSCOPE_API_KEY' in os.environ:
    dashscope.api_key = os.environ['DASHSCOPE_API_KEY']
    # in fact,if you have set DASHSCOPE_API_KEY in your environment variable,
    # you can ignore this, and the sdk will automatically get the api_key from the environment variable
else:
    dashscope.api_key = '<your-dashscope-api-key>'
    # if you can not set api_key in your environment variable,
    # you can set it here by code

# Submit the transcription task files list
# the transcription api supports most of the common audio formats
# you can check supported formats and other parameters here: https://help.aliyun.com/document_detail/2712535.html
# transcription api supports 100 files at most in one job, and each file size should be less than 2GB

# Submit the transcription task
task_response = dashscope.audio.asr.Transcription.async_call(
    model='sensevoice-v1',
    # 'paraformer-v1'
    file_urls=[
        'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav',
        'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav',
        'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_example_1.wav',
        'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_example_2.wav'
    ])
# This is the description of 'file_urls'.
# You need to provide a URL from which the file can be downloaded via HTTP.
# Typically, we can **store these files in public cloud storage services (such as Alibaba Cloud OSS)**
# and share a publicly accessible link.
# Note that it is best to add an expiration time to these links,
# to prevent third-party access if the file address is leaked.

# get the transcription result
transcribe_response = dashscope.audio.asr.Transcription.wait(
    task=task_response.output.task_id)
if transcribe_response.status_code == HTTPStatus.OK:
    print(json.dumps(transcribe_response.output, indent=4, ensure_ascii=False))
    print('transcription done!')
# you will get the transcription result in the transcribe_response.output by param : transcription_url
# transcription_url is a downloadable file of json format transcription result
