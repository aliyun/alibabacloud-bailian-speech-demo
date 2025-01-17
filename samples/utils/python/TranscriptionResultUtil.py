# !/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)
import json
import random
import time

import requests
from dashscope.api_entities.dashscope_response import TranscriptionResponse


def handle_transcription_result(transcribe_response: TranscriptionResponse):
    """
        Handle the transcription result. download the result url and print the transcription result
    """
    if transcribe_response.output.task_status == 'SUCCEEDED':
        results = transcribe_response.output.get('results')
        if results:
            __result_turn = 0
            for result in json.loads(json.dumps(results)):
                transcription_url = result['transcription_url']
                if transcription_url:
                    # download the transcription result
                    __local_file_path = './' + str(
                        __result_turn) + '_transcription_result.json'
                    download_file(transcription_url, __local_file_path)
                    # read the transcription result
                    read_file_and_print_content(__local_file_path)
                __result_turn += 1


def download_file(url, local_path):
    """
        Downloads a file from a given URL to a local path.

        Parameters:
        - url: File URL Address
        - local_path: Local Path where the file will be saved

        Returns:
        None
    """
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f'Failed to download the file: {e} ,retrying...')
        time.sleep(random.randint(1, 5))
        response = requests.get(url,
                                allow_redirects=True,
                                verify=False,
                                timeout=15)

    with open(local_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


def read_file_and_print_content(file_path):
    """
        Reads a file and retrieves its content.

        Parameter:
        - file_path: File Path

        Return Value:
        String representation of file content.
    """
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
