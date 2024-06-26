import subprocess
import threading

import pyaudio
from dashscope.audio.tts_v2 import *


# Define a callback to handle the result
class RealtimeMp3Player:
    def __init__(self):
        self.ffmpeg_process = None
        self._stream = None
        self._player = None
        self.play_thread = None
        self.stop_event = threading.Event()

    def start(self):
        self._player = pyaudio.PyAudio()  # initialize pyaudio to play audio
        self._stream = self._player.open(
            format=pyaudio.paInt16, channels=1, rate=22050,
            output=True)  # initialize pyaudio stream
        self.ffmpeg_process = subprocess.Popen(
            [
                'ffmpeg', '-i', 'pipe:0', '-f', 's16le', '-ar', '22050', '-ac',
                '1', 'pipe:1'
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )  # initialize ffmpeg to decode mp3
        print('audio player is started')

    def stop(self):
        self.ffmpeg_process.stdin.close()
        self.ffmpeg_process.wait()
        self.play_thread.join()
        self._stream.stop_stream()
        self._stream.close()
        self._player.terminate()
        if self.ffmpeg_process:
            self.ffmpeg_process.terminate()
        print('audio player is stoped')

    def play_audio(self):
        # play audio with pcm data decode by ffmpeg
        while not self.stop_event.is_set():
            pcm_data = self.ffmpeg_process.stdout.read(1024)
            if pcm_data:
                self._stream.write(pcm_data)
            else:
                break

    def write(self, data: bytes) -> None:
        # print('write audio data:', len(data))
        self.ffmpeg_process.stdin.write(data)
        if self.play_thread is None:
            # initialize play thread
            print('start play thread')
            self._stream.start_stream()
            self.play_thread = threading.Thread(target=self.play_audio)
            self.play_thread.start()
