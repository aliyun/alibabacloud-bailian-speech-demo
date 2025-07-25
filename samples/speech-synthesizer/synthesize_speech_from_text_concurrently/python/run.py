#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import multiprocessing
import os

import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer


def init_dashscope_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ[
            'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually


def synthesis_one_text_to_speech(task):
    '''
    Synthesize speech with given text and voice, sync call and save the audio into file_path
    for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
    '''
    init_dashscope_api_key()
    text_to_synthesize = task[0]
    voice = task[1]
    pid = os.getpid()
    file_to_save = os.path.join(f'result_{voice}_p{pid}.mp3')

    # Initialize the speech synthesizer
    # you can customize the synthesis parameters, like voice, format, sample_rate or other parameters
    speech_synthesizer = SpeechSynthesizer(model='cosyvoice-v2',
                                           voice=voice,
                                           callback=None)

    # Synthesize speech with given text, sync call and return the audio data in result
    # for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
    audio_data = speech_synthesizer.call(text_to_synthesize)
    print('[Process {}][Metric] requestId: {}, first package delay ms: {}'.
          format(pid, speech_synthesizer.get_last_request_id(),
                 speech_synthesizer.get_first_package_delay()))
    if audio_data is not None:
        # Save the synthesized audio to a file
        with open(file_to_save, 'wb') as f:
            f.write(audio_data)

        print('[Process {}] Synthesized text {} to file : {}'.format(
            pid, text_to_synthesize, file_to_save))
    else:
        print('[Process {}] Synthesis Fail'.format(pid))


def multi_process_pool():
    # Create a pool of processes with the number of available CPU cores
    process_pool = multiprocessing.Pool(processes=3)

    # Get the number of CPU cores avaliable
    # num_cores = multiprocessing.cpu_count()
    # print(f"Number of CPU cores: {num_cores}")
    # process_pool = multiprocessing.Pool(processes=num_cores)

    # Please replace the text with your own text to synthesis
    task_list = [
        ['我是龙小淳，欢迎体验阿里云百炼语音合成大模型服务！', 'longxiaochun_v2'],
        ['我是龙婉，欢迎体验阿里云百炼语音合成大模型服务！', 'longwan_v2'],
        ['我是龙书，欢迎体验阿里云百炼语音合成大模型服务！', 'longhua_v2'],
    ]

    # Use the map method to distribute tasks among the pool and collect the results
    process_pool.map(synthesis_one_text_to_speech, task_list)
    exit(0)


if __name__ == '__main__':
    multi_process_pool()
