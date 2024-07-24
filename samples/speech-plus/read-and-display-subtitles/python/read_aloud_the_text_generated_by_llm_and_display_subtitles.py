#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
# MIT License  (https://opensource.org/licenses/MIT)
import os
import wx
import wx.richtext as rt
import time
import threading
from http import HTTPStatus
from enum import Enum, unique

import dashscope
from dashscope import Generation
from dashscope.audio.tts_v2 import *
from RealtimeMp3Player import RealtimeMp3Player

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


class SubtitlePlayer(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(parent=None, title='Real-time Subtitle Example', size=(1000, 300))
        panel = wx.Panel(self)

        self.label_text = ""
        # self.label = wx.StaticText(panel, label=self.label_text, pos=(10, 10))
        self.label = rt.RichTextCtrl(panel, pos=(10, 10), size=(1380, 260), style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.TE_READONLY|wx.TE_MULTILINE)
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
        self.label.SetStyle(0, self.label.GetLastPosition(), wx.TextAttr(wx.Colour(0, 0, 0)))

        # Add new text at the end     
        self.label.SetInsertionPointEnd()
        self.label.WriteText(new_text)
        
        # Get the entire text
        current_text = self.label.GetValue()
        
        # Find the start of the last line
        last_newline = current_text.rfind('\n', 0, self.label.GetLastPosition() - len(new_text))
        if last_newline == -1:
            start_of_last_line = 0
        else:
            start_of_last_line = last_newline + 1
        
        # Highlight the last line
        last_position = self.label.GetLastPosition()
        self.label.SetStyle(start_of_last_line, last_position, wx.TextAttr(wx.Colour(10, 200, 10)))

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
        while True:
            time.sleep(0.05)
            with self.task_lock and self.queue_lock:
                if self.stop_task and len(self.audio_queue) == 0 and len(self.text_queue) == 0:
                    break
                # 如果audio_queue不为空
                if len(self.audio_queue) > 0:
                    is_audio_stop, audio = self.audio_queue[0]
                    # 本句音频结束
                    if is_audio_stop:
                        # 将所有剩余文本上屏
                        while len(self.text_queue) > 0:
                            is_text_stop, text = self.text_queue.pop(0)
                            if not is_text_stop:
                                # 如果没有等到对应的text end，则不会pop
                                self.add_text_to_label(text)
                            else:
                                self.add_text_to_label("\n")
                                self.audio_queue.pop(0)

                        # 等待播放器缓存中所有音频播放结束
                        self.wait_and_refresh_player()
                    else:
                        # 将音频写入播放器
                        self.player.write(audio)
                        self.audio_queue.pop(0)
                                        
                if len(self.text_queue) > 0:
                    is_text_stop, text = self.text_queue[0]
                    # 本句文本结束
                    if is_text_stop:
                        self.add_text_to_label("\n")
                        # 将所有剩余音频写入播放器
                        while len(self.audio_queue) > 0:
                            is_audio_stop, audio = self.audio_queue.pop(0)
                            if not is_audio_stop:
                                # 如果没有等待到对应的audio end，则不会pop
                                self.player.write(audio)
                            else:
                                # 等待播放器缓存中所有音频播放结束
                                self.wait_and_refresh_player()
                                self.text_queue.pop(0)
                    else:
                        # 将文本上屏
                        self.add_text_to_label(text)
                        self.text_queue.pop(0)

# Define a callback to handle the result

class CallbackWithFrame(ResultCallback):
    def __init__(self, frame) -> None:
        super().__init__()
        self.frame = frame

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
        print(f'recv speech synthsis message {message}')

    def on_data(self, data: bytes) -> None:
        # play audio realtime
        self.frame.submit_audio(data)


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

    text = ""
    type:TaskType = TaskType.TEXT
    def __init__(self, text, type):
        self.text = text
        self.type = type
    
    def __str__(self):
        return "TtsTask(text=" + self.text + ", type=" + str(self.type.type_code) + ")"


class TtsTaskHandler:
    def __init__(self, callback:CallbackWithFrame, frame:SubtitlePlayer):
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
            model='cosyvoice-v1',
            voice='longxiaochun',
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
                    self.synthesizer.streaming_call(task.text)
                    self.frame.submit_text(task.text)
                elif task.type == TtsTask.TaskType.SENTENCE_END:
                    self.synthesizer.streaming_complete()
                    self.frame.sentence_end()
                    print('#'*10 + 'sentence end' + '#'*10)
                elif task.type == TtsTask.TaskType.SENTENCE_BEGIN:
                    self.restart_synthesizer()
    
    def submit_task(self, task:TtsTask):
        with self.lock:
            # skip empty text
            if task.type == TtsTask.TaskType.TEXT and not task.text:
                return
            self.task_list.append(task)      
            
    def stop(self):
        with self.lock:
            self.stop_task = True
        self.work_thread.join()
        

def process(frame:SubtitlePlayer, ttsTaskHandler:TtsTaskHandler):
    messages = [
        {'role': 'user', 'content': '请讲一个一百五十字的小故事。'}]
    responses = Generation.call(model="qwen-turbo",
                                messages=messages,
                                result_format='message',  # set result format as 'message'
                                stream=True,  # enable stream output
                                incremental_output=True,  # enable incremental output
                                )
    ttsTaskHandler.submit_task(TtsTask("", TtsTask.TaskType.SENTENCE_BEGIN))
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            text = response.output.choices[0]['message']['content'] 
            print('recv text from llm:'+text)
            if '。' in text:
                # split text by '。'
                parts = text.split('。', 1)
                ttsTaskHandler.submit_task(TtsTask(parts[0]+'。', TtsTask.TaskType.TEXT))
                ttsTaskHandler.submit_task(TtsTask("", TtsTask.TaskType.SENTENCE_END))
                ttsTaskHandler.submit_task(TtsTask("", TtsTask.TaskType.SENTENCE_BEGIN))
                ttsTaskHandler.submit_task(TtsTask(parts[1], TtsTask.TaskType.TEXT))
            else:
                ttsTaskHandler.submit_task(TtsTask(text, TtsTask.TaskType.TEXT))
                
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
if __name__ == "__main__": 
    app = wx.App(False)
    frame = SubtitlePlayer()
    callback = CallbackWithFrame(frame)
    ttsTaskHandler = TtsTaskHandler(callback, frame)
    thread = threading.Thread(target=process, args=(frame, ttsTaskHandler))
    thread.start()
    app.MainLoop()
        
