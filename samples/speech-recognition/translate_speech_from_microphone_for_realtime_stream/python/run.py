# For prerequisites running the following sample, visit https://help.aliyun.com/zh/model-studio/getting-started/first-api-call-to-qwen

import os
import signal  # for keyboard events handling (press "Ctrl+C" to terminate recording and translation)
import sys
import threading

import pyaudio
from dashscope import Client

mic = None
stream = None
target_language = 'en'
running = True


def get_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']
    return '<your-dashscope-api-key>'


def signal_handler(sig, frame):
    global running
    print('Ctrl+C pressed, stop translation ...')
    running = False


def receive_events(session):
    """Consume realtime translation events and print them."""
    try:
        for event in session.events():
            kind = event.get('type')
            if kind == 'response.text.delta':
                print(event.get('delta', ''), end='', flush=True)
            elif kind == 'response.text.done':
                print('\n[translation done] ', event.get('text', ''))
            elif kind == 'response.audio_transcript.delta':
                print('transcription stash: {}'.format(event.get('delta', '')))
            elif kind == 'conversation.item.input_audio_transcription.completed':
                print('\n[transcript completed] ', event.get('transcript', ''))
            elif kind == 'response.done':
                print('request id: ', event.get('response', {}).get('id'))
                print('usage: ', event.get('response', {}).get('usage'))
    except Exception as e:
        print('receive error: {}'.format(e))


# main function
if __name__ == '__main__':
    api_key = get_api_key()
    print('Initializing ...')

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
        print("Press 'Ctrl+C' to stop recording and translation...")

        try:
            while running:
                data = stream.read(3200, exception_on_overflow=False)
                session.append_audio(data)
        finally:
            session.close()
            receiver.join(timeout=30)

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
