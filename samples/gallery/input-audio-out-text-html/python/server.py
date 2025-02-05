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
        self.send_events = []

    def on_open(self) -> None:
        print(f'[{self.tag}] Recognition started')  # recognition open

    def on_complete(self) -> None:
        print(f'[{self.tag}] Results ==> ', self.text)
        print(f'[{self.tag}] Recognition completed')  # recognition complete

    def on_error(self, result: RecognitionResult) -> None:
        print(f'[{self.tag}] RecognitionCallback task_id: ', result.request_id)
        print(f'[{self.tag}] RecognitionCallback error: ', result.message)
        exit(0)

    async def send_asr_result(self, message: str,
                              event: asyncio.Event) -> None:
        await self.websocket.send(message)
        event.set()

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if 'text' in sentence:
            is_end = False
            if RecognitionResult.is_sentence_end(sentence):
                is_end = True
            print(sentence['text'])
            msg = {'text': sentence['text'], 'is_end': is_end}
            event = asyncio.Event()
            self.send_events.append(event)
            self.loop.call_soon_threadsafe(
                asyncio.create_task,
                self.send_asr_result(json.dumps(msg), event))

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

        outfile = open('audio.pcm', 'wb')
        try:
            print('Client connected')
            while True:
                data = await websocket.recv()
                if isinstance(data, bytes):
                    # print("Received data:", len(data))
                    recognition.send_audio_frame(data)
                    outfile.write(data)
                if isinstance(data, str):
                    print('Received message:', data)
                    if data == 'stop':
                        break
        except websockets.exceptions.ConnectionClosed:
            print('Client disconnected')
        except Exception as e:
            print(f'Error: {e}')
        recognition.stop()

        # wait until all asr results are sent
        for event in callback.send_events:
            await event.wait()

        await websocket.send('asr stopped')
        print('asr stopped')

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
