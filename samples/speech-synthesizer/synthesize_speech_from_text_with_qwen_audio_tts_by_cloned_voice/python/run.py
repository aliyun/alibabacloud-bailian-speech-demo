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
# the voice enrollment and the speech synthesis must use the same model
MODEL = 'qwen-audio-3.0-tts-flash'

# the prefix of your cloned voice name
PREFIX = 'demo'

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


def create_clone_voice(audio_url: str,
                       prefix: str = PREFIX,
                       model: str = MODEL):
    '''
    Clone a new voice with the given audio, and return the new voice id.
    '''
    voice_clone_service = VoiceEnrollmentService()
    print('start cloning your voice...')
    new_voice_id = voice_clone_service.create_voice(target_model=model,
                                                    prefix=prefix,
                                                    url=audio_url)
    print('requestId: ', voice_clone_service.get_last_request_id())
    print('voice clone done.')
    print('your new voice is: {}'.format(new_voice_id))
    voices_list = voice_clone_service.list_voices(
        prefix=prefix,
        page_index=0,
        page_size=10,
    )
    print('requestId: ', voice_clone_service.get_last_request_id())
    print('your current voices list:')
    for voice in voices_list:
        print(voice)
    return new_voice_id


def delete_voice_by_prefix(prefix: str = PREFIX):
    '''
    Delete the voices filtered by prefix, to avoid occupying your voice quota.
    '''
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
                                      voice: str,
                                      model: str = MODEL,
                                      output_file: str = 'result.mp3'):
    '''
    Synthesize speech with your cloned voice, play the synthesized audio
    in real-time and save it into output_file.
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
    ## we presume you have already recorded audio and get the downloadable url.
    ## the url must be accessible from the public network.
    if len(sys.argv) < 2:
        audio_url = 'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/cosyvoice/210024_happy.wav'
    else:
        audio_url = sys.argv[1]

    init_dashscope_api_key()

    # you can either synthesize text with a new cloned voice
    your_cloned_voice = create_clone_voice(audio_url)
    ## or use the voice id which has been created before
    # your_cloned_voice = 'qwen-audio-demo-xxxxxx'
    synthesis_text_to_speech_and_play(text=text_to_synthesize,
                                      voice=your_cloned_voice)

    ## you can delete the voices filtered by prefix
    # delete_voice_by_prefix(PREFIX)
