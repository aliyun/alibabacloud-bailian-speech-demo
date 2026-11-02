#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
# MIT License  (https://opensource.org/licenses/MIT)
import json
import os
import sys
import time

from dashscope import Client

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../../utils/python'))

from RealtimeMp3Player import RealtimeMp3Player

# This sample code demonstrates how to decode MP3 audio into PCM format and play it using subprocess and pyaudio.
# Decoding MP3 to PCM before playback is a common approach to audio data handling.
# Alternatively, other libraries can be utilized either to decode MP3 or to play the audio directly.

def get_api_key():
    """
    Set your DashScope API key. More information: https://help.aliyun.com/document_detail/2712195.html
    """
    if 'DASHSCOPE_API_KEY' in os.environ:
        # in fact,if you have set DASHSCOPE_API_KEY in your environment variable,
        # you can ignore this, and the sdk will automatically get the api_key from the environment variable
        return os.environ['DASHSCOPE_API_KEY']
    else:
        # if you can not set api_key in your environment variable,
        # you can set it here by code
        return '<your-dashscope-api-key>'

player = RealtimeMp3Player()
# start player
player.start()

model = 'qwen-audio-3.0-tts-flash'
voice_narrator = 'longanfengyue'
voice_motherDuck = 'longanfengyue'
voice_babyDuck = 'longanfengyue'

# Please replace the path with your audio file path
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'story.json')
print('Input file_path is: %s' % file_path)

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

story = data['story']

with Client(api_key=get_api_key()) as client:
    for item in story:
        print(item)
        if item['role'] == 'narrator':
            voice_name = voice_narrator
        elif item['role'] == 'motherDuck':
            voice_name = voice_motherDuck
        elif item['role'] == 'babyDuck':
            voice_name = voice_babyDuck
        else:
            voice_name = voice_narrator

        time.sleep(1)
        # Synthesize speech with given text, sync call and return the audio data in result
        # you can customize the synthesis parameters, like model, format, sample_rate or other parameters
        # for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
        audio = client.audio.tts.synthesize(
            item['text'],
            model=model,
            voice=voice_name,
            format='mp3',
            sample_rate=22050)
        player.write(audio)
# stop realtime mp3 player
player.stop()
