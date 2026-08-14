#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import sys
from http import HTTPStatus

import dashscope
from dashscope.audio.asr import Transcription

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../../utils/python'))

from TranscriptionResultUtil import handle_transcription_result

# This demo submits a file transcription task asynchronously and blocks the current
# thread until the task finishes (async submit + synchronous wait).
# for more information, please refer to https://help.aliyun.com/document_detail/2712535.html

# supported model : 'qwen-audio-3.0-asr-flash-filetrans'
MODEL = 'qwen-audio-3.0-asr-flash-filetrans'

# the audio url, must be accessible from the public network
AUDIO_URL = 'https://gw.alipayobjects.com/os/bmw-prod/0574ee2e-f494-45a5-820f-63aee583045a.wav'


def init_dashscope():
    '''
    Set your DashScope API-key and workspace endpoint. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ[
            'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually

    # the qwen-audio filetrans model is served under a workspace-specific endpoint
    workspace_id = os.environ.get('DASHSCOPE_WORKSPACE_ID', '<your-workspace-id>')
    dashscope.base_http_api_url = (
        f'https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1')


# main function
if __name__ == '__main__':
    init_dashscope()

    # async submit the transcription task, returns immediately with a task id
    # language_hints (optional): zh=Chinese, en=English. Leave it unset to let the
    # model detect the language automatically. qwen-audio-3.0-asr-flash-filetrans
    # supports up to 4 values (only the first 4 take effect).
    task_response = Transcription.async_call(model=MODEL,
                                             language_hints=['zh', 'en'],
                                             file_urls=[AUDIO_URL])
    if task_response.status_code != HTTPStatus.OK:
        print('task submission failed: {}'.format(task_response.message))
        sys.exit(1)

    task_id = task_response.output.task_id
    print('transcription task submitted, task id: {}'.format(task_id))

    # block until the task finishes (succeeded or failed)
    transcribe_response = Transcription.wait(task=task_id)
    if transcribe_response.status_code == HTTPStatus.OK:
        # download the transcription_url and print the recognized text
        handle_transcription_result(transcribe_response)
        print('transcription done!')
    else:
        print('transcription failed: {}'.format(transcribe_response.message))
