# coding=utf-8
#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import sys
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer

text_to_synthesize = '想不到时间过得这么快！昨天和你视频聊天，看到你那自豪又满意的笑容，我的心里呀，就如同喝了一瓶蜜一样甜呢！真心为你开心呢！'
file_to_save = 'result.mp3'

def init_dashscope_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ['DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually


def synthesize_speech_from_text(text, file_path):
    '''
    Synthesize speech with given text, sync call and save the audio data into file_path
    For more information, please refer to https://help.aliyun.com/document_detail/2712523.html
    '''
    # Initialize the speech synthesizer
    # you can customize the synthesis parameters, like voice, format, sample_rate or other parameters
    speech_synthesizer = SpeechSynthesizer(
        model='cosyvoice-v1',
        voice='loongstella',
        callback=None)
    audio = speech_synthesizer.call(text)
    print('requestId: ', speech_synthesizer.get_last_request_id())
    # Save the synthesized audio to a file
    with open(file_path, 'wb') as f:
        f.write(audio)
    first_package_delay = speech_synthesizer._first_package_timestamp - speech_synthesizer._start_stream_timestamp
    print(f'Synthesized text {text} to file : {file_path}')
    print(f'first package delay: {first_package_delay} ms')
    


# main function
if __name__ == '__main__':
    init_dashscope_api_key()
    synthesize_speech_from_text(text=text_to_synthesize,
                              file_path=file_to_save)