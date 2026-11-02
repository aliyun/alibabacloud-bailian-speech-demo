#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import json
import os
import re
import sys
from urllib import request

from dashscope import Client


def get_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']
    return '<your-dashscope-api-key>'


def parse_sensevoice_result(data,
                            keep_trans=True,
                            keep_emotions=True,
                            keep_events=True):
    '''
    本工具用于解析 sensevoice 识别结果
    keep_trans: 是否保留转写文本，默认为True
    keep_emotions: 是否保留情感标签，默认为True
    keep_events: 是否保留事件标签，默认为True
    '''
    # 定义要保留的标签
    emotion_list = ['NEUTRAL', 'HAPPY', 'ANGRY', 'SAD']
    event_list = ['Speech', 'Applause', 'BGM', 'Laughter']

    # 所有支持的标签
    all_tags = [
        'Speech', 'Applause', 'BGM', 'Laughter', 'NEUTRAL', 'HAPPY', 'ANGRY',
        'SAD', 'SPECIAL_TOKEN_1'
    ]
    tags_to_cleanup = []
    for tag in all_tags:
        tags_to_cleanup.append(f'<|{tag}|> ')
        tags_to_cleanup.append(f'<|/{tag}|>')
        tags_to_cleanup.append(f'<|{tag}|>')

    def get_clean_text(text: str):
        for tag in tags_to_cleanup:
            text = text.replace(tag, '')
        pattern = r'\s{2,}'
        text = re.sub(pattern, ' ', text).strip()
        return text

    for item in data['transcripts']:
        for sentence in item['sentences']:
            if keep_emotions:
                # 提取 emotion
                emotions_pattern = r'<\|(' + '|'.join(emotion_list) + r')\|>'
                emotions = re.findall(emotions_pattern, sentence['text'])
                sentence['emotion'] = list(set(emotions))
                if not sentence['emotion']:
                    sentence.pop('emotion', None)

            if keep_events:
                # 提取 event
                events_pattern = r'<\|(' + '|'.join(event_list) + r')\|>'
                events = re.findall(events_pattern, sentence['text'])
                sentence['event'] = list(set(events))
                if not sentence['event']:
                    sentence.pop('event', None)

            if keep_trans:
                # 提取纯文本
                sentence['text'] = get_clean_text(sentence['text'])
            else:
                sentence.pop('text', None)

        if keep_trans:
            item['text'] = get_clean_text(item['text'])
        else:
            item.pop('text', None)
        item['sentences'] = list(
            filter(lambda x: 'text' in x or 'emotion' in x or 'event' in x,
                   item['sentences']))
    return data


def submit_and_wait_transcription_job():
    """
        Submit the transcription task files list and get the transcription result
        the transcription api supports most of the common audio formats
        you can check supported formats and other parameters here: https://help.aliyun.com/document_detail/2712535.html
        transcription api supports 100 files at most in one job, and each file size should be less than 2GB
    """
    api_key = get_api_key()
    # Use raise_on_error=False so we can inspect the terminal task status
    # ourselves, matching the original 1.x status_code check.
    client = Client(api_key=api_key, raise_on_error=False)
    file_urls = [
        'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_example_1.wav',
        'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/long_audio_demo_en.aac'
    ]
    try:
        # In DashScope SDK 2.x the batch filetranscription service is
        # exposed through client.audio.asr.transcribe. The default
        # qwen-audio-3.1-asr-flash-filetrans model is used here because
        # sensevoice-v1 is not available on the v2 batch endpoint.
        # The endpoint used in this environment accepts only one file_url
        # per job, so we submit a separate job for each file.
        for file_url in file_urls:
            job = client.audio.asr.transcribe(
                model='qwen-audio-3.1-asr-flash-filetrans',
                file_urls=[file_url],
                parameters={'language_hints': ['en']},
            )

            print('task_id: ', job.task_id)

            if job.status == 'SUCCEEDED':
                transcription = job.output
                if transcription.get('subtask_status') == 'SUCCEEDED':
                    url = transcription['transcription_url']
                    result = json.loads(request.urlopen(url).read().decode('utf8'))
                    print(
                        json.dumps(parse_sensevoice_result(result),
                                   indent=4,
                                   ensure_ascii=False))
                else:
                    print('transcription failed!')
                    print(transcription)
            else:
                print('Error: ', job.status)
        print('transcription done!')
    finally:
        client.close()


# run the transcription script
if __name__ == '__main__':
    submit_and_wait_transcription_job()
