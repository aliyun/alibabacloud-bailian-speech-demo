#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import json
import os
import sys

from dashscope import Client


def get_api_key():
    """Load DashScope API key from environment or use a placeholder."""
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']
    return '<your-dashscope-api-key>'


# main function
if __name__ == '__main__':
    api_key = get_api_key()

    # Please replace the path with your audio file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '../../..', 'sample-data',
                             'hello_world_male_16k_16bit_mono.wav')
    print('Input file is: %s' % file_path)

    client = Client(api_key=api_key)
    recognition = None
    try:
        recognition = client.audio.asr.recognize(
            model='fun-asr-realtime',
            # 'paraformer-realtime-v2' is also supported by the V2 SDK
            format='wav',
            sample_rate=16000,
        )
        recognition.start()

        chunk_size = 3200
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                recognition.send_audio_frame(chunk)

        recognition.stop()

        sentence_list = []
        for result in recognition.results():
            sentence = result.get_sentence()
            if sentence is None or 'text' not in sentence:
                continue
            if result.is_sentence_end():
                print(sentence['text'])
            sentence_list.append(sentence)

        if not sentence_list:
            print('No result')
        else:
            print('The brief result is:  ')
            for sentence in sentence_list:
                print(sentence['text'])
            print(
                '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
                .format(
                    recognition.request_id,
                    recognition.first_package_delay,
                    recognition.last_package_delay,
                ))
            with open('result.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(sentence_list, indent=4))
            print('Full recognition result is saved into file: result.json')
    finally:
        if recognition is not None:
            recognition.close()
        client.close()
