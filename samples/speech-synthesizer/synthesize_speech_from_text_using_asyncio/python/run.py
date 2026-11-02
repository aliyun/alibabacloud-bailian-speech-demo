# !/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import asyncio
import os
import queue
import threading
from datetime import datetime

from dashscope import Client

test_text_array = ['想不到时间过得这么快！昨',
                   '天和你视频聊天，看到你那',
                   '自豪又满意的笑容，我的心里',
                   '呀，就如同喝了一瓶蜜一样甜',
                   '呢！真心为你开心呢！']


class ThreadSafeAsyncioEvent(asyncio.Event):
    def set(self):
        self._loop.call_soon_threadsafe(super().set)


def get_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        return '<your-dashscope-api-key>'  # set API-key manually


def get_current_time_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')


async def synthesis_text_to_speech_using_asyncio(text_array):
    '''
    Synthesize speech with given text by streaming mode, async call and play the synthesized audio in real-time.
    for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
    '''
    complete_event = ThreadSafeAsyncioEvent()
    text_queue = queue.Queue()
    metrics = {}

    with open('result.mp3', 'wb') as audio_file:

        def run_synthesis():
            with Client(api_key=get_api_key()) as client:
                with client.audio.tts.connect(
                        model='cosyvoice-v3-flash',
                        voice='longanhuan',
                        format='mp3') as session:

                    def read_audio():
                        for chunk in session.audio_chunks():
                            audio_file.write(chunk)

                    reader_thread = threading.Thread(target=read_audio)
                    reader_thread.start()

                    try:
                        while True:
                            try:
                                text = text_queue.get(timeout=0.1)
                            except queue.Empty:
                                continue
                            if text is None:
                                break
                            session.send_text(text)

                        session.stop()
                        reader_thread.join()
                    finally:
                        metrics['request_id'] = session.session.request_id
                        metrics['first_package_delay'] = session.first_package_delay
                        session.close()

            complete_event.set()

        synthesis_thread = threading.Thread(target=run_synthesis)
        synthesis_thread.start()

        for text in text_array:
            text_queue.put(text)
            print(f'[{get_current_time_str()}] send text: {text}')
            await asyncio.sleep(0.1)
        text_queue.put(None)

        await complete_event.wait()
        synthesis_thread.join()

    print(f'[{get_current_time_str()}]' +
          '[Metric] requestId: {}, first package delay ms: {}'.format(
              metrics.get('request_id'), metrics.get('first_package_delay')))


# this task will print the current time every second.
async def print_time():
    start_time = datetime.now()
    while True:
        cur_time = datetime.now()
        print(f'[{get_current_time_str()}] other task counting down')
        if (cur_time - start_time).seconds > 10:
            break
        await asyncio.sleep(1)  # 等待1秒


async def main():
    await asyncio.gather(print_time(),
                         synthesis_text_to_speech_using_asyncio(test_text_array))


if __name__ == "__main__":
    asyncio.run(main())
