# !/usr/bin/env python3
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

text_to_synthesize = '想不到时间过得这么快！昨天和你视频聊天，看到你那自豪又满意的笑容，我的心里呀，就如同喝了一瓶蜜一样甜呢！真心为你开心呢！'


def get_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        return '<your-dashscope-api-key>'  # set API-key manually


def synthesis_text_to_speech_and_play_by_streaming_mode(text):
    '''
    Synthesize speech with given text by streaming mode, async call and play the synthesized audio in real-time.
    for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
    '''
    player = RealtimeMp3Player()
    # start player
    player.start()

    complete_event = threading.Event()

    with open('result.mp3', 'wb') as audio_file:
        with Client(api_key=get_api_key()) as client:
            with client.audio.tts.connect(
                    model='cosyvoice-v3-flash',
                    voice='longanhuan',
                    format='mp3') as session:

                def read_audio():
                    for chunk in session.audio_chunks():
                        # send to player
                        player.write(chunk)
                        # save audio to file
                        audio_file.write(chunk)
                    complete_event.set()

                reader_thread = threading.Thread(target=read_audio)
                reader_thread.start()

                # send the whole text at once; the server streams audio back
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
    synthesis_text_to_speech_and_play_by_streaming_mode(
        text=text_to_synthesize)
