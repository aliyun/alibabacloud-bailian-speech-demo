# coding=utf-8
#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import json
import time
import threading
from threading import Lock
import websockets
import asyncio
from http import HTTPStatus

import dashscope
from dashscope import Generation
from dashscope.audio.tts_v2 import *

#This Python code demonstrates how to use the DashScope API to perform streaming text-to-speech (TTS)
# synthesis of large language model (LLM) responses and dynamically transmit the synthesized audio
# data via a WebSocket connection.

# Set your DashScope API key. More information: https://help.aliyun.com/document_detail/2712195.html
if 'DASHSCOPE_API_KEY' in os.environ:
    dashscope.api_key = os.environ['DASHSCOPE_API_KEY']
    # in fact,if you have set DASHSCOPE_API_KEY in your environment variable,
    # you can ignore this, and the sdk will automatically get the api_key from the environment variable
else:
    dashscope.api_key = '<your-dashscope-api-key>'
    # if you can not set api_key in your environment variable,
    # you can set it here by code
    
class TaskQueue:
    def __init__(self):
        self.text_queue = []
        self.audio_queue = []
        self.lock = Lock()
    
    def put_text(self, text, is_last):
        with self.lock:
            self.text_queue.append([text, is_last])
    
    def put_audio(self, audio, is_last):
        with self.lock:
            self.audio_queue.append([audio, is_last])
    
    def get_cur_queue(self):
        with self.lock:
            cur_audio_queue = self.audio_queue
            cur_text_queue = self.text_queue
            self.audio_queue = []
            self.text_queue = []
        return cur_audio_queue, cur_text_queue


# Define a callback to handle the result
class Callback(ResultCallback):
    
    def __init__(self, queue:TaskQueue) -> None:
        super().__init__()
        self.queue = queue
        
    def on_open(self):
        print('websocket is open.')

    def on_complete(self):
        print('speech synthesis task complete successfully.')
        self.queue.put_audio(b'', True)

    def on_error(self, message: str):
        print(f'speech synthesis task failed, {message}')

    def on_close(self):
        print('websocket is closed.')

    def on_event(self, message):
        # print(f'recv speech synthsis message {message}')
        pass

    def on_data(self, data: bytes) -> None:
        # send audio to client
        print(f'on audio')
        self.queue.put_audio(data, False)

messages = []

def LlmTask(query, taskQueue):
    global messages

    # Prepare for the LLM call
    messages.append({'role': 'user', 'content': query})
    # only save the recent 5 rounds messages
    messages = messages[-10:]
    responses = Generation.call(
        model='qwen-turbo',
        messages=messages,
        result_format='message',  # set result format as 'message'
        stream=True,  # enable stream output
        incremental_output=True,  # enable incremental output
    )
    assistant_response = ''
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            text_chunk = response.output.choices[0]['message']['content'] 
            assistant_response += text_chunk
            print(text_chunk, end='')
            taskQueue.put_text(text_chunk, False)
            # send llm text chunk to websocket & synthesizer

        else:
            print(
                'Request id: %s, Status code: %s, error code: %s, error message: %s'
                % (
                    response.request_id,
                    response.status_code,
                    response.code,
                    response.message,
                ))
    taskQueue.put_text('', True)
    # save history messages
    messages.append({'role': 'assistant', 'content': assistant_response})


# mock a tts server
async def echo(websocket, path):
    async for message in websocket:
        print('recv: '+message)
        data = json.loads(message)    

        taskQueue = TaskQueue()
        
        llm_thread = threading.Thread(target=LlmTask, args=(data['text'], taskQueue))
        llm_thread.start()

        # Call the speech synthesizer callback
        synthesizer_callback = Callback(taskQueue)

        # Synthesize speech with llm streaming output text, sync call and playback of MP3 audio streams.
        # you can customize the synthesis parameters, like model, format, sample_rate or other parameters
        # for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
        synthesizer = SpeechSynthesizer(
            model='cosyvoice-v1',
            voice='longxiaochun',
            callback=synthesizer_callback,
        )
        
        while True:
            time.sleep(0.01)
            cur_audio_queue, cur_text_queue = taskQueue.get_cur_queue()
            task_end = False
            cur_audio = b''
            for task in cur_audio_queue:
                if task[1] == False:
                    cur_audio += task[0]
                else:
                    task_end = True
            await(websocket.send(cur_audio))
            for task in cur_text_queue:
                if task[1] == False:
                    synthesizer.streaming_call(task[0])
                    await websocket.send(task[0])
                else:
                    synthesizer.async_streaming_complete()
            if task_end:
                break

port = 11111
start_server = websockets.serve(echo, 'localhost', port, ping_interval=None)
print('websocket server running at ws://127.0.0.1:{}'.format(port))
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
