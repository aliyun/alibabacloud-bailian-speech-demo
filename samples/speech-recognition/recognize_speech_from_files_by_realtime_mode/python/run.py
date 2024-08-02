# coding=utf-8
#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import time
import multiprocessing

import dashscope
from dashscope.audio.asr import Recognition, RecognitionCallback, RecognitionResult


def init_dashscope_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ['DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually


# Real-time speech recognition callback
class MyRecognitionCallback(RecognitionCallback):
    def __init__(self, tag) -> None:
        super().__init__()
        self.tag = tag
        self.text = ''

    def on_open(self) -> None:
        print(f'[{self.tag}]Recognition open')  # recognition open

    def on_complete(self) -> None:
        print(f'[{self.tag}]Recognition complete')  # recognition complete

    def on_error(self, result: RecognitionResult) -> None:
        print(f'[{self.tag}]RecognitionCallback task_id: ', result.request_id)
        print(f'[{self.tag}]RecognitionCallback error: ', result.message)

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if 'text' in sentence:
            print(f'[{self.tag}]RecognitionCallback text: ', sentence['text'])
            self.text = sentence['text']
            if RecognitionResult.is_sentence_end(sentence):
                print(
                    f'[{self.tag}]RecognitionCallback sentence end,request_id:{result.get_request_id()}, usage:{result.get_usage(sentence)}')

    def on_close(self) -> None:
        print(f'[{self.tag}]RecognitionCallback close.')


def process_recognition(file_path):
    # Create the recognition callback
    callback = MyRecognitionCallback(f'process {os.getpid()}')
    # Initialize recognition service by sync call
    # you can customize the recognition parameters, like model, format, sample_rate
    # for more information, please refer to https://help.aliyun.com/document_detail/2712536.html
    recognition = Recognition(
        model='paraformer-realtime-v2',
        # 'paraformer-realtime-v1'、'paraformer-realtime-8k-v1'
        format='wav',
        # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
        sample_rate=16000,  # supported 8000、16000
        callback=callback)

    # Start recognition with the audio file simulate multi channel audio stream from microphone
    recognition.start()
    f = open(file_path, 'rb')
    while True:
        # 3200 bytes is 20ms audio data
        chunk = f.read(3200)
        if not chunk:
            break
        else:
            recognition.send_audio_frame(chunk)
        time.sleep(0.02)
    f.close()
    recognition.stop()
    return callback.text


def multi_process_recognition():
    # Get the number of CPU cores avaliable
    num_cores = multiprocessing.cpu_count()
    # print(f"Number of CPU cores: {num_cores}")

    # Create a pool of processes with the number of available CPU cores
    process_pool = multiprocessing.Pool(processes=num_cores)

    # Please replace the path with your audio source
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_list = [
        os.path.join(current_dir, '../..', 'sampledata',
                     'hello_world_male_16k_16bit_mono.wav'),
        os.path.join(current_dir, '../..', 'sampledata',
                     'hello_world_male_16k_16bit_mono.wav'),
        os.path.join(current_dir, '../..', 'sampledata',
                     'hello_world_male_16k_16bit_mono.wav'),
    ]

    # Use the map method to distribute tasks among the pool and collect the results
    results = process_pool.map(process_recognition, file_list)

    # Close the pool and wait for all processes to complete
    process_pool.close()
    process_pool.join()

    # Print all results
    for result in results:
        print(result)


if __name__ == '__main__':
    init_dashscope_api_key()
    multi_process_recognition()
