import logging
import os
import signal
import sys
import threading
import time

import pyaudio
from dashscope import Client

# 配置日志 - 关键改进
logger = logging.getLogger('dashscope')
logger.setLevel(logging.DEBUG)

# 创建控制台处理器并设置级别为debug
console_handler = logging.StreamHandler(sys.stdout)  # 明确指定输出到stdout
console_handler.setLevel(logging.DEBUG)

# 创建格式化器
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# 添加格式化器到处理器
console_handler.setFormatter(formatter)

# 添加处理器到logger
logger.addHandler(console_handler)

# 强制刷新日志输出
logger.propagate = False

pya = None
mic_stream = None
running = True


def get_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']
    return 'YOUR_API_KEY'


def signal_handler(sig, frame):
    global running
    print('Ctrl+C pressed, stop recognition ...')
    running = False


if __name__ == '__main__':
    api_key = get_api_key()
    print('Initializing ...')

    record_pcm_file = open('./record_16khz.pcm', 'wb')

    pya = pyaudio.PyAudio()
    mic_stream = pya.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=16000,
                          input=True)

    client = Client(api_key=api_key)
    try:
        session = client.audio.realtime.connect(
            model='qwen3-asr-flash-realtime',
        )
        session.connect()

        session.update_session(
            output_modalities=["text"],
            enable_input_audio_transcription=True,
            transcription_params={
                "language": "zh",
                "sample_rate": 16000,
                "input_audio_format": "pcm",
                "corpus_text": "这是一段中文对话",
            },
        )

        def receive_events():
            """Consume realtime events and print ASR results."""
            try:
                for event in session.events():
                    event_type = event.get('type')
                    if 'session.created' == event_type:
                        print('start session: {}'.format(
                            event.get('session', {}).get('id')))
                    elif 'conversation.item.input_audio_transcription.completed' == event_type:
                        print('final recognized text: {}'.format(
                            event.get('transcript')))
                    elif 'conversation.item.input_audio_transcription.text' == event_type:
                        print("got stash result: {}".format(event.get('stash')))
                    elif 'input_audio_buffer.speech_started' == event_type:
                        print('======Speech Start======')
                    elif 'input_audio_buffer.speech_stopped' == event_type:
                        print('======Speech Stop======')
                    elif 'response.done' == event_type:
                        print('======RESPONSE DONE======')
                        print('[Metric] response: {}, first text delay: {}'.format(
                            session.last_response_id,
                            session.last_first_text_delay,
                        ))
            except Exception as e:
                print('[Error] {}'.format(e))

        receiver = threading.Thread(target=receive_events)
        receiver.start()

        signal.signal(signal.SIGINT, signal_handler)
        print("Press 'Ctrl+C' to stop conversation...")

        try:
            while running:
                audio_data = mic_stream.read(3200, exception_on_overflow=False)
                record_pcm_file.write(audio_data)
                session.append_audio(audio_data)
        finally:
            running = False
            session.close()
            receiver.join(timeout=30)
    finally:
        try:
            mic_stream.stop_stream()
            mic_stream.close()
        except Exception:
            pass
        try:
            pya.terminate()
        except Exception:
            pass
        try:
            record_pcm_file.close()
        except Exception:
            pass
        client.close()
