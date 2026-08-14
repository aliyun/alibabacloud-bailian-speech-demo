#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import sys

import dashscope
from dashscope.audio.asr import Recognition, VocabularyService

# This demo shows how to use qwen-audio-3.0-asr-flash-streaming with a precompiled
# vocabulary: create the vocabulary list to get its id, pass the id when recognizing,
# and delete the list afterwards.
# for more information, please refer to https://help.aliyun.com/document_detail/2712536.html

# supported model : 'qwen-audio-3.0-asr-flash-streaming'
MODEL = 'qwen-audio-3.0-asr-flash-streaming'

# the prefix of your vocabulary name
PREFIX = 'demo'


def init_dashscope_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ[
            'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually


def init_dashscope_endpoint():
    '''
    The qwen-audio series models are served under a workspace-specific endpoint,
    so both the HTTP and the WebSocket base urls have to be redirected to
    https://{workspace_id}.cn-beijing.maas.aliyuncs.com . The workspace id can be
    found on the Alibaba Cloud Model Studio console.
    '''
    workspace_id = os.environ.get('DASHSCOPE_WORKSPACE_ID')
    if not workspace_id:
        print('the environment variable DASHSCOPE_WORKSPACE_ID is required, '
              'because the qwen-audio series models are served under a '
              'workspace-specific endpoint. Please set it to your Model Studio '
              'workspace id, for example: export DASHSCOPE_WORKSPACE_ID=llm-xxxxxx')
        sys.exit(1)
    dashscope.base_http_api_url = (
        f'https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1')
    dashscope.base_websocket_api_url = (
        f'wss://{workspace_id}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'
    )


def recognize_speech_with_vocabulary(audio_path):
    service = VocabularyService()

    # define the precompiled vocabulary.
    # 'weight' accepts [1, 5] (regular hotword, 4 recommended) or 50 (super
    # hotword). A super hotword boosts recall dramatically, but at most 50 of
    # them are allowed and only the qwen-audio-3.0-asr-flash-streaming /
    # -filetrans / -flash series support it.
    my_vocabulary = [
        {'text': '语音实验室', 'weight': 4},  # regular hotword
        {'text': '通义千问', 'weight': 50},  # super hotword
    ]

    vocabulary_id = None
    try:
        # create the vocabulary list
        vocabulary_id = service.create_vocabulary(prefix=PREFIX,
                                                  target_model=MODEL,
                                                  vocabulary=my_vocabulary)
        print('vocabulary created with id: {}'.format(vocabulary_id))

        status_info = service.query_vocabulary(vocabulary_id)
        if status_info.get('status') != 'OK':
            print('vocabulary status is not OK: {}'.format(status_info))
            return
        print('vocabulary status is OK, starting recognition...')

        recognition = Recognition(model=MODEL,
                                  format='wav',
                                  sample_rate=16000,
                                  callback=None)

        # pass the precompiled vocabulary id when recognizing
        result = recognition.call(file=audio_path, phrase_id=vocabulary_id)
        print('recognition result: ', result.output)
        print('[Metric] requestId: {}, first package delay ms: {}'.format(
            recognition.get_last_request_id(),
            recognition.get_first_package_delay()))
    finally:
        # always delete the vocabulary list to avoid occupying your quota
        if vocabulary_id:
            service.delete_vocabulary(vocabulary_id)
            print('vocabulary deleted.')


# main function
if __name__ == '__main__':
    init_dashscope_api_key()
    init_dashscope_endpoint()

    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '../../..', 'sample-data',
        'hello_world_male_16k_16bit_mono.wav')
    file_path = os.path.normpath(file_path)
    if not os.path.exists(file_path):
        print('audio file not found: {}'.format(file_path))
        sys.exit(1)

    recognize_speech_with_vocabulary(file_path)
