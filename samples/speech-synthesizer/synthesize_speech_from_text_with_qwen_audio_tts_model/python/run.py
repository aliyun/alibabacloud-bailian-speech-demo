#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import sys
import threading

import dashscope
from dashscope.audio.tts_v2 import *

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../../utils/python'))

from RealtimeMp3Player import RealtimeMp3Player

# supported models : 'qwen-audio-3.0-tts-flash'、'qwen-audio-3.0-tts-plus'
MODEL = 'qwen-audio-3.0-tts-flash'

# choose the voice matching the language of your text
DEFAULT_VOICE = 'longanfengyue'

text_to_synthesize = '今天的天气真不错！我们一起出去玩吧！'


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


# Define a callback to handle the synthesis result
class SpeechSynthesisCallback(ResultCallback):
    def __init__(self,
                 player: RealtimeMp3Player,
                 output_file: str = 'result.mp3'):
        self.player = player
        self.output_file = output_file
        self.file = None
        self.complete_event = threading.Event()

    def on_open(self):
        self.file = open(self.output_file, 'wb')
        print('websocket is open.')

    def on_complete(self):
        print('speech synthesis task complete successfully.')
        self.complete_event.set()

    def on_error(self, message: str):
        print(f'speech synthesis task failed, {message}')
        # wake up the main thread on failure, otherwise it waits forever
        self.complete_event.set()

    def on_close(self):
        print('websocket is closed.')
        if self.file:
            self.file.close()

    def on_event(self, message):
        # print(f'recv speech synthesis message {message}')
        pass

    def on_data(self, data: bytes) -> None:
        # send to player
        self.player.write(data)
        # save audio to file
        if self.file:
            self.file.write(data)

    def wait_for_complete(self):
        self.complete_event.wait()


def synthesis_text_to_speech_and_play(text: str,
                                      voice: str = DEFAULT_VOICE,
                                      model: str = MODEL,
                                      instruction: str = None,
                                      output_file: str = 'result.mp3'):
    '''
    Synthesize speech with given text, play the synthesized audio in real-time
    and save it into output_file.
    The optional 'instruction' controls the speaking style, emotion or dialect.
    for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
    '''
    player = RealtimeMp3Player()
    # start player
    player.start()

    callback = SpeechSynthesisCallback(player, output_file)

    # Initialize the speech synthesizer
    # you can customize the synthesis parameters, like voice, format, sample_rate or other parameters
    speech_synthesizer = SpeechSynthesizer(model=model,
                                           voice=voice,
                                           instruction=instruction,
                                           callback=callback)

    speech_synthesizer.call(text)
    print('Synthesized text: {}'.format(text))
    callback.wait_for_complete()
    player.stop()
    print('[Metric] requestId: {}, first package delay ms: {}'.format(
        speech_synthesizer.get_last_request_id(),
        speech_synthesizer.get_first_package_delay()))


# main function
if __name__ == '__main__':
    init_dashscope_api_key()

    # ========================================================================
    # Example 1: Default style — synthesize plain text with the voice's native style
    # ========================================================================
    print('\n=== Example 1: Default style ===')
    synthesis_text_to_speech_and_play(
        text=text_to_synthesize,
        output_file='result_default.mp3')

    # ========================================================================
    # Example 2: Instruction — control speaking style via natural language
    # The instruction describes the desired voice persona, speed, tone, etc.
    # ========================================================================
    print('\n=== Example 2: Style instruction ===')
    instruction_style = '年轻活泼的女性声音，声音清脆甜美，语速很快，带有明显的上扬语调，适合介绍时尚产品'
    synthesis_text_to_speech_and_play(
        text=text_to_synthesize,
        instruction=instruction_style,
        output_file='result_instruction_style.mp3')

    # ========================================================================
    # Example 3: Instruction — synthesize in a specific dialect
    # ========================================================================
    print('\n=== Example 3: Dialect instruction ===')
    instruction_dialect = '请用河南话表达'
    synthesis_text_to_speech_and_play(
        text=text_to_synthesize,
        instruction=instruction_dialect,
        output_file='result_instruction_dialect.mp3')

    # ========================================================================
    # Example 4: Emotion & rich-language tags embedded in text
    # Control tags (e.g. [excited]) set emotion for following text.
    # Rich-language tags (e.g. [laughing]) insert sound effects at that position.
    # Supported tags: [sad], [excited], [angry], [serious], [whispers], [laughing],
    # [sighing], [giggles], [cough], etc. Full list in the official documentation.
    # ========================================================================
    print('\n=== Example 4: Emotion & rich-language tags ===')
    text_with_emotion = '[excited]今天的天气真不错！[laughing]我们一起出去玩吧！'
    synthesis_text_to_speech_and_play(
        text=text_with_emotion,
        output_file='result_emotion_tags.mp3')
