#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
#  MIT License  (https://opensource.org/licenses/MIT)

import os
import multiprocessing

import dashscope
from dashscope.audio.tts_v2 import AudioFormat, SpeechSynthesizer

# Set your DashScope API key. More information: https://help.aliyun.com/document_detail/2712195.html
if 'DASHSCOPE_API_KEY' in os.environ:
    dashscope.api_key = os.environ['DASHSCOPE_API_KEY']
    # in fact,if you have set DASHSCOPE_API_KEY in your environment variable,
    # you can ignore this, and the sdk will automatically get the api_key from the environment variable
else:
    dashscope.api_key = '<your-dashscope-api-key>'
    # if you can not set api_key in your environment variable,
    # you can set it here by code


def process_synthesis(text_to_synthesize):
    pid = os.getpid()
    file_to_save = f'result_p{pid}.mp3'

    # Initialize the speech synthesizer
    # you can customize the synthesis parameters, like voice, format, sample_rate or other parameters
    speech_synthesizer = SpeechSynthesizer(
        model='cosyvoice-v1',
        voice='longxiaochun',
        callback=None)

    # Synthesize speech with given text, sync call and return the audio data in result
    # for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
    audio_data = speech_synthesizer.call(text_to_synthesize)
    print('requestId: ', speech_synthesizer.get_last_request_id())
    if audio_data is not None:
        # Save the synthesized audio to a file
        with open(file_to_save, 'wb') as f:
            f.write(audio_data)

        print('[Process {}] Synthesized text {} to file : {}'.format(pid, text_to_synthesize, file_to_save))
    else:
        print('[Process {}] Synthesis Fail'.format(pid))
    

def multi_process_pool():
    # Get the number of CPU cores avaliable
    num_cores = multiprocessing.cpu_count()
    # print(f"Number of CPU cores: {num_cores}")

    # Create a pool of processes with the number of available CPU cores
    process_pool = multiprocessing.Pool(processes=num_cores)

    # Please replace the text with your own text to synthesis
    text_list = [
        '欢迎体验阿里云百炼大模型语音合成服务！',
        '欢迎体验阿里云百炼大模型语音合成服务！',
    ]
    
    # Use the map method to distribute tasks among the pool and collect the results
    process_pool.map(process_synthesis, text_list)
    
    # Close the pool and wait for all processes to complete
    process_pool.close()
    process_pool.join()




if __name__ == '__main__':
    multi_process_pool()