#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import sys
import threading
import time

from dashscope import Client

# This demo shows how to use qwen-audio-3.0-asr-flash-streaming with a precompiled
# vocabulary: create the vocabulary list to get its id, pass the id when recognizing,
# and delete the list afterwards.
# for more information, please refer to https://help.aliyun.com/document_detail/2712536.html

# supported model : 'qwen-audio-3.0-asr-flash-streaming'
MODEL = 'qwen-audio-3.0-asr-flash-streaming'

# the prefix of your vocabulary name
PREFIX = 'demo'


def get_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']
    return '<your-dashscope-api-key>'


def get_workspace():
    '''
    The qwen-audio series models are served under a workspace-specific endpoint.
    The workspace id can be found on the Alibaba Cloud Model Studio console.
    '''
    workspace_id = os.environ.get('DASHSCOPE_WORKSPACE_ID')
    if not workspace_id:
        print('the environment variable DASHSCOPE_WORKSPACE_ID is required, '
              'because the qwen-audio series models are served under a '
              'workspace-specific endpoint. Please set it to your Model Studio '
              'workspace id, for example: export DASHSCOPE_WORKSPACE_ID=llm-xxxxxx')
        sys.exit(1)
    return workspace_id


def recognize_speech_with_vocabulary(audio_path):
    api_key = get_api_key()
    workspace_id = get_workspace()

    client = Client(api_key=api_key, workspace=workspace_id)
    vocabulary_id = None
    recognition = None
    try:
        # define the precompiled vocabulary.
        # 'weight' accepts [1, 5] (regular hotword, 4 recommended) or 50 (super
        # hotword). A super hotword boosts recall dramatically, but at most 50 of
        # them are allowed and only the qwen-audio-3.0-asr-flash-streaming /
        # -filetrans / -flash series support it.
        my_vocabulary = [
            {'text': '语音实验室', 'weight': 4},  # regular hotword
            {'text': '通义千问', 'weight': 50},  # super hotword
        ]

        # create the vocabulary list
        vocab = client.audio.vocabularies.create(
            prefix=PREFIX,
            target_model=MODEL,
            vocabulary=my_vocabulary,
        )
        vocabulary_id = vocab.vocabulary_id
        print('vocabulary created with id: {}'.format(vocabulary_id))

        # Wait until the vocabulary becomes usable. The V2 SDK returns the
        # vocabulary object directly; if the service exposes a status field we
        # poll it, otherwise we proceed after a short backoff.
        status = getattr(vocab, 'status', None)
        deadline = time.monotonic() + 60
        while status and status != 'OK' and time.monotonic() < deadline:
            time.sleep(1)
            vocab = client.audio.vocabularies.get(vocabulary_id)
            status = getattr(vocab, 'status', 'OK')
        if status and status != 'OK':
            print('vocabulary status is not OK: {}'.format(status))
            return
        print('vocabulary status is OK, starting recognition...')

        recognition = client.audio.asr.recognize(
            model=MODEL,
            format='wav',
            sample_rate=16000,
            vocabulary_id=vocabulary_id,
        )
        recognition.start()

        sentences = []

        def consume_results():
            for result in recognition.results():
                sentence = result.get_sentence()
                if sentence and sentence.get('text'):
                    sentences.append(sentence)

        consumer = threading.Thread(target=consume_results)
        consumer.start()

        chunk_size = 3200
        with open(audio_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                recognition.send_audio_frame(chunk)

        recognition.stop()
        consumer.join(timeout=30)

        if sentences:
            print('recognition result: ', [s.get('text') for s in sentences])
        print('[Metric] requestId: {}, first package delay ms: {}'.format(
            recognition.request_id,
            recognition.first_package_delay))
    finally:
        if recognition is not None:
            recognition.close()
        # always delete the vocabulary list to avoid occupying your quota
        if vocabulary_id:
            client.audio.vocabularies.delete(vocabulary_id)
            print('vocabulary deleted.')
        client.close()


# main function
if __name__ == '__main__':
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '../../..', 'sample-data',
        'hello_world_male_16k_16bit_mono.wav')
    file_path = os.path.normpath(file_path)
    if not os.path.exists(file_path):
        print('audio file not found: {}'.format(file_path))
        sys.exit(1)

    recognize_speech_with_vocabulary(file_path)
