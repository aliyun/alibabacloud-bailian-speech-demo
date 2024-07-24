#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
# MIT License  (https://opensource.org/licenses/MIT)
import os
import sys
import threading
import time
from http import HTTPStatus

import dashscope
from dashscope import Generation
from dashscope.audio.asr import (Recognition, RecognitionCallback,
                                 RecognitionResult)
import speech_synthesizer
from pcm_recorder import Recorder
from app_util import MyApp
from pcm_player import PlayerCallback

# This sample code demonstrates how to decode MP3 audio into PCM format and play it using subprocess and pyaudio.
# Decoding MP3 to PCM before playback is a common approach to audio data handling.
# Alternatively, other libraries can be utilized either to decode MP3 or to play the audio directly.

# Set your DashScope API key. More information: https://help.aliyun.com/document_detail/2712195.html
if 'DASHSCOPE_API_KEY' in os.environ:
    dashscope.api_key = os.environ['DASHSCOPE_API_KEY']
    # in fact,if you have set DASHSCOPE_API_KEY in your environment variable,
    # you can ignore this, and the sdk will automatically get the api_key from the environment variable
else:
    dashscope.api_key = '<your-dashscope-api-key>'
    # if you can not set api_key in your environment variable,
    # you can set it here by code


# recognition callback
class MyRecognitionCallback(RecognitionCallback):
    def __init__(self, callback_to_stop):
        super().__init__()
        self._player_callback = None
        self._audio_player = None
        self._callback_to_stop = callback_to_stop

    def on_open(self) -> None:
        print('Recognition open')  # recognition open

    def on_complete(self) -> None:
        print('Recognition complete')  # recognition complete

    def on_error(self, result: RecognitionResult) -> None:
        print('RecognitionCallback task_id: ', result.request_id)
        print('RecognitionCallback error: ', result.message)
        # Forcefully exit the program
        sys.exit(1)

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if 'text' in sentence:
            # print('RecognitionCallback text: ', sentence['text'])

            if RecognitionResult.is_sentence_end(sentence):
                print(
                    '\nRecognitionCallback sentence end, request_id:%s, text: %s'
                    % (result.get_request_id(), sentence['text']))
                event_to_stop.set()
                # LLM call
                if not self._audio_player:
                    self._player_callback = MyPlayerCallback()
                    self._audio_player = speech_synthesizer.SpeechSynthesisPlayer(self._player_callback)
                call_LLM(sentence['text'], self._audio_player)
            else:
                if self._audio_player:
                    print("interrupt playing tts")
                    self._audio_player.interrupt()
                    self._audio_player = None

    def on_close(self) -> None:
        print('Recognition close')


class MyPlayerCallback(PlayerCallback):
    def on_play_end(self):
        print("play end")
        app.update_text("点击按键开始交互")


class RecordToRecognize:
    def __init__(self):
        # Create the recognition callback
        self.recognition = None
        self.last_vad_status = False
        self._audio_frame_count = 0
        self._recorder = Recorder(self.audio_callback)
        self.callback = MyRecognitionCallback(self.stop_record_and_recognize)

    def call_recognition(self):
        # Initialize recognition service by async mode
        # you can customize the recognition parameters, like model, format, sample_rate
        # for more information, please refer to https://help.aliyun.com/document_detail/2712536.html
        self.recognition = Recognition(
            model='paraformer-realtime-v2',
            # 'paraformer-realtime-v1'、'paraformer-realtime-8k-v1'
            format='pcm',
            # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
            sample_rate=16000,  # supported 8000、16000
            callback=self.callback)
        # Start recognition
        self.recognition.start()

    # Audio recording callback
    def audio_callback(self, indata, frames, time, status):
        """Send audio data to the recognition service"""
        if status:
            print(status)
        # Convert the recording data to bytes and send it to the recognition service
        buffer = indata.tobytes()
        if self._recorder.is_working():
            self._audio_frame_count += 1
            sys.stdout.write("\rRecording: [{:<10}]".format('=' * self._audio_frame_count))
            sys.stdout.flush()
            self.recognition.send_audio_frame(buffer)

    def start_record_and_recognize(self):
        self.call_recognition()
        self._recorder.start()
        self._audio_frame_count = 0

    def stop_record_and_recognize(self):
        self._recorder.stop()
        self.recognition.stop()


def call_LLM(text: str, tts_player: speech_synthesizer.SpeechSynthesisPlayer):
    # Prepare for the LLM call
    messages = [{'role': 'user', 'content': text}]
    synthesizer = tts_player
    print('call llm with recognized text: ', text)
    responses = Generation.call(
        model='qwen-turbo',
        messages=messages,
        result_format='message',  # set result format as 'message'
        stream=True,  # enable stream output
        incremental_output=True,  # enable incremental output
    )

    for response in responses:
        if response.status_code == HTTPStatus.OK:
            # send llm result to synthesizer
            synthesizer.call_synthesizer(response.output.choices[0]['message']['content'])
        else:
            print(
                'Request id: %s, Status code: %s, error code: %s, error message: %s'
                % (
                    response.request_id,
                    response.status_code,
                    response.code,
                    response.message,
                ))

    synthesizer.streaming_complete()


# main function
if __name__ == '__main__':
    _recognition = RecordToRecognize()
    app = MyApp()


    def start_recognition():
        app.update_text("Listening...")
        _recognition.start_record_and_recognize()
        print("click to start asr")

        global event_to_stop
        event_to_stop = threading.Event()
        print("event_to_stop has been notified and go to stop...")
        event_to_stop.wait()
        app.update_text("Thinking...")
        _recognition.stop_record_and_recognize()
        app.update_text("Speaking...")


    # click to start record
    def on_button1_click(event):
        _recognition_thread = threading.Thread(target=start_recognition())
        _recognition_thread.start()


    app.setButtonClicks(on_button1_click)

    # start GUI loop
    app.MainLoop()
    sys.exit(0)
