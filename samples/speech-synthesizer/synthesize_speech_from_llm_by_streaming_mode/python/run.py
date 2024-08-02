# coding=utf-8
#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import sys
from http import HTTPStatus

import dashscope
from dashscope import Generation
from dashscope.audio.tts_v2 import *

# add parent directory for utils to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
sys.path.append(parent_dir)

from samples.utils.python.RealtimeMp3Player import RealtimeMp3Player

query_to_llm = '番茄炒鸡蛋怎么做？'

def init_dashscope_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ['DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually


def synthesize_speech_from_llm_by_streaming_mode(query_text: str):
    '''
    Synthesize speech with llm streaming output text, sync call and playback of MP3 audio streams.
    you can customize the synthesis parameters, like model, format, sample_rate or other parameters
    for more information, please refer to https://help.aliyun.com/document_detail/2712523.html

    '''
    player = RealtimeMp3Player()
    # start player
    player.start()
    
    # Define a callback to handle the result

    class Callback(ResultCallback):
        def on_open(self):
            print('websocket is open.')

        def on_complete(self):
            print('speech synthesis task complete successfully.')

        def on_error(self, message: str):
            print(f'speech synthesis task failed, {message}')

        def on_close(self):
            print('websocket is closed.')

        def on_event(self, message):
            # print(f'recv speech synthsis message {message}')
            pass

        def on_data(self, data: bytes) -> None:
            # save audio to file
            player.write(data)

    # Call the speech synthesizer callback
    synthesizer_callback = Callback()

    synthesizer = SpeechSynthesizer(
        model='cosyvoice-v1',
        voice='longxiaochun',
        callback=synthesizer_callback,
    )

    # Prepare for the LLM call
    messages = [{'role': 'user', 'content': query_text}]
    responses = Generation.call(
        model='qwen-turbo',
        messages=messages,
        result_format='message',  # set result format as 'message'
        stream=True,  # enable stream output
        incremental_output=True,  # enable incremental output
    )
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            print(response.output.choices[0]['message']['content'], end='')
            # send llm result to synthesizer
            synthesizer.streaming_call(
                response.output.choices[0]['message']['content'])
        else:
            print(
                'Request id: %s, Status code: %s, error code: %s, error message: %s'
                % (
                    response.request_id,
                    response.status_code,
                    response.code,
                    response.message,
                ))
    synthesizer.streaming_complete()
    print('requestId: ', synthesizer.get_last_request_id())
    # stop realtime mp3 player
    player.stop()


# main function
if __name__ == '__main__':
    init_dashscope_api_key()
    synthesize_speech_from_llm_by_streaming_mode(query_text=query_to_llm)