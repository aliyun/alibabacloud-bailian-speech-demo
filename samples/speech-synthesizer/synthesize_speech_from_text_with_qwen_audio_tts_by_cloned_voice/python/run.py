#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import sys
import threading
import time

from dashscope import Client

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


def get_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        return '<your-dashscope-api-key>'  # set API-key manually


def wait_voice_ready(client, voice_id, timeout=300.0):
    deadline = time.monotonic() + timeout
    previous_status = None
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError('Voice is not ready before timeout')
        voice = client.audio.voices.get(voice_id, timeout=min(30.0, remaining))
        if voice.status != previous_status:
            print(f'Voice status: {voice.status}', flush=True)
            previous_status = voice.status
        if voice.status == 'OK':
            return
        if voice.status != 'DEPLOYING':
            raise RuntimeError(
                f'Voice is unavailable or has unsupported status: {voice.status}')
        time.sleep(min(2.0, max(0, deadline - time.monotonic())))


def create_clone_voice(client,
                       audio_url: str,
                       prefix: str = PREFIX,
                       model: str = MODEL):
    '''
    Clone a new voice with the given audio, and return the new voice id.
    '''
    print('start cloning your voice...')
    voice = client.audio.voices.create(target_model=model,
                                       prefix=prefix,
                                       url=audio_url)
    new_voice_id = voice.voice_id
    print('requestId: ', voice.request_id)
    print('voice clone done.')
    print('your new voice is: {}'.format(new_voice_id))

    print('waiting for the cloned voice to be ready...')
    wait_voice_ready(client, new_voice_id)

    voices_list = client.audio.voices.list(
        prefix=prefix,
        page_index=0,
        page_size=10,
    )
    print('your current voices list:')
    for voice in voices_list.voices:
        print(voice)
    return new_voice_id


def delete_voice_by_prefix(client, prefix: str = PREFIX):
    '''
    Delete the voices filtered by prefix, to avoid occupying your voice quota.
    '''
    voices_list = client.audio.voices.list(
        prefix=prefix,
        page_index=0,
        page_size=10,
    )
    for voice in voices_list.voices:
        voice_id = voice['voice_id']
        client.audio.voices.delete(voice_id)
        print(f'voice {voice} deleted')


def synthesis_text_to_speech_and_play(client,
                                      text: str,
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

    complete_event = threading.Event()

    with open(output_file, 'wb') as audio_file:
        with client.audio.tts.connect(
                model=model,
                voice=voice,
                format='mp3',
                parameters={"word_timestamp_enabled": True}) as session:

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
    ## we presume you have already recorded audio and get the downloadable url.
    ## the url must be accessible from the public network.
    if len(sys.argv) < 2:
        audio_url = 'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/cosyvoice/210024_happy.wav'
    else:
        audio_url = sys.argv[1]

    with Client(api_key=get_api_key()) as client:
        # you can either synthesize text with a new cloned voice
        your_cloned_voice = create_clone_voice(client, audio_url)
        ## or use the voice id which has been created before
        # your_cloned_voice = 'qwen-audio-demo-xxxxxx'
        synthesis_text_to_speech_and_play(client,
                                          text=text_to_synthesize,
                                          voice=your_cloned_voice)

    ## you can delete the voices filtered by prefix
    # delete_voice_by_prefix(client, PREFIX)
