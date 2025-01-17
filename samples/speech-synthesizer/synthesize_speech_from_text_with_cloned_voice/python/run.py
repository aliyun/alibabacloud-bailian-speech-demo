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


def create_clone_voice(audio_url: str):
    voice_clone_service = VoiceEnrollmentService()
    print('start cloning your voice...')
    new_voice_id = voice_clone_service.create_voice(
        target_model='cosyvoice-v1', prefix='demo', url=audio_url)
    print('requestId: ', voice_clone_service.get_last_request_id())
    print('voice clone done.')
    print('your new voice is: {}'.format(new_voice_id))
    voices_list = voice_clone_service.list_voices(
        page_index=0,
        page_size=10,
    )
    print('requestId: ', voice_clone_service.get_last_request_id())
    print('your current voices list:')
    for voice in voices_list:
        print(voice)
    return new_voice_id


def delete_voice_by_prefix(prefix):
    voice_clone_service = VoiceEnrollmentService()
    voices_list = voice_clone_service.list_voices(
        prefix=prefix,
        page_index=0,
        page_size=10,
    )
    print('requestId: ', voice_clone_service.get_last_request_id())
    for voice in voices_list:
        voice_id = voice['voice_id']
        voice_clone_service.delete_voice(voice_id)
        print('requestId: ', voice_clone_service.get_last_request_id())
        print(f'voice {voice} deleted')


def synthesis_text_to_speech_and_play(text, your_voice):
    '''
    Synthesize speech with given text by streaming mode, async call and play the synthesized audio in real-time.
    for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
    '''
    player = RealtimeMp3Player()
    # start player
    player.start()

    complete_event = threading.Event()

    # Define a callback to handle the result

    class Callback(ResultCallback):
        def on_open(self):
            self.file = open('result.mp3', 'wb')
            print('websocket is open.')

        def on_complete(self):
            print('speech synthesis task complete successfully.')
            complete_event.set()

        def on_error(self, message: str):
            print(f'speech synthesis task failed, {message}')

        def on_close(self):
            print('websocket is closed.')

        def on_event(self, message):
            # print(f'recv speech synthsis message {message}')
            pass

        def on_data(self, data: bytes) -> None:
            # send to player
            player.write(data)
            # save audio to file
            self.file.write(data)

    # Call the speech synthesizer callback
    synthesizer_callback = Callback()

    # Initialize the speech synthesizer
    # you can customize the synthesis parameters, like voice, format, sample_rate or other parameters
    speech_synthesizer = SpeechSynthesizer(model='cosyvoice-v1',
                                           voice=your_voice,
                                           callback=synthesizer_callback)

    speech_synthesizer.call(text)
    print('Synthesized text: {}'.format(text))
    complete_event.wait()
    player.stop()
    print('[Metric] requestId: {}, first package delay ms: {}'.format(
        speech_synthesizer.get_last_request_id(),
        speech_synthesizer.get_first_package_delay()))


# main function
if __name__ == '__main__':
    if len(sys.argv) < 2:
        audio_url = 'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/cosyvoice/210024_happy.wav'
    else:
        audio_url = sys.argv[1]
    text_to_synthesize = '你好，欢迎使用阿里巴巴通义语音实验室的音色复刻服务～'
    ## we presume you have already recorded audio and get the downloadable url.
    ## if not, please refer to the record.py to record audio and get the url.
    init_dashscope_api_key()
    # you can ethier synthesize text with new voice
    your_cloned_voice = create_clone_voice(audio_url)
    ## or use voice id which has been created before
    # your_cloned_voice = 'cosyvoice-demo-xxxxxx'
    synthesis_text_to_speech_and_play(text_to_synthesize, your_cloned_voice)
    ## you can deleted voices filtered by prefix
    # delete_voice_by_prefix('demo')
