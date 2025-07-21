import os
import sys
import time
import pyaudio
import dashscope
from dashscope.audio.qwen_tts_realtime import *

from B64PCMPlayer import B64PCMPlayer

voice = 'Chelsie'

pya = None
b64_player: B64PCMPlayer = None
qwen_tts_realtime: QwenTtsRealtime = None
text_to_synthesize = [
    '1500能源',
    '是人类赖以',
    '生存和发展的',
    '重要物质基',
    '础，能源低碳',
    '发展关乎人类',
    '未来。工业革命',
    '以来，化石能源',
    '大规模开发利用',
    '有力推动了人类文明',
    '进步，但也产生资',
    '源枯竭、气候变化、',
    '地缘政治冲突等问题。',
]

DO_VIDEO_TEST = False

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



class MyCallback(QwenTtsRealtimeCallback):
    def on_open(self) -> None:
        global pya
        global b64_player
        print('connection opened, init player')
        pya = pyaudio.PyAudio()
        b64_player = B64PCMPlayer(pya, save_file=True)

    def on_close(self, close_status_code, close_msg) -> None:
        print('connection closed with code: {}, msg: {}, destroy player'.format(close_status_code, close_msg))
        global pya
        global b64_player
        # b64_player.wait_for_complete()
        b64_player.shutdown()
        if pya:
            pya.terminate()
            pya = None

    def on_event(self, response: str) -> None:
        try:
            global qwen_tts_realtime
            global b64_player
            type = response['type']
            if 'session.created' == type:
                print('start session: {}'.format(response['session']['id']))
            if 'response.audio.delta' == type:
                recv_audio_b64 = response['delta']
                b64_player.add_data(recv_audio_b64)
            if 'response.done' == type:
                print(f'response {qwen_tts_realtime.get_last_response_id()} done')
            if 'session.finished' == type:
                print('session finished')
        except Exception as e:
            print('[Error] {}'.format(e))
            return



if __name__  == '__main__':
    init_dashscope_api_key()

    print('Initializing ...')

    callback = MyCallback()

    qwen_tts_realtime = QwenTtsRealtime(
        model='qwen-tts-realtime',
        callback=callback, 
        )

    qwen_tts_realtime.connect()
    qwen_tts_realtime.update_session(
        voice = 'Cherry',
        response_format = AudioFormat.PCM_24000HZ_MONO_16BIT,
        mode = 'server_commit'        
    )
    for text_chunk in text_to_synthesize:
        print(f'send texd: {text_chunk}')
        qwen_tts_realtime.append_text(text_chunk)
        time.sleep(0.1)
    qwen_tts_realtime.finish()
    print('[Metric] session: {}, first audio delay: {}'.format(
                    qwen_tts_realtime.get_session_id(), 
                    qwen_tts_realtime.get_first_audio_delay(),
                    ))
