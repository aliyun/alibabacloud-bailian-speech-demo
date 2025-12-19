#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
# MIT License  (https://opensource.org/licenses/MIT)
import asyncio
import json
import os
import queue
from http import HTTPStatus

import dashscope
import websockets
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

# Define a callback to handle the result


class WSCallback(ResultCallback):
    def __init__(self, websocket, loop: asyncio.AbstractEventLoop):
        self.websocket = websocket
        self.loop = loop
        self.completed = queue.Queue()

    def on_open(self):
        print('websocket is open.')

    def on_complete(self):
        print('speech synthesis task complete successfully.')
        self.completed.put(True)

    def on_error(self, message: str):
        print(f'speech synthesis task failed, {message}')
        self.completed.put(False)

    def on_close(self):
        print('websocket is closed.')

    def on_event(self, message):
        pass
        # print(f'recv speech synthsis message {message}')

    def on_data(self, data: bytes) -> None:
        # send data to websocket
        print('on_data recv speech synthsis data {}'.format(len(data)))
        self.loop.call_soon_threadsafe(asyncio.create_task,
                                       self.websocket.send(data))
        print('on_data done')


messages = []


async def LlmTask(query, websocket):
    global messages
    loop = asyncio.get_event_loop()
    # Call the speech synthesizer callback
    synthesizer_callback = WSCallback(websocket=websocket, loop=loop)

    # Synthesize speech with llm streaming output text, sync call and playback of MP3 audio streams.
    # you can customize the synthesis parameters, like model, format, sample_rate or other parameters
    # for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
    synthesizer = SpeechSynthesizer(
        model='cosyvoice-v3-flash',
        voice='longanhuan',
        format=AudioFormat.PCM_22050HZ_MONO_16BIT,
        callback=synthesizer_callback,
    )

    # Prepare for the LLM call
    messages.append({'role': 'user', 'content': query})
    # only save the recent 5 rounds messages
    messages = messages[-10:]
    responses = Generation.call(
        model='qwen-plus',
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
            # send llm text chunk to websocket & synthesizer
            # await (websocket.send(text_chunk))
            loop.call_soon_threadsafe(asyncio.create_task,
                                      websocket.send(text_chunk))
            synthesizer.streaming_call(text_chunk)
        else:
            print(
                'Request id: %s, Status code: %s, error code: %s, error message: %s'
                % (
                    response.request_id,
                    response.status_code,
                    response.code,
                    response.message,
                ))
        await asyncio.sleep(0.05)
    synthesizer.async_streaming_complete()
    while True:
        if not synthesizer_callback.completed.empty():
            break
        await asyncio.sleep(0.1)
    # save history messages
    messages.append({'role': 'assistant', 'content': assistant_response})


# mock a tts server
async def echo(websocket):
    async for message in websocket:
        print('recv: ' + message)
        data = json.loads(message)
        await LlmTask(data['text'], websocket=websocket)


async def main():
    port = 11111
    async with websockets.serve(echo, 'localhost', port, ping_interval=None):
        print('websocket server running at ws://127.0.0.1:{}'.format(port))
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
