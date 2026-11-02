#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import sys
import threading

from dashscope import Client

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../../utils/python'))

from RealtimeMp3Player import RealtimeMp3Player

# supported models : 'qwen-audio-3.1-tts-flash'、'qwen-audio-3.1-tts-plus'
MODEL = 'qwen-audio-3.1-tts-flash'

# choose the voice matching the language of your text
DEFAULT_VOICE = 'longanfengyue_v3.1'

text_to_synthesize = '今天的天气真不错！我们一起出去玩吧！'


def get_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        return '<your-dashscope-api-key>'  # set API-key manually


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

    complete_event = threading.Event()

    parameters = {"word_timestamp_enabled": True}
    if instruction is not None:
        parameters["instruction"] = instruction

    with open(output_file, 'wb') as audio_file:
        with Client(api_key=get_api_key()) as client:
            with client.audio.tts.connect(
                    model=model,
                    voice=voice,
                    format='mp3',
                    parameters=parameters) as session:

                def read_audio():
                    for chunk in session.audio_chunks():
                        # send to player
                        player.write(chunk)
                        # save audio to file
                        audio_file.write(chunk)
                    complete_event.set()

                reader_thread = threading.Thread(target=read_audio)
                reader_thread.start()

                session.send_text(text)
                session.stop()
                complete_event.wait()
                reader_thread.join()

                request_id = session.session.request_id
                first_package_delay = session.first_package_delay

    player.stop()
    print('Synthesized text: {}'.format(text))
    print('[Metric] requestId: {}, first package delay ms: {}'.format(
        request_id, first_package_delay))


# main function
if __name__ == '__main__':
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
