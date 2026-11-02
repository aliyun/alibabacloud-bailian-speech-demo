# !/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import asyncio
import os
import queue
import threading
import time
from contextlib import contextmanager
from datetime import datetime

from dashscope import Client

test_text_array = ['想不到时间过得这么快！昨',
                   '天和你视频聊天，看到你那',
                   '自豪又满意的笑容，我的心里',
                   '呀，就如同喝了一瓶蜜一样甜',
                   '呢！真心为你开心呢！']

SYNTHESIS_TIMEOUT_SECONDS = 60
RECEIVER_JOIN_TIMEOUT_SECONDS = 5


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


@contextmanager
def preserve_primary_error(context):
    value = context.__enter__()
    try:
        yield value
    except BaseException as error:
        try:
            context.__exit__(type(error), error, error.__traceback__)
        except BaseException:
            pass
        raise
    else:
        context.__exit__(None, None, None)


def synthesize_worker(text_queue, cancelled, file_path):
    with preserve_primary_error(Client(api_key=get_api_key())) as client:
        with preserve_primary_error(client.audio.tts.connect(
                model='cosyvoice-v3-flash',
                voice='longanhuan',
                format='mp3')) as session:
            done = threading.Event()
            errors = []

            def read_audio():
                try:
                    with open(file_path, 'wb') as audio_file:
                        for chunk in session.audio_chunks():
                            audio_file.write(chunk)
                except Exception as error:
                    errors.append(error)
                finally:
                    done.set()

            reader_thread = threading.Thread(target=read_audio, daemon=True)
            reader_thread.start()
            metrics = None
            failure = None
            try:
                while not cancelled.is_set():
                    if errors:
                        raise errors[0]
                    try:
                        text = text_queue.get(timeout=0.05)
                    except queue.Empty:
                        continue
                    if text is None:
                        session.stop()
                        break
                    session.send_text(text)

                deadline = time.monotonic() + SYNTHESIS_TIMEOUT_SECONDS
                while not cancelled.is_set() and not done.wait(0.05):
                    if time.monotonic() >= deadline:
                        raise TimeoutError('Timed out waiting for synthesis to finish')
                if errors:
                    raise errors[0]
                metrics = {
                    'request_id': session.session.request_id,
                    'first_package_delay': session.first_package_delay,
                }
            except BaseException as error:
                failure = error
            finally:
                try:
                    session.close()
                except Exception as error:
                    if failure is None:
                        failure = error
                reader_thread.join(timeout=RECEIVER_JOIN_TIMEOUT_SECONDS)
                if reader_thread.is_alive() and failure is None:
                    failure = TimeoutError(
                        'Timed out waiting for receiver thread to stop')

            if failure is not None:
                raise failure
            return metrics


async def synthesis_text_to_speech_using_asyncio(
        text_array, file_path='result.mp3'):
    '''
    Synthesize speech with given text by streaming mode, async call and play the synthesized audio in real-time.
    for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
    '''
    text_queue = queue.Queue()
    cancelled = threading.Event()
    loop = asyncio.get_running_loop()
    worker = loop.run_in_executor(
        None,
        synthesize_worker,
        text_queue,
        cancelled,
        file_path,
    )

    try:
        for text in text_array:
            if worker.done():
                await worker
            text_queue.put(text)
            print(f'[{get_current_time_str()}] send text: {text}')
            await asyncio.sleep(0.1)
        text_queue.put(None)
        metrics = await asyncio.shield(worker)
    finally:
        cancelled.set()
        text_queue.put(None)
        if not worker.done():
            await asyncio.shield(asyncio.gather(worker, return_exceptions=True))

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
