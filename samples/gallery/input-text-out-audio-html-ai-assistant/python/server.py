#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
# MIT License  (https://opensource.org/licenses/MIT)
import asyncio
import json
import os
import threading
from contextlib import closing

import websockets
from dashscope import Client

#This Python code demonstrates how to use the DashScope API to perform streaming text-to-speech (TTS)
# synthesis of large language model (LLM) responses and dynamically transmit the synthesized audio
# data via a WebSocket connection.

def get_api_key():
    """
    Set your DashScope API key. More information: https://help.aliyun.com/document_detail/2712195.html
    """
    if 'DASHSCOPE_API_KEY' in os.environ:
        # in fact,if you have set DASHSCOPE_API_KEY in your environment variable,
        # you can ignore this, and the sdk will automatically get the api_key from the environment variable
        return os.environ['DASHSCOPE_API_KEY']
    else:
        # if you can not set api_key in your environment variable,
        # you can set it here by code
        return '<your-dashscope-api-key>'

messages = []


def run_pipeline(query, websocket, loop):
    """Run LLM + TTS in a worker thread and forward text/audio to the client."""
    with Client(api_key=get_api_key()) as client:
        with client.audio.tts.connect(
                model='cosyvoice-v3-flash',
                voice='longanhuan',
                format='pcm',
                sample_rate=22050) as session:

            def read_audio():
                for chunk in session.audio_chunks():
                    # send data to websocket
                    print('on_data recv speech synthesis data {}'.format(
                        len(chunk)))
                    loop.call_soon_threadsafe(asyncio.create_task,
                                              websocket.send(chunk))

            reader_thread = threading.Thread(target=read_audio)
            reader_thread.start()

            try:
                # only save the recent 5 rounds messages
                local_history = messages[-10:] + [{'role': 'user',
                                                   'content': query}]
                with closing(client.chat.completions.create(
                        model='qwen-plus',
                        messages=local_history,
                        stream=True,
                        parameters={
                            'incremental_output': True
                        })) as stream:
                    assistant_response = ''
                    for text_chunk in stream.text_stream:
                        assistant_response += text_chunk
                        print(text_chunk, end='')
                        # send llm text chunk to websocket & synthesizer
                        loop.call_soon_threadsafe(asyncio.create_task,
                                                  websocket.send(text_chunk))
                        session.send_text(text_chunk)
            finally:
                session.stop()
                reader_thread.join()

    return assistant_response


async def LlmTask(query, websocket):
    loop = asyncio.get_event_loop()
    global messages
    assistant_response = await loop.run_in_executor(
        None, run_pipeline, query, websocket, loop)
    # save history messages
    messages.append({'role': 'user', 'content': query})
    messages.append({'role': 'assistant', 'content': assistant_response})
    # only keep recent 5 rounds (10 messages)
    messages = messages[-10:]


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
