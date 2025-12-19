# !/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import json
import os
import sys

import dashscope

from dashscope.audio.asr import *


def init_dashscope_api_key():
    """
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ[
            'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually


# main function
if __name__ == '__main__':
    init_dashscope_api_key()

    # Please replace the path with your audio file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '../../..', 'sample-data',
                             'hello_world_male_16k_16bit_mono.wav')
    print('Input file is: %s' % file_path)

    recognition = Recognition(
        model='fun-asr-realtime',
        format='wav',
        sample_rate=16000,
        callback=None,
    )
    result = recognition.call(file_path)
    sentence_list = result.get_sentence()
    if sentence_list is None:
        print('No result')
        print(result)
    else:
        print('The brief result is:  ')
        for sentence in sentence_list:
            print(sentence['text'])
        print(
            '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
            .format(
                recognition.get_last_request_id(),
                recognition.get_first_package_delay(),
                recognition.get_last_package_delay(),
            ))
        if sentence_list is not None:
            with open('result.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(sentence_list, indent=4))
        print('Full recognition result is saved into file: result.json')
