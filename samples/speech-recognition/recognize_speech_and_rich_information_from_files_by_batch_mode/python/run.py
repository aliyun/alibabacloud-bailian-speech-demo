# !/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import json
import os
import re
import sys
from http import HTTPStatus
from urllib import request

import dashscope

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../../utils/python'))

from dashscope.api_entities.dashscope_response import TranscriptionResponse


def init_dashscope_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ[
            'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually


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


def submit_transcription_job() -> TranscriptionResponse:
    """
        Submit the transcription task files list and get the transcription result
        the transcription api supports most of the common audio formats
        you can check supported formats and other parameters here: https://help.aliyun.com/document_detail/2712535.html
        transcription api supports 100 files at most in one job, and each file size should be less than 2GB
    """
    #

    # Submit the transcription task

    task_response = dashscope.audio.asr.Transcription.async_call(
        model='sensevoice-v1',
        language_hints=['en'],
        file_urls=[
            'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_example_1.wav',
            'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/long_audio_demo_en.aac'
        ])
    # This is the description of 'file_urls'.
    # You need to provide a URL from which the file can be downloaded via HTTP.
    # Typically, we can **store these files in public cloud storage services (such as Alibaba Cloud OSS)**
    # and share a publicly accessible link.
    # Note that it is best to add an expiration time to these links,
    # to prevent third-party access if the file address is leaked.

    print('task_id: ', task_response.output.task_id)

    transcription_response = dashscope.audio.asr.Transcription.wait(
        task=task_response.output.task_id)

    if transcription_response.status_code == HTTPStatus.OK:
        for transcription in transcription_response.output['results']:
            if transcription['subtask_status'] == 'SUCCEEDED':
                url = transcription['transcription_url']
                result = json.loads(request.urlopen(url).read().decode('utf8'))
                print(
                    json.dumps(parse_sensevoice_result(result,
                                                       keep_trans=False,
                                                       keep_emotions=False),
                               indent=4,
                               ensure_ascii=False))
            else:
                print('transcription failed!')
                print(transcription)
        print('transcription done!')
    else:
        print('Error: ', transcription_response.output.message)


# run the transcription script
if __name__ == '__main__':
    init_dashscope_api_key()
    submit_transcription_job()
