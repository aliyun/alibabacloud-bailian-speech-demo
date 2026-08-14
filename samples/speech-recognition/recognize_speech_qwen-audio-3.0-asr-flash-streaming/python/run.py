#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import sys
import time

import dashscope
from dashscope.audio.asr import (Recognition, RecognitionCallback,
                                 RecognitionResult)

# This demo shows the most basic real-time speech recognition with
# qwen-audio-3.0-asr-flash-streaming: read a local audio file, send it to the
# service frame by frame, and print the recognition result from the callback.
#
# Advanced capabilities are demonstrated in dedicated samples:
#   - conversation context   : ../../recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-context
#   - pre-created vocabulary : ../../recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-vocabulary
#
# for more information, please refer to https://help.aliyun.com/document_detail/2712536.html

# supported model : 'qwen-audio-3.0-asr-flash-streaming'
MODEL = 'qwen-audio-3.0-asr-flash-streaming'


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


# Real-time speech recognition callback
class MyRecognitionCallback(RecognitionCallback):
    def on_open(self) -> None:
        print('RecognitionCallback open.')

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if not sentence or 'text' not in sentence:
            return
        if RecognitionResult.is_sentence_end(sentence):
            print('RecognitionCallback sentence end, text: ', sentence['text'])
        else:
            # partial recognition result
            print('RecognitionCallback text: ', sentence['text'])

    def on_complete(self) -> None:
        print('RecognitionCallback completed.')

    def on_error(self, result: RecognitionResult) -> None:
        print('RecognitionCallback error: ', result.message)

    def on_close(self) -> None:
        print('RecognitionCallback closed.')


def recognize_speech_from_file(audio_path):
    '''
    Recognize speech from a local audio file and print the result in real time.
    '''
    recognition = Recognition(
        model=MODEL,
        format='wav',  # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr'
        sample_rate=16000,  # supported 8000、16000
        callback=MyRecognitionCallback())

    recognition.start()

    chunk_size = 3200
    with open(audio_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            recognition.send_audio_frame(chunk)
            time.sleep(0.05)  # simulate the real-time audio stream

    recognition.stop()
    print('[Metric] requestId: {}, first package delay ms: {}'.format(
        recognition.get_last_request_id(),
        recognition.get_first_package_delay()))


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

    recognize_speech_from_file(file_path)
