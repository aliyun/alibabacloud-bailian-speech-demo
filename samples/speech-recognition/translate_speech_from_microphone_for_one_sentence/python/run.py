# For prerequisites running the following sample, visit https://help.aliyun.com/zh/model-studio/getting-started/first-api-call-to-qwen

import os
import signal
import sys
import threading
from datetime import datetime

import pyaudio
from dashscope import Client


def get_timestamp():
    """return timestamp in milliseconds"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def get_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']
    return '<your-dashscope-api-key>'


mic = None
stream = None
target_language = 'en'
running = True
sentence_finished = threading.Event()


def signal_handler(sig, frame):
    global running
    print('\t[log] Ctrl+C pressed, stop translation ...')
    running = False


def receive_events(session):
    """Consume translation events until the first sentence finishes."""
    try:
        for event in session.events():
            kind = event.get('type')
            if kind == 'response.text.delta':
                print('[{}] translate to {}: {}'.format(
                    get_timestamp(), target_language, event.get('delta', '')),
                    end='',
                    flush=True)
            elif kind == 'response.text.done':
                print('\n[{}] translation done: {}'.format(
                    get_timestamp(), event.get('text', '')))
                sentence_finished.set()
            elif kind == 'conversation.item.input_audio_transcription.completed':
                print('\n[{}] transcript : {}'.format(
                    get_timestamp(), event.get('transcript', '')))
            elif kind == 'response.done':
                sentence_finished.set()
    except Exception as e:
        print('\t[log] receive error: {}'.format(e))


# main function
if __name__ == '__main__':
    api_key = get_api_key()
    print('\t[log] Initializing ...')

    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=16000,
                      input=True)

    client = Client(api_key=api_key)
    try:
        session = client.audio.realtime.connect(
            model='qwen3.8-livetranslate-flash-realtime',
        )
        session.connect()
        session.update_session(
            output_modalities=["text"],
            translation_params={"language": target_language},
        )

        receiver = threading.Thread(target=receive_events, args=(session,))
        receiver.start()

        signal.signal(signal.SIGINT, signal_handler)
        print('\t[log] Translation started')
        print('translation will stop after recording one sentence...')

        audio_buffer = []
        try:
            while running and not sentence_finished.is_set():
                data = stream.read(3200, exception_on_overflow=False)
                audio_buffer.append(data)
                session.append_audio(data)
        finally:
            session.close()
            receiver.join(timeout=30)

        if audio_buffer:
            filename = '{}_record.pcm'.format(
                session.session_id or 'unknown')
            with open(filename, 'wb') as f:
                for audio in audio_buffer:
                    f.write(audio)
            print('\t[log] Recorded audio saved to {}'.format(filename))

        print(
            '[Metric] requestId: {}, first text delay ms: {}'.format(
                session.last_response_id,
                session.last_first_text_delay,
            ))
    finally:
        if stream is not None:
            try:
                stream.stop_stream()
                stream.close()
            except Exception:
                pass
        if mic is not None:
            try:
                mic.terminate()
            except Exception:
                pass
        client.close()
