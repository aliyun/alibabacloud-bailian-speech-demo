import os
import time
import base64
import pyaudio
from concurrent.futures import ThreadPoolExecutor
from dashscope import Client

from B64PCMPlayer import B64PCMPlayer

pya = None
b64_player: B64PCMPlayer = None
text_to_synthesize = [
    '这是第一句话。',
    '这是第二句话。',
    '这是第三句话。',
    '这是第四句话。',
    '这是第五句话。',
]

DO_VIDEO_TEST = False


def init_dashscope_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ[
            'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        return '<your-dashscope-api-key>'  # set API-key manually


def receive_audio(session):
    try:
        for chunk in session.audio_chunks():
            b64_player.add_data(base64.b64encode(chunk).decode('ascii'))
    except Exception as e:
        print('[Error] {}'.format(e))


if __name__ == '__main__':
    api_key = init_dashscope_api_key()

    print('Initializing ...')

    pya = pyaudio.PyAudio()
    b64_player = B64PCMPlayer(pya, save_file=True)

    try:
        with Client(api_key=api_key) as client:
            with client.audio.tts.connect(
                    model='qwen-audio-3.0-tts-flash',
                    voice='longanfengyue',
                    format='pcm',
                    sample_rate=24000) as session:
                with ThreadPoolExecutor(max_workers=1) as executor:
                    receiver = executor.submit(receive_audio, session)
                    try:
                        for text_chunk in text_to_synthesize:
                            print(f'send text: {text_chunk}')
                            session.send_text(text_chunk)
                            session.flush()
                            time.sleep(2)
                        session.stop()
                        receiver.result()
                    finally:
                        request_id = session.session.request_id
                        first_package_delay = session.first_package_delay
                        session.close()
    finally:
        b64_player.wait_for_complete()
        b64_player.shutdown()
        if pya:
            pya.terminate()
            pya = None

    print('[Metric] session: {}, first audio delay: {}'.format(
        request_id,
        first_package_delay,
    ))
