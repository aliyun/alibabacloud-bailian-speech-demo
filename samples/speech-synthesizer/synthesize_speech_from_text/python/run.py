#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os

from dashscope import Client

text_to_synthesize = '想不到时间过得这么快！昨天和你视频聊天，看到你那自豪又满意的笑容，我的心里呀，就如同喝了一瓶蜜一样甜呢！真心为你开心呢！'
file_to_save = 'result.mp3'


def get_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        return '<your-dashscope-api-key>'  # set API-key manually


def synthesize_speech_from_text(text, file_path):
    '''
    Synthesize speech with given text, sync call and save the audio data into file_path
    For more information, please refer to https://help.aliyun.com/document_detail/2712523.html
    '''
    with Client(api_key=get_api_key()) as client:
        with client.audio.tts.connect(
                model='cosyvoice-v3-flash',
                voice='longanhuan',
                format='mp3') as session:
            session.send_text(text)
            session.stop()
            audio = b''.join(session.audio_chunks())
            request_id = session.session.request_id
            first_package_delay = session.first_package_delay

    # Save the synthesized audio to a file
    with open(file_path, 'wb') as f:
        f.write(audio)
    print(f'Synthesized text {text} to file : {file_path}')
    print('[Metric] requestId: {}, first package delay ms: {}'.format(
        request_id, first_package_delay))


# main function
if __name__ == '__main__':
    synthesize_speech_from_text(text=text_to_synthesize,
                                file_path=file_to_save)
