# !/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import asyncio
import os
import dashscope
from datetime import datetime
from dashscope.audio.tts_v2 import *

test_text_array = ['想不到时间过得这么快！昨',
                      '天和你视频聊天，看到你那',
                      '自豪又满意的笑容，我的心里',
                      '呀，就如同喝了一瓶蜜一样甜',
                      '呢！真心为你开心呢！']


class ThreadSafeAsyncioEvent(asyncio.Event):
    def set(self):
        self._loop.call_soon_threadsafe(super().set)

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


def get_current_time_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')

async def synthesis_text_to_speech_using_asyncio(text_array):
    '''
    Synthesize speech with given text by streaming mode, async call and play the synthesized audio in real-time.
    for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
    '''

    # Define a callback to handle the result

    class Callback(ResultCallback):
        def __init__(self, complete_event):
            self.file = open('result.mp3', 'wb')
            self.complete_event = complete_event
        
        def on_open(self):
            print(f'[{get_current_time_str()}] websocket is open.')

        def on_complete(self):
            print(f'[{get_current_time_str()}] speech synthesis task complete successfully.')
            self.complete_event.set()

        def on_error(self, message: str):
            print(f'[{get_current_time_str()}] speech synthesis task failed, {message}')

        def on_close(self):
            print(f'[{get_current_time_str()}] websocket is closed.')

        def on_event(self, message):
            # print(f'recv speech synthsis message {message}')
            pass

        def on_data(self, data: bytes) -> None:
            # save audio to file
            self.file.write(data)

    # Call the speech synthesizer callback
    complete_event = ThreadSafeAsyncioEvent()
    synthesizer_callback = Callback(complete_event)

    # Initialize the speech synthesizer
    # you can customize the synthesis parameters, like voice, format, sample_rate or other parameters
    speech_synthesizer = SpeechSynthesizer(model='cosyvoice-v1',
                                           voice='loongstella',
                                           callback=synthesizer_callback)

    for text in text_array:
        speech_synthesizer.streaming_call(text)
        print(f'[{get_current_time_str()}] send text: {text}')
        await asyncio.sleep(0.1)
    speech_synthesizer.async_streaming_complete()
    
    await complete_event.wait()
    
    print(f'[{get_current_time_str()}]' + '[Metric] requestId: {}, first package delay ms: {}'.format(
        speech_synthesizer.get_last_request_id(),
        speech_synthesizer.get_first_package_delay()))



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
    await asyncio.gather(print_time(), synthesis_text_to_speech_using_asyncio(test_text_array))

if __name__ == "__main__":
    init_dashscope_api_key()
    asyncio.run(main())