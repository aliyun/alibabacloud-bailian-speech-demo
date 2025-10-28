import logging
import os
import base64
import signal
import sys
import time
import pyaudio
import dashscope
from dashscope.audio.qwen_omni import *

from B64PCMPlayer import B64PCMPlayer
from dashscope.audio.qwen_omni.omni_realtime import TranscriptionParams

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
conversation = None

def init_dashscope_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ[
            'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = 'YOUR_API_KEY'  # set API-key manually


class MyCallback(OmniRealtimeCallback):
    def on_open(self) -> None:
        global pya
        global mic_stream
        print('connection opened, init microphone')
        pya = pyaudio.PyAudio()
        mic_stream = pya.open(format=pyaudio.paInt16,
                              channels=1,
                              rate=16000,
                              input=True)

    def on_close(self, close_status_code, close_msg) -> None:
        print('connection closed with code: {}, msg: {}, destroy microphone'.format(close_status_code, close_msg))
        sys.exit(0)

    def on_event(self, response: str) -> None:
        try:
            global conversation
            type = response['type']
            if 'session.created' == type:
                print('start session: {}'.format(response['session']['id']))
            if 'conversation.item.input_audio_transcription.completed' == type:
                print('final recognized text: {}'.format(response['transcript']))
            if 'conversation.item.input_audio_transcription.text' == type:
                text = response['stash']
                print("got stash result: {}".format(text))
            if 'input_audio_buffer.speech_started' == type:
                print('======Speech Start======')
            if 'input_audio_buffer.speech_stopped' == type:
                print('======Speech Stop======')
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


if __name__ == '__main__':
    init_dashscope_api_key()

    print('Initializing ...')

    record_pcm_file = open('./record_16khz.pcm', 'wb')

    callback = MyCallback()

    conversation = OmniRealtimeConversation(
        model='qwen3-asr-flash-realtime',
        url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime',
        callback=callback,
    )

    conversation.connect()

    transcription_params = TranscriptionParams(
        language='zh',
        sample_rate=16000,
        input_audio_format="pcm",
        corpus_text="这是一段中文对话"
    )

    conversation.update_session(
        output_modalities=[MultiModality.TEXT],
        enable_input_audio_transcription=True,
        transcription_params=transcription_params,
    )

    def signal_handler(sig, frame):
        print('Ctrl+C pressed, stop recognition ...')
        # Stop recognition
        conversation.close()
        print('omni realtime stopped.')
        # Forcefully exit the program
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)
    print("Press 'Ctrl+C' to stop conversation...")

    while True:
        if mic_stream:
            audio_data = mic_stream.read(3200, exception_on_overflow=False)
            record_pcm_file.write(audio_data)
            audio_b64 = base64.b64encode(audio_data).decode('ascii')
            conversation.append_audio(audio_b64)

        else:
            break