# For prerequisites running the following sample, visit https://help.aliyun.com/zh/model-studio/getting-started/first-api-call-to-qwen
import os
import signal  # for keyboard events handling (press "Ctrl+C" to terminate recording and translation)
import sys
import threading

import pyaudio
from dashscope import Client

# Set recording parameters
sample_rate = 16000  # sampling rate (Hz)
channels = 1  # mono channel
dtype = 'int16'  # data type
format_pcm = 'pcm'  # the format of the audio data
block_size = 3200  # number of frames per buffer

running = True
mic = None
stream = None


def get_api_key():
    """Load DashScope API key from environment or use a placeholder."""
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']
    return '<your-dashscope-api-key>'


def signal_handler(sig, frame):
    global running
    print('Ctrl+C pressed, stop translation ...')
    running = False


# main function
if __name__ == '__main__':
    api_key = get_api_key()
    print('Initializing ...')

    # Open the microphone before starting the ASR session.
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=16000,
                      input=True)

    client = Client(api_key=api_key)
    session = None
    try:
        # Call recognition service by async mode, you can customize the recognition parameters, like model, format,
        # sample_rate. For more information, please refer to https://help.aliyun.com/document_detail/2712536.html
        session = client.audio.asr.recognize(
            model='fun-asr-realtime',
            # 'paraformer-realtime-v2' is also supported by the V2 SDK
            format=format_pcm,
            # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
            sample_rate=sample_rate,
            # support 8000, 16000
        )
        session.start()

        def consume_results():
            """Print partial and final recognition results."""
            for result in session.results():
                sentence = result.get_sentence()
                if not sentence or 'text' not in sentence:
                    continue
                print('ASR text: ', sentence['text'])
                if result.is_sentence_end():
                    print(
                        'ASR sentence end, request_id:%s, usage:%s'
                        % (result.request_id, result.get_usage()))

        consumer = threading.Thread(target=consume_results)
        consumer.start()

        signal.signal(signal.SIGINT, signal_handler)
        print("Press 'Ctrl+C' to stop recording and translation...")

        try:
            while running:
                data = stream.read(block_size, exception_on_overflow=False)
                session.send_audio_frame(data)
        finally:
            # Stop recognition
            session.stop()
            consumer.join(timeout=30)

        print(
            '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
            .format(
                session.request_id,
                session.first_package_delay,
                session.last_package_delay,
            ))
    finally:
        # Clean up the audio stream and microphone
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
        if session is not None:
            session.close()
        client.close()
