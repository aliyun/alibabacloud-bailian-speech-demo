import os
import base64
import signal
import sys
import time
import pyaudio
import dashscope
from dashscope.audio.qwen_omni import *

from B64PCMPlayer import B64PCMPlayer

voice = 'Chelsie'

pya = None
mic_stream = None
b64_player = None
conversation = None

DO_VIDEO_TEST = False

if DO_VIDEO_TEST:
    fake_video = None
    with open('data/cat_480p.jpg', 'rb') as image_file:
        fake_video = base64.b64encode(image_file.read()).decode('ascii')

def init_dashscope_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ[
            'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually


class MyCallback(OmniRealtimeCallback):
    def on_open(self) -> None:
        global pya
        global mic_stream
        global b64_player
        print('connection opened, init microphone')
        pya = pyaudio.PyAudio()
        mic_stream = pya.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True)
        b64_player = B64PCMPlayer(pya)

    def on_close(self, close_status_code, close_msg) -> None:
        print('connection closed with code: {}, msg: {}, destroy microphone'.format(close_status_code, close_msg))
        sys.exit(0)

    def on_event(self, response: str) -> None:
        try:
            global conversation
            global b64_player
            type = response['type']
            if 'session.created' == type:
                print('start session: {}'.format(response['session']['id']))
            if 'conversation.item.input_audio_transcription.completed' == type:
                print('question: {}'.format(response['transcript']))
            if 'response.audio_transcript.delta' == type:
                text = response['delta']
                print("got llm response delta: {}".format(text))
            if 'response.audio.delta' == type:
                recv_audio_b64 = response['delta']
                b64_player.add_data(recv_audio_b64)
            if 'input_audio_buffer.speech_started' == type:
                print('======VAD Speech Start======')
                b64_player.cancel_playing()
            if 'response.done' == type:
                print('======RESPONSE DONE======')
                print('[Metric] response: {}, first text delay: {}, first audio delay: {}'.format(
                                conversation.get_last_response_id(), 
                                conversation.get_last_first_text_delay(), 
                                conversation.get_last_first_audio_delay(),
                                ))
        except Exception as e:
            print('[Error] {}'.format(e))
            return


if __name__  == '__main__':
    init_dashscope_api_key()

    print('Initializing ...')
    
    record_pcm_file = open('data/record_16khz.pcm', 'wb')

    callback = MyCallback()

    conversation = OmniRealtimeConversation(
        model='qwen-omni-turbo-realtime-latest',
        callback=callback, 
        )

    conversation.connect()

    conversation.update_session(
        output_modalities=[MultiModality.AUDIO, MultiModality.TEXT],
        voice=voice,
        input_audio_format=AudioFormat.PCM_16000HZ_MONO_16BIT,
        output_audio_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
        enable_input_audio_transcription=True,
        input_audio_transcription_model='gummy-realtime-v1',
        enable_turn_detection=True,
        turn_detection_type='server_vad',
    )

    def signal_handler(sig, frame):
        print('Ctrl+C pressed, stop recognition ...')
        # Stop recognition
        conversation.close()
        b64_player.shutdown()
        print('omni realtime stopped.')
        # Forcefully exit the program
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    print("Press 'Ctrl+C' to stop conversation...")

    #模拟多轮交互，在server_vad模式下，服务会自动处理打断，用户可以持续发送静音
    last_photo_time = time.time()*1000
    while True:
        if mic_stream:
            audio_data = mic_stream.read(3200, exception_on_overflow=False)
            record_pcm_file.write(audio_data)
            audio_b64 = base64.b64encode(audio_data).decode('ascii')
            conversation.append_audio(audio_b64)
            if DO_VIDEO_TEST and time.time()*1000 - last_photo_time > 500:
                # 每500ms发送一张图片
                conversation.append_video(fake_video)
                last_photo_time = time.time()*1000
        else:
            break
