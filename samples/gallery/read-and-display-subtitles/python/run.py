#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import sys
import threading
import time
from enum import Enum, unique
from http import HTTPStatus

import dashscope
import wx
import wx.richtext as rt
from dashscope import Generation
from dashscope.audio.tts_v2 import *
sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../../utils/python'))

from RealtimeMp3Player import RealtimeMp3Player

# This sample code demonstrates how to decode MP3 audio into PCM format and play it using subprocess and pyaudio.
# Decoding MP3 to PCM before playback is a common approach to audio data handling.
# Alternatively, other libraries can be utilized either to decode MP3 or to play the audio directly.


def init_dashscope_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ[
            'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually


class SubtitlePlayer(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(parent=None,
                         title='Real-time Subtitle Example',
                         size=(1000, 300))
        panel = wx.Panel(self)

        self.label_text = ''
        # self.label = wx.StaticText(panel, label=self.label_text, pos=(10, 10))
        self.label = rt.RichTextCtrl(panel,
                                     pos=(10, 10),
                                     size=(1380, 260),
                                     style=wx.VSCROLL | wx.HSCROLL
                                     | wx.NO_BORDER | wx.TE_READONLY
                                     | wx.TE_MULTILINE)
        font = self.label.GetFont()
        font.PointSize += 6
        self.label.SetFont(font)
        self.Show()
        self.task_lock = threading.Lock()
        self.stop_task = False
        self.queue_lock = threading.Lock()
        # [is_stop, audio]
        self.audio_queue = []
        # [is_stop, text]
        self.text_queue = []
        self.work_thread = threading.Thread(target=self.run)
        self.work_thread.start()
        self.player = RealtimeMp3Player()
        self.player.start()

    def update_label(self, new_text):
        # Remove highlight from existing text
        self.label.SetStyle(0, self.label.GetLastPosition(),
                            wx.TextAttr(wx.Colour(0, 0, 0)))

        # Add new text at the end
        self.label.SetInsertionPointEnd()
        self.label.WriteText(new_text)

        # Get the entire text
        current_text = self.label.GetValue()

        # Find the start of the last line
        last_newline = current_text.rfind(
            '\n', 0,
            self.label.GetLastPosition() - len(new_text))
        if last_newline == -1:
            start_of_last_line = 0
        else:
            start_of_last_line = last_newline + 1

        # Highlight the last line
        last_position = self.label.GetLastPosition()
        self.label.SetStyle(start_of_last_line, last_position,
                            wx.TextAttr(wx.Colour(10, 200, 10)))

        # Ensure the control scrolls to show the new text
        self.label.ShowPosition(last_position)

    def add_text_to_label(self, new_text):
        wx.CallAfter(self.update_label, new_text)

    def stop(self):
        with self.task_lock:
            self.stop_task = True
        self.work_thread.join()

    def submit_audio(self, audio):
        with self.queue_lock:
            if audio is not None:
                self.audio_queue.append([False, audio])

    def submit_text(self, text):
        with self.queue_lock:
            if text is not None:
                self.text_queue.append([False, text])

    def sentence_end(self):
        with self.queue_lock:
            self.text_queue.append([True, None])
            self.audio_queue.append([True, None])

    def wait_and_refresh_player(self):
        if self.player is not None:
            self.player.stop()
        self.player = RealtimeMp3Player()
        self.player.start()

    def run(self):
        class PlayerState(Enum):
            RUNNING = (0)
            WAITING_FOR_AUDIO_STOP = (1)
            WAITING_FOR_TEXT_STOP = (1)

            def __init__(self, code):
                self.type_code = code

        state = PlayerState.RUNNING
        while True:

            # Use separate locks
            with self.task_lock:
                stop_task = self.stop_task

            with self.queue_lock:
                audio_task = self.audio_queue[0] if self.audio_queue else None
                text_task = self.text_queue[0] if self.text_queue else None

            if audio_task is None or text_task is None:
                time.sleep(0.05)
                continue

            if stop_task and not audio_task and not text_task:
                break

            is_audio_stop, audio = audio_task
            is_text_stop, text = text_task

            if is_audio_stop and is_text_stop:
                self.add_text_to_label('\n')
                self.wait_and_refresh_player()
                with self.queue_lock:
                    self.audio_queue.pop(0)
                    self.text_queue.pop(0)
                state = PlayerState.RUNNING
                continue

            if state == PlayerState.RUNNING:
                if is_audio_stop:
                    state = PlayerState.WAITING_FOR_TEXT_STOP
                    self.add_text_to_label(text)
                    with self.queue_lock:
                        self.text_queue.pop(0)
                elif is_text_stop:
                    state == PlayerState.WAITING_FOR_AUDIO_STOP
                    self.player.write(audio)
                    with self.queue_lock:
                        self.audio_queue.pop(0)
                else:
                    self.player.write(audio)
                    self.add_text_to_label(text)
                    with self.queue_lock:
                        self.audio_queue.pop(0)
                        self.text_queue.pop(0)
            elif state == PlayerState.WAITING_FOR_AUDIO_STOP:
                if is_audio_stop:
                    print('should not reach here!')
                    sys.exit(0)
                else:
                    self.player.write(audio)
                    with self.queue_lock:
                        self.audio_queue.pop(0)
            elif state == PlayerState.WAITING_FOR_TEXT_STOP:
                if is_text_stop:
                    print('should not reach here!')
                else:
                    self.add_text_to_label(text)
                    with self.queue_lock:
                        self.text_queue.pop(0)
            else:
                print('state not support, should not reach here!')


# Define a callback to handle the result


class CallbackWithFrame(ResultCallback):
    def __init__(self, frame, audio_save) -> None:
        super().__init__()
        self.frame = frame
        self.audio_save = audio_save

    def on_open(self):
        self.audio_length = 0
        print('websocket is open.')

    def on_complete(self):
        print('speech synthesis task complete successfully.')

    def on_error(self, message: str):
        print(f'speech synthesis task failed, {message}')

    def on_close(self):
        print('websocket is closed.')

    def on_event(self, message):
        # print(f'recv speech synthsis message {message}')
        pass

    def on_data(self, data: bytes) -> None:
        # play audio realtime
        self.frame.submit_audio(data)
        self.audio_save.write(data)


# TtsTask
class TtsTask:
    # Event types in tasklist
    @unique
    class TaskType(Enum):
        SENTENCE_BEGIN = (0)
        SENTENCE_END = (1)
        TEXT = (2)

        def __init__(self, code):
            self.type_code = code

    text = ''
    type: TaskType = TaskType.TEXT

    def __init__(self, text, type):
        self.text = text
        self.type = type

    def __str__(self):
        return 'TtsTask(text=' + self.text + ', type=' + str(
            self.type.type_code) + ')'


class TtsTaskHandler:
    def __init__(self, callback: CallbackWithFrame, frame: SubtitlePlayer):
        self.task_list = []
        self.lock = threading.Lock()
        self.stop_task = False
        self.synthesizer = None
        self.work_thread = threading.Thread(target=self.run)
        self.work_thread.start()
        self.frame = frame
        self.callback = callback

    def restart_synthesizer(self):
        self.synthesizer = SpeechSynthesizer(
            model='cosyvoice-v2',
            voice='longhua_v2',
            callback=self.callback,
        )

    def run(self):
        while True:
            with self.lock:
                if self.stop_task and len(self.task_list) == 0:
                    self.frame.stop()
                    break
                if len(self.task_list) == 0:
                    time.sleep(0.01)
                    continue
                task = self.task_list.pop(0)
                if task.type == TtsTask.TaskType.TEXT:
                    print('[tts] send text: ' + task.text)
                    self.synthesizer.streaming_call(task.text)
                    self.frame.submit_text(task.text)
                    print('[tts] text submitted')
                elif task.type == TtsTask.TaskType.SENTENCE_END:
                    print('[tts] streaming complete: ' + task.text)
                    self.synthesizer.streaming_complete()
                    print('[tts] streaming completed: ' + task.text)
                    self.frame.sentence_end()
                    print('#' * 10 + 'sentence end' + '#' * 10)
                elif task.type == TtsTask.TaskType.SENTENCE_BEGIN:
                    self.restart_synthesizer()
                    print('[tts] restart synthesizer')

    def submit_task(self, task: TtsTask):
        with self.lock:
            # skip empty text
            if task.type == TtsTask.TaskType.TEXT and not task.text:
                return
            self.task_list.append(task)

    def stop(self):
        with self.lock:
            self.stop_task = True
        self.work_thread.join()


def process(frame: SubtitlePlayer, ttsTaskHandler: TtsTaskHandler):
    messages = [{'role': 'user', 'content': '请讲一个一百五十字的小故事。'}]
    responses = Generation.call(
        model='qwen-plus',
        messages=messages,
        result_format='message',  # set result format as 'message'
        stream=True,  # enable stream output
        incremental_output=True,  # enable incremental output
    )
    ttsTaskHandler.submit_task(TtsTask('', TtsTask.TaskType.SENTENCE_BEGIN))
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            text = response.output.choices[0]['message']['content']
            print('recv text from llm:' + text)
            if '。' in text:
                # split text by '。'
                parts = text.split('。', 1)
                ttsTaskHandler.submit_task(
                    TtsTask(parts[0] + '。', TtsTask.TaskType.TEXT))
                ttsTaskHandler.submit_task(
                    TtsTask('', TtsTask.TaskType.SENTENCE_END))
                ttsTaskHandler.submit_task(
                    TtsTask('', TtsTask.TaskType.SENTENCE_BEGIN))
                ttsTaskHandler.submit_task(
                    TtsTask(parts[1], TtsTask.TaskType.TEXT))
            else:
                ttsTaskHandler.submit_task(TtsTask(text,
                                                   TtsTask.TaskType.TEXT))

        else:
            print(
                'Request id: %s, Status code: %s, error code: %s, error message: %s'
                % (
                    response.request_id,
                    response.status_code,
                    response.code,
                    response.message,
                ))
    ttsTaskHandler.stop()


# Synthesize speech with llm streaming output text, sync call and playback of MP3 audio streams.
# you can customize the synthesis parameters, like model, format, sample_rate or other parameters
# for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
if __name__ == '__main__':
    init_dashscope_api_key()
    app = wx.App(False)
    frame = SubtitlePlayer()
    audio_save = open('result.mp3', 'wb')
    callback = CallbackWithFrame(frame, audio_save)
    ttsTaskHandler = TtsTaskHandler(callback, frame)
    thread = threading.Thread(target=process, args=(frame, ttsTaskHandler))
    thread.start()
    app.MainLoop()
