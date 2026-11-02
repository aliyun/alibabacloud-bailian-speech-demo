#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import json
import os
import sys

import requests
from dashscope import Client


def get_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']
    return '<your-dashscope-api-key>'


def download_file(url, local_path):
    """Download a transcription result file."""
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()
    with open(local_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


def read_file_and_print_content(file_path):
    """Read and print the transcribed text."""
    with open(file_path, 'r', encoding='utf-8') as f:
        trans_result = f.read()
        if trans_result:
            trans_result = json.loads(trans_result)
            print('============= transcription for file : ',
                  trans_result['file_url'], ' === START ===')
            for transcript in trans_result['transcripts']:
                for sentence in transcript['sentences']:
                    text = sentence['text']
                    print('==>: ', text)
            print('============= transcription for file : ',
                  trans_result['file_url'], ' ===  END  ===\n\n')


def transcribe_one_file(client, file_url, index):
    """Submit a single-file transcription job and download its result."""
    job = client.audio.asr.transcribe(
        model='fun-asr',
        # 'paraformer-v2' is also supported by the V2 SDK
        file_urls=[file_url],
    )
    print('transcription task id: ', job.task_id)
    print('transcription result : ')
    print(json.dumps(job.output, indent=4, ensure_ascii=False))

    results = (job.output or {}).get('results') or []
    for result in results:
        transcription_url = result.get('transcription_url')
        if transcription_url:
            local_path = './{}_transcription_result.json'.format(index)
            download_file(transcription_url, local_path)
            read_file_and_print_content(local_path)


def submit_and_wait_transcription():
    """
        Submit the transcription task files list
        the transcription api supports most of the common audio formats
        you can check supported formats and other parameters here: https://help.aliyun.com/document_detail/2712535.html
        transcription api supports 100 files at most in one job, and each file size should be less than 2GB
    """
    api_key = get_api_key()
    # Use raise_on_error=False so we can inspect the terminal task status
    # ourselves, matching the original 1.x status_code check.
    client = Client(api_key=api_key, raise_on_error=False)
    try:
        file_urls = [
            'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_example_1.wav',
            'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/sample_video_poetry.mp4',
            'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/long_audio_demo_cn.mp3'
        ]
        # The V2 fun-asr endpoint accepts one file_url per job in this
        # environment, so submit a job for each URL and download each result.
        for index, file_url in enumerate(file_urls):
            print(f'\n===== processing file {index} =====')
            transcribe_one_file(client, file_url, index)
    finally:
        client.close()


# run the transcription script
if __name__ == '__main__':
    submit_and_wait_transcription()
