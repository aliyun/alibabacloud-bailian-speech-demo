import asyncio
import json
import queue
import threading

import websockets
from dashscope import Client


def get_api_key():
    """Load DashScope API key from environment or use a placeholder."""
    import os
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']
    return '<your-dashscope-api-key>'


# Real-time speech recognition callback
class AudioServer:
    def __init__(self):
        pass

    def _asr_worker(self, audio_queue, results_queue, stop_event, outfile,
                    loop):
        """Run the V2 ASR session in a worker thread."""

        with Client(api_key=get_api_key()) as client:
            session = client.audio.asr.recognize(
                model='fun-asr-realtime',
                # 'paraformer-realtime-v2' is also supported by the V2 SDK
                format='pcm',
                # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr',
                # you can check the supported formats in the document
                # otherwise, we recommend using 'opus', opus is a very efficient zip format
                sample_rate=16000,  # supported 8000、16000
            )
            session.start()

            def consume_results():
                """Push final and partial sentences back to the async handler."""
                try:
                    for result in session.results():
                        sentence = result.get_sentence()
                        if sentence and 'text' in sentence:
                            msg = {
                                'text': sentence['text'],
                                'is_end': result.is_sentence_end()
                            }
                            loop.call_soon_threadsafe(
                                results_queue.put_nowait, msg)
                finally:
                    loop.call_soon_threadsafe(results_queue.put_nowait, None)

            consumer = threading.Thread(target=consume_results)
            consumer.start()

            try:
                while not stop_event.is_set():
                    try:
                        data = audio_queue.get(timeout=0.1)
                    except queue.Empty:
                        continue
                    if data is None:
                        break
                    session.send_audio_frame(data)
                    outfile.write(data)
                session.stop()
                consumer.join(timeout=30)
            finally:
                session.close()

    async def handle_client(self, websocket):
        loop = asyncio.get_running_loop()
        audio_queue = queue.Queue()
        results_queue = asyncio.Queue()
        stop_event = threading.Event()

        outfile = open('audio.pcm', 'wb')
        asr_thread = threading.Thread(
            target=self._asr_worker,
            args=(audio_queue, results_queue, stop_event, outfile, loop),
        )
        asr_thread.start()

        try:
            print('Client connected')
            while True:
                data = await websocket.recv()
                if isinstance(data, bytes):
                    audio_queue.put(data)
                if isinstance(data, str):
                    print('Received message:', data)
                    if data == 'stop':
                        break
        except websockets.exceptions.ConnectionClosed:
            print('Client disconnected')
        except Exception as e:
            print(f'Error: {e}')
        finally:
            stop_event.set()
            audio_queue.put(None)
            outfile.close()

            # wait until all asr results are sent
            while True:
                try:
                    msg = await asyncio.wait_for(results_queue.get(),
                                                 timeout=5)
                except asyncio.TimeoutError:
                    break
                if msg is None:
                    break
                await websocket.send(json.dumps(msg))

            await websocket.send('asr stopped')
            print('asr stopped')
            asr_thread.join(timeout=5)

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
