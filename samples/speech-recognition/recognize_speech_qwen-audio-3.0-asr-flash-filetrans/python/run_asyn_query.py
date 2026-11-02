#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import json
import os
import sys
import time

import requests
from dashscope import Client

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../../utils/python'))

# This demo submits a file transcription task asynchronously and polls the task
# result with fetch(), so you can query the result whenever you need it.
# for more information, please refer to https://help.aliyun.com/document_detail/2712535.html

# supported model : 'qwen-audio-3.1-asr-flash-filetrans'
MODEL = 'qwen-audio-3.1-asr-flash-filetrans'

# the audio url, must be accessible from the public network
AUDIO_URL = 'https://gw.alipayobjects.com/os/bmw-prod/0574ee2e-f494-45a5-820f-63aee583045a.wav'

# poll interval and max attempts to avoid waiting forever
POLL_INTERVAL_SECONDS = 3
MAX_POLL_ATTEMPTS = 60


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
    The qwen-audio filetrans model is served under a workspace-specific endpoint.
    The workspace id can be found on the Alibaba Cloud Model Studio console.
    '''
    workspace_id = os.environ.get('DASHSCOPE_WORKSPACE_ID', '<your-workspace-id>')
    if not workspace_id or workspace_id == '<your-workspace-id>':
        print('the environment variable DASHSCOPE_WORKSPACE_ID is required, '
              'because the qwen-audio filetrans model is served under a '
              'workspace-specific endpoint. Please set it to your Model Studio '
              'workspace id, for example: export DASHSCOPE_WORKSPACE_ID=llm-xxxxxx')
        sys.exit(1)
    return workspace_id


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


def handle_transcription_result(job):
    """Download each per-file transcription result and print it."""
    results = (job.output or {}).get('results') or []
    for index, result in enumerate(results):
        transcription_url = result.get('transcription_url')
        if transcription_url:
            local_path = './{}_transcription_result.json'.format(index)
            download_file(transcription_url, local_path)
            read_file_and_print_content(local_path)


def poll_until_done(client, task_id):
    '''
    Poll the task status with fetch() until it succeeds or fails, or until the
    max attempts is reached. Returns the final job, or None on timeout.
    '''
    # Use a derived client that does not raise on FAILED status so we can
    # read the terminal status ourselves.
    polling_client = client.with_options(raise_on_error=False)
    for _ in range(MAX_POLL_ATTEMPTS):
        time.sleep(POLL_INTERVAL_SECONDS)  # sleep to avoid throttling
        job = polling_client.audio.asr.jobs.fetch(task_id)
        status = job.status
        print('current status: {}'.format(status))
        if status in ('SUCCEEDED', 'FAILED', 'CANCELED', 'UNKNOWN'):
            return job
    print('task did not finish within {} attempts.'.format(MAX_POLL_ATTEMPTS))
    return None


# main function
if __name__ == '__main__':
    api_key = get_api_key()
    workspace_id = get_workspace()

    client = Client(api_key=api_key, workspace=workspace_id)
    try:
        # async submit the transcription task, returns immediately with a task id
        # language_hints (optional): zh=Chinese, en=English. Leave it unset to let the
        # model detect the language automatically. qwen-audio-3.1-asr-flash-filetrans
        # supports up to 4 values (only the first 4 take effect).
        job = client.audio.asr.jobs.create(
            model=MODEL,
            file_urls=[AUDIO_URL],
            parameters={'language_hints': ['zh', 'en']},
        )
        print('transcription task submitted, task id: {}'.format(job.task_id))

        final_job = poll_until_done(client, job.task_id)
        if final_job and final_job.status == 'SUCCEEDED':
            # download the transcription_url and print the recognized text
            handle_transcription_result(final_job)
            print('transcription done!')
        elif final_job:
            print('transcription failed: {}'.format(final_job.status))
        else:
            sys.exit(1)
    finally:
        client.close()
