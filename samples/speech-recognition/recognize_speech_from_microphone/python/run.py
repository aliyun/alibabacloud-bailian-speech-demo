# coding=utf-8
#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import sys
import time

import dashscope
from dashscope.audio.asr import (Recognition, RecognitionCallback,
                                 RecognitionResult)

import sounddevice as sd  # for audio recording
import signal  # for keyboard events handling (press "Ctrl+C" to terminate recording and recognition)

# Set recording parameters
sample_rate = 16000  # sampling rate (Hz)
channels = 1  # mono channel
dtype = 'int16'  # data type
format_pcm = 'pcm'  # the format of the audio data
block_size = 3200  # number of frames per buffer


def init_dashscope_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ['DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually


# Audio recording callback
def audio_callback(indata, frames, time, status):
    # Send audio data to the recognition service
    if status:
        print(status)
    # Convert the recording data to bytes and send it to the recognition service
    buffer = indata.tobytes()
    recognition.send_audio_frame(buffer)


# Real-time speech recognition callback
class MyRecognitionCallback(RecognitionCallback):
    def on_open(self) -> None:

        # Start the recording stream when recognition starts
        global stream  # global variable 'stream', used to recording audio
        stream = sd.InputStream(samplerate=sample_rate,
                                channels=channels,
                                dtype=dtype,
                                blocksize=block_size,
                                callback=audio_callback)
        stream.start()
        print('Recognition initialized.')  # Recognition initialized

    def on_complete(self) -> None:
        print('Recognition completed.')  # recognition completed

    def on_error(self, result: RecognitionResult) -> None:
        print('RecognitionCallback task_id: ', result.request_id)
        print('RecognitionCallback error: ', result.message)
        # Stop and close the audio stream if it is running
        if 'stream' in globals() and stream.active:
            stream.stop()
            stream.close()
        # Forcefully exit the program
        sys.exit(1)

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if 'text' in sentence:
            print('RecognitionCallback text: ', sentence['text'])
            if RecognitionResult.is_sentence_end(sentence):
                print(
                    'RecognitionCallback sentence end, request_id:%s, usage:%s'
                    % (result.get_request_id(), result.get_usage(sentence)))

    def on_close(self) -> None:
        print('Recognition closed.')


def signal_handler(sig, frame):
    print("Ctrl+C pressed, stop recognition ...")
    # Stop recording
    if 'stream' in globals():
        stream.stop()
        stream.close()
    # Stop recognition
    recognition.stop()
    print('Recognition stopped.')
    # Forcefully exit the program
    sys.exit(0)


# main function
if __name__ == '__main__':
    init_dashscope_api_key()
    print('Initializing ...')

    # Create the recognition callback
    callback = MyRecognitionCallback()

    # Call recognition service by async mode, you can customize the recognition parameters, like model, format,
    # sample_rate For more information, please refer to https://help.aliyun.com/document_detail/2712536.html
    recognition = Recognition(
        model='paraformer-realtime-v2',
        # 'paraformer-realtime-v1'、'paraformer-realtime-8k-v1'
        format=format_pcm,
        # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
        sample_rate=sample_rate,
        # support 8000, 16000
        callback=callback)

    # Start recognition
    recognition.start()
    print('Recognition started.')

    signal.signal(signal.SIGINT, signal_handler)
    print("Press 'Ctrl+C' to stop recording and recognition...")
    # Create a keyboard listener until "Ctrl+C" is pressed
    while True:
        time.sleep(0.1)
