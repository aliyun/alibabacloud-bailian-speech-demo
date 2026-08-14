#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import json
import os

import requests

# This demo shows how to call qwen-audio-3.0-asr-flash in non-streaming mode with
# conversation context. The context helps to improve the recognition accuracy of
# proper nouns. See https://help.aliyun.com/document_detail/2712536.html

# supported model : 'qwen-audio-3.0-asr-flash'
MODEL = 'qwen-audio-3.0-asr-flash'

# the audio url, must be accessible from the public network
AUDIO_URL = 'https://gw.alipayobjects.com/os/bmw-prod/0574ee2e-f494-45a5-820f-63aee583045a.wav'

# timeout of the http request, in seconds
REQUEST_TIMEOUT = 60


def get_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    # load API-key from environment variable DASHSCOPE_API_KEY
    return os.environ.get('DASHSCOPE_API_KEY', '<your-dashscope-api-key>')


def get_workspace_id():
    # load workspace id from environment variable DASHSCOPE_WORKSPACE_ID
    return os.environ.get('DASHSCOPE_WORKSPACE_ID', '<your-workspace-id>')


def build_request_body(audio_url):
    '''
    Build the multimodal request body. The two leading text messages act as the
    conversation context, and the last message carries the audio to recognize.
    '''
    messages = [
        {
            'role': 'user',
            'content': [{
                'type': 'input_text',
                'text': '你好啊'
            }]
        },
        {
            'role': 'assistant',
            'content': [{
                'type': 'text',
                'text': '你好啊，我是通义千问，有什么可以帮助你的？'
            }]
        },
        {
            'role': 'user',
            'content': [{
                'type': 'input_audio',
                'input_audio': {
                    'data': audio_url
                }
            }]
        },
    ]
    return {
        'model': MODEL,
        'input': {
            'messages': messages
        },
        'parameters': {
            'format': 'wav',
            'sample_rate': 16000
        }
    }


def recognize_speech(workspace_id, api_key, audio_url):
    url = (f'https://{workspace_id}.cn-beijing.maas.aliyuncs.com'
           '/api/v1/services/aigc/multimodal-generation/generation')
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        # X-DashScope-SSE controls whether to return results in SSE streaming mode.
        # set to 'enable' to receive incremental results, 'disable' for the final result only.
        'X-DashScope-SSE': 'disable',
    }
    response = requests.post(url,
                             headers=headers,
                             json=build_request_body(audio_url),
                             timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()


def extract_text(result):
    '''
    Extract the recognized text from the response. The asr-flash model returns
    the text at output.text, while the generic multimodal shape carries it at
    output.choices[0].message.content[0].text.
    '''
    output = result.get('output', {})
    if output.get('text'):
        return output['text']

    choices = output.get('choices', [])
    if choices:
        content = choices[0].get('message', {}).get('content', [])
        if content:
            return content[0].get('text', '')
    return ''


# main function
if __name__ == '__main__':
    result = recognize_speech(get_workspace_id(), get_api_key(), AUDIO_URL)
    print(json.dumps(result, indent=4, ensure_ascii=False))

    print('recognition result: {}'.format(extract_text(result)))
