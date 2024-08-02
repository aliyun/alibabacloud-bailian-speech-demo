# coding=utf-8
#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import json
import os

import dashscope
from dashscope.audio.asr import Recognition, RecognitionResult


def init_dashscope_api_key():
    """
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ['DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually


class RecognizeSpeechFromSingleFile:
    def __init__(self):
        pass

    def recognize_file(self,file_name: str) -> RecognitionResult:
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
                                 file_name)
        print('Input file is: %s' % file_path)

        # Start recognition with the audio file
        return recognition.call(file_path)


# main function
if __name__ == '__main__':
    init_dashscope_api_key()
    # Initialize recognition
    speech_recognizer = RecognizeSpeechFromSingleFile()
    result = speech_recognizer.recognize_file('hello_world_male_16k_16bit_mono.wav')

    # Check the result
    print(json.dumps(result, indent=4, ensure_ascii=False))
