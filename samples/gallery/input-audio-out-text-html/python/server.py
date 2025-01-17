import json
import asyncio
import websockets
import dashscope
from dashscope.audio.asr import *


# Real-time speech recognition callback
class MyRecognitionCallback(RecognitionCallback):
    def __init__(self, tag, websocket, loop) -> None:
        super().__init__()
        self.tag = tag
        self.text = ''
        self.websocket = websocket
        self.loop = loop

    def on_open(self) -> None:
        print(f'[{self.tag}] Recognition started')  # recognition open

    def on_complete(self) -> None:
        print(f'[{self.tag}] Results ==> ', self.text)
        print(f'[{self.tag}] Recognition completed')  # recognition complete

    def on_error(self, result: RecognitionResult) -> None:
        print(f'[{self.tag}] RecognitionCallback task_id: ', result.request_id)
        print(f'[{self.tag}] RecognitionCallback error: ', result.message)
        exit(0)

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if 'text' in sentence:
            is_end = False
            if RecognitionResult.is_sentence_end(sentence):
                is_end = True
            print(sentence['text'])
            msg = {'text': sentence['text'], 'is_end': is_end}
            self.loop.call_soon_threadsafe(
                asyncio.create_task, self.websocket.send(json.dumps(msg)))

    def on_close(self) -> None:
        print(f'[{self.tag}] RecognitionCallback closed')


class AudioServer:
    def __init__(self):
        pass

    async def handle_client(self, websocket):
        loop = asyncio.get_event_loop()
        callback = MyRecognitionCallback('process0', websocket, loop)
        recognition = Recognition(
            model='paraformer-realtime-v2',
            # 'paraformer-realtime-v1'、'paraformer-realtime-8k-v1'
            format='pcm',
            # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr',
            # you can check the supported formats in the document
            # otherwise, we recommend using 'opus', opus is a very efficient zip format
            sample_rate=16000,  # supported 8000、16000
            semantic_punctuation_enabled=False,
            callback=callback)

        recognition.start()
        try:
            print('Client connected')
            while True:
                data = await websocket.recv()
                if isinstance(data, bytes):
                    # print("Received data:", len(data))
                    recognition.send_audio_frame(data)
                # await asyncio.sleep(0.05)
        except websockets.exceptions.ConnectionClosed:
            print('Client disconnected')
        except Exception as e:
            print(f'Error: {e}')
        recognition.stop()

    def close(self):
        print('server is closed')


async def main():
    audio_server = AudioServer()
    async with websockets.serve(audio_server.handle_client, 'localhost', 9090):
        print('WebSocket server started on ws://localhost:9090')
        try:
            await asyncio.Future()  # run forever
        finally:
            audio_server.close()


if __name__ == '__main__':
    asyncio.run(main())
