# coding=utf-8
#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import sys
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer

# add parent directory for utils to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
sys.path.append(parent_dir)

from samples.utils.python.RealtimeMp3Player import RealtimeMp3Player

text_to_synthesize = '欢迎体验阿里云百炼大模型语音合成服务！'
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
        voice='longxiaochun',
        callback=None)
    audio = speech_synthesizer.call(text)
    print('requestId: ', speech_synthesizer.get_last_request_id())
    # Save the synthesized audio to a file
    with open(file_path, 'wb') as f:
        f.write(audio)
    print('Synthesized text %s to file : %s' % (text, file_path))
    
    # play audio
    player = RealtimeMp3Player()
    # start player
    player.start()
    player.write(audio)
    player.stop()


# main function
if __name__ == '__main__':
    init_dashscope_api_key()
    synthesize_speech_from_text(text=text_to_synthesize,
                              file_path=file_to_save)