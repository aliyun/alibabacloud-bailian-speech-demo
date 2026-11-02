import os
import base64
import signal
import sys
import threading
import time
import pyaudio
from dashscope import Client

from B64PCMPlayer import B64PCMPlayer

voice = 'Chelsie'
model = 'qwen3.5-omni-flash-realtime'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

pya = None
mic_stream = None
b64_player = None
session = None
session_closed_event = threading.Event()

DO_VIDEO_TEST = False

if DO_VIDEO_TEST:
    fake_video = None
    with open(os.path.join(BASE_DIR, 'data', 'cat_480p.jpg'), 'rb') as image_file:
        fake_video = base64.b64encode(image_file.read()).decode('ascii')

def init_dashscope_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        return '<your-dashscope-api-key>'  # set API-key manually


def handle_events():
    """Background thread: read realtime events and dispatch them."""
    global session
    global b64_player
    try:
        for event in session.events():
            event_type = event.get('type', '')
            if 'session.created' == event_type:
                print('start session: {}'.format(event['session']['id']))
            if 'conversation.item.input_audio_transcription.completed' == event_type:
                print('question: {}'.format(event['transcript']))
            if 'response.audio_transcript.delta' == event_type:
                text = event['delta']
                print("got llm response delta: {}".format(text))
            if 'response.audio.delta' == event_type:
                recv_audio_b64 = event['delta']
                b64_player.add_data(recv_audio_b64)
            if 'input_audio_buffer.speech_started' == event_type:
                print('======VAD Speech Start======')
                b64_player.cancel_playing()
            if 'response.done' == event_type:
                print('======RESPONSE DONE======')
                print('[Metric] response: {}, first text delay: {}, first audio delay: {}'.format(
                                session.last_response_id,
                                session.last_first_text_delay,
                                session.last_first_audio_delay,
                                ))
    except Exception as e:
        print('[Error] {}'.format(e))
    finally:
        session_closed_event.set()


if __name__  == '__main__':
    api_key = init_dashscope_api_key()

    print('Initializing ...')

    record_pcm_file = open(os.path.join(BASE_DIR, 'data', 'record_16khz.pcm'), 'wb')

    with Client(api_key=api_key) as client:
        with client.audio.realtime.connect(
            model=model,
        ) as session:
            session.update_session(
                output_modalities=["audio", "text"],
                voice=voice,
                input_audio_config={"type": "pcm", "sample_rate": 16000},
                output_audio_config={"type": "pcm", "sample_rate": 24000},
                enable_input_audio_transcription=True,
                input_audio_transcription_model='gummy-realtime-v1',
                enable_turn_detection=True,
                turn_detection_type='server_vad',
            )

            print('connection opened, init microphone')
            pya = pyaudio.PyAudio()
            mic_stream = pya.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=16000,
                            input=True)
            b64_player = B64PCMPlayer(pya)

            # start event dispatch thread
            event_thread = threading.Thread(target=handle_events, daemon=True)
            event_thread.start()

            def signal_handler(sig, frame):
                print('Ctrl+C pressed, stop recognition ...')
                # Stop recognition
                session.end_session()
                b64_player.shutdown()
                print('omni realtime stopped.')
                # Forcefully exit the program
                sys.exit(0)

            signal.signal(signal.SIGINT, signal_handler)
            print("Press 'Ctrl+C' to stop conversation...")

            #模拟多轮交互，在server_vad模式下，服务会自动处理打断，用户可以持续发送静音
            last_photo_time = time.time()*1000
            try:
                while True:
                    if session_closed_event.is_set():
                        break
                    if mic_stream:
                        audio_data = mic_stream.read(3200, exception_on_overflow=False)
                        record_pcm_file.write(audio_data)
                        session.append_audio(audio_data)
                        if DO_VIDEO_TEST and time.time()*1000 - last_photo_time > 500:
                            # 每500ms发送一张图片
                            session.append_video(fake_video)
                            last_photo_time = time.time()*1000
                    else:
                        break
            finally:
                record_pcm_file.close()
                mic_stream.close()
                pya.terminate()
