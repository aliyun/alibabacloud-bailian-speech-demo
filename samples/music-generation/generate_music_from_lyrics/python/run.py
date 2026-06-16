#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import json
import os
import sys

import requests

MUSIC_GENERATION_ENDPOINT = 'https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation'
MODEL_NAME = 'fun-music-v1'
LYRICS = """[verse]
清晨的阳光穿过窗帘,
咖啡的香气弥漫房间.
翻开昨天未读完的书,
时光就这样悄悄流转.

[chorus]
慢慢来不着急,
生活本该如此惬意.
把烦恼都丢进风里,
拥抱每一个晴天雨季."""
GENDER = 'female'
FILE_TO_SAVE = 'result.mp3'


def get_dashscope_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']
    else:
        return '<your-dashscope-api-key>'


def generate_music_from_lyrics(lyrics, gender, file_path):
    '''
    Generate music with given lyrics, sync call and save the audio data into file_path.
    For more information, please refer to https://help.aliyun.com/zh/model-studio/fun-music
    '''
    api_key = get_dashscope_api_key()

    response = requests.post(
        MUSIC_GENERATION_ENDPOINT,
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
        json={
            'model': MODEL_NAME,
            'input': {
                'lyrics': lyrics,
                'gender': gender,
            },
        },
    )

    response.raise_for_status()
    result = response.json()

    if 'output' in result and 'audio' in result['output'] and 'url' in result['output']['audio']:
        audio_url = result['output']['audio']['url']
        print(f'Music generation successful!')
        print(f'Audio URL: {audio_url}')

        # Download the audio file
        audio_response = requests.get(audio_url)
        audio_response.raise_for_status()

        with open(file_path, 'wb') as f:
            f.write(audio_response.content)
        print(f'Audio saved to: {file_path}')
    else:
        print('Music generation failed or unexpected response format.')
        print(json.dumps(result, indent=4, ensure_ascii=False))

    if 'usage' in result:
        print(f"[Usage] input_tokens: {result['usage'].get('input_tokens', 'N/A')}")


# main function
if __name__ == '__main__':
    generate_music_from_lyrics(lyrics=LYRICS, gender=GENDER, file_path=FILE_TO_SAVE)
