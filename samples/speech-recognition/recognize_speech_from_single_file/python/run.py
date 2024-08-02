# coding=utf-8
#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import json
import os

import dashscope
from dashscope.audio.asr import Recognition, RecognitionResult
from samples.utils.python import AudioDecoder


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

    def recognize_file(self, file_path: str) -> RecognitionResult:
        # Initialize recognition service by sync call
        # you can customize the recognition parameters, like model, format, sample_rate
        # for more information, please refer to https://help.aliyun.com/document_detail/2712536.html
        recognition = Recognition(
            model='paraformer-realtime-v2',
            # 'paraformer-realtime-v1'、'paraformer-realtime-8k-v1'
            format='pcm',
            # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
            sample_rate=16000,  # supported 8000、16000
            callback=None)

        # Start recognition with the audio file
        return recognition.call(file_path)


# main function
if __name__ == '__main__':
    init_dashscope_api_key()

    # Please replace the path with your audio file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '../..', 'sampledata',
                             "sample_audio.mp3")
    print('Input file is: %s' % file_path)

    decoded_file_path = os.path.join(current_dir,
                                     "temple_decoded.pcm")

    # Decode your audio/video file to 16k 16bit mono pcm file to current directory
    AudioDecoder.convert_to_pcm(file_path, decoded_file_path)

    # Initialize recognition
    speech_recognizer = RecognizeSpeechFromSingleFile()
    result = speech_recognizer.recognize_file(decoded_file_path)

    # Check the result
    print(json.dumps(result, indent=4, ensure_ascii=False))

    # Remove the decoded file
    os.remove(decoded_file_path)
