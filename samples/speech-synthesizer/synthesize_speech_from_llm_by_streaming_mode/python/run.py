#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import sys
import threading
from contextlib import closing

from dashscope import Client

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../../utils/python'))

from RealtimeMp3Player import RealtimeMp3Player

system_text = '你是一个闲聊型语音AI助手，主要任务是和用户展开日常性的友善聊天。请不要回复使用任何格式化文本，回复要求口语化，不要使用markdown格式或者列表。'
query_to_llm = '番茄炒鸡蛋怎么做？'


def get_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        return '<your-dashscope-api-key>'  # set API-key manually


def synthesize_speech_from_llm_by_streaming_mode(query_text: str):
    '''
    Synthesize speech with llm streaming output text, sync call and playback of MP3 audio streams.
    you can customize the synthesis parameters, like model, format, sample_rate or other parameters
    for more information, please refer to https://help.aliyun.com/document_detail/2712523.html

    '''
    player = RealtimeMp3Player()
    # start player
    player.start()

    complete_event = threading.Event()

    with Client(api_key=get_api_key()) as client:
        with client.audio.tts.connect(
                model='cosyvoice-v3-flash',
                voice='longanhuan',
                format='mp3') as session:

            def read_audio():
                for chunk in session.audio_chunks():
                    # send to player
                    player.write(chunk)
                complete_event.set()

            reader_thread = threading.Thread(target=read_audio)
            reader_thread.start()

            try:
                # Prepare for the LLM call
                messages = [{
                    'role': 'system',
                    'content': system_text
                }, {
                    'role': 'user',
                    'content': query_text
                }]
                print('>>> query: ' + query_text)
                with closing(client.chat.completions.create(
                        model='qwen-plus',
                        messages=messages,
                        stream=True,
                        parameters={
                            'incremental_output': True
                        })) as stream:
                    print('>>> answer: ', end='')
                    for text_chunk in stream.text_stream:
                        print(text_chunk, end='', flush=True)
                        # send llm result to synthesizer
                        session.send_text(text_chunk)
            finally:
                session.stop()
                complete_event.wait()
                reader_thread.join()

                request_id = session.session.request_id
                first_package_delay = session.first_package_delay

    # add new line after llm outputs
    print('')
    print('>>> playback completed')
    print('[Metric] requestId: {}, first package delay ms: {}'.format(
        request_id, first_package_delay))
    # stop realtime mp3 player
    player.stop()


# main function
if __name__ == '__main__':
    synthesize_speech_from_llm_by_streaming_mode(query_text=query_to_llm)
