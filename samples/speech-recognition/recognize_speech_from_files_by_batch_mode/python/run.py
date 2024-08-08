# coding=utf-8
#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import json
import os
import sys
from http import HTTPStatus
import dashscope
from dashscope.api_entities.dashscope_response import TranscriptionResponse

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../utils/python'))
from TranscriptionResultUtil import handle_transcription_result

def init_dashscope_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ['DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually


def submit_transcription_job() -> TranscriptionResponse:
    """
        Submit the transcription task files list
        the transcription api supports most of the common audio formats
        you can check supported formats and other parameters here: https://help.aliyun.com/document_detail/2712535.html
        transcription api supports 100 files at most in one job, and each file size should be less than 2GB
    """
    #

    # Submit the transcription task
    task_response = dashscope.audio.asr.Transcription.async_call(
        model='paraformer-v2',
        # 'paraformer-8k-v1', 'paraformer-mtl-v1'
        file_urls=[
            'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_example_1.wav',
            'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/sample_video_poetry.mp4',
            'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/long_audio_demo_cn.mp3'
        ])
    # This is the description of 'file_urls'.
    # You need to provide a URL from which the file can be downloaded via HTTP.
    # Typically, we can **store these files in public cloud storage services (such as Alibaba Cloud OSS)**
    # and share a publicly accessible link.
    # Note that it is best to add an expiration time to these links,
    # to prevent third-party access if the file address is leaked.
    return task_response


def retrieve_transcription_result(transcription_response: TranscriptionResponse) -> None:
    """
        get the transcription result
    """

    transcribe_response = dashscope.audio.asr.Transcription.wait(
        task=transcription_response.output.task_id)
    if transcribe_response.status_code == HTTPStatus.OK:
        print("transcription result : ")
        print(json.dumps(transcribe_response.output, indent=4, ensure_ascii=False))
        # you will get the transcription result in the transcribe_response.output by param : transcription_url
        # transcription_url is a downloadable file of json format transcription result
        handle_transcription_result(transcribe_response)


# run the transcription script
if __name__ == '__main__':
    init_dashscope_api_key()
    transcription_response = submit_transcription_job()
    retrieve_transcription_result(transcription_response)
