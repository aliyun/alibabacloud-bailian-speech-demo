#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import sys
import threading

from dashscope import Client

# This demo shows the most basic real-time speech recognition with
# qwen-audio-3.0-asr-flash-streaming: read a local audio file, send it to the
# service frame by frame, and print the recognition result.
#
# Advanced capabilities are demonstrated in dedicated samples:
#   - conversation context   : ../../recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-context
#   - pre-created vocabulary : ../../recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-vocabulary
#
# for more information, please refer to https://help.aliyun.com/document_detail/2712536.html

# supported model : 'qwen-audio-3.0-asr-flash-streaming'
MODEL = 'qwen-audio-3.0-asr-flash-streaming'


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


def recognize_speech_from_file(audio_path):
    '''
    Recognize speech from a local audio file and print the result in real time.
    '''
    api_key = get_api_key()
    workspace_id = get_workspace()

    client = Client(api_key=api_key, workspace=workspace_id)
    recognition = None
    try:
        recognition = client.audio.asr.recognize(
            model=MODEL,
            format='wav',  # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr'
            sample_rate=16000,  # supported 8000、16000
        )
        recognition.start()

        def consume_results():
            for result in recognition.results():
                sentence = result.get_sentence()
                if not sentence or 'text' not in sentence:
                    continue
                if result.is_sentence_end():
                    print('ASR sentence end, text: ', sentence['text'])
                else:
                    # partial recognition result
                    print('ASR text: ', sentence['text'])

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

        print('[Metric] requestId: {}, first package delay ms: {}'.format(
            recognition.request_id,
            recognition.first_package_delay))
    finally:
        if recognition is not None:
            recognition.close()
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

    recognize_speech_from_file(file_path)
