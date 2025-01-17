#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import time
import wave

import pyaudio

CHUNK = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000


def record_audio_from_voice_clonse():
    mic = pyaudio.PyAudio()
    stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)
    start_time = time.time()
    audio_buffer = []
    print('请在录音开始后朗读以下中文示例文案，或您准备好的其他文案。')
    print('示例文案：在这个世界上，最重要的事情就是保持好奇心，不断去探索未知的领域，只有这样我们才能成长并有所突破。')
    print('开始录音...')
    # record for 10 seconds
    while time.time() - start_time < 10:
        if stream:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_buffer.append(data)
    stream.stop_stream()
    mic.terminate()
    # convert pcm to wave file
    output_wave_file = 'your_record_file.wav'
    with wave.open(output_wave_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(mic.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(audio_buffer))
    print(f'录音保存在 {output_wave_file}')
    print('... 请将录制好的音频上传到云端并获取可下载http链接。')
    print('... 如果您没有云存储能力，可以使用阿里云的OSS（对象存储服务），上传录制好的音频到oss，并获取一个具有失效的url链接。')
    print('... https://help.aliyun.com/zh/oss/user-guide/simple-upload')


# main function
if __name__ == '__main__':
    record_audio_from_voice_clonse()
