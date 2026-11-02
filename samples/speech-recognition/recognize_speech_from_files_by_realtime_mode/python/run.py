#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import multiprocessing
import os
import threading
import sys

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../../utils/python'))

from dashscope import Client
from AudioDecoder import AudioDecodeCallback, AudioDecoder


def get_api_key():
    """Load DashScope API key from environment or use a placeholder."""
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']
    return '<your-dashscope-api-key>'


def process_recognition(file_path):
    """Decode one media file and stream its audio to realtime ASR (V2 SDK)."""
    api_key = get_api_key()
    print(f'recognition with file :{file_path}')

    client = Client(api_key=api_key)
    try:
        session = client.audio.asr.recognize(
            model='fun-asr-realtime',
            # 'paraformer-realtime-v2' is also supported by the V2 SDK
            format='opus',
            # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr',
            # we recommend using 'opus', opus is a very efficient zip format
            sample_rate=16000,  # supported 8000、16000
        )
        session.start()

        recognized_text = []

        def consume_results():
            """Consume ASR result events until the session finishes."""
            for result in session.results():
                sentence = result.get_sentence()
                if sentence and sentence.get('text') and result.is_sentence_end():
                    recognized_text.append(sentence['text'])

        consumer = threading.Thread(target=consume_results)
        consumer.start()

        class MyAudioDecoderCallback(AudioDecodeCallback):
            def on_audio_data(self, audio_data):
                if audio_data is not None:
                    session.send_audio_frame(audio_data)

        audio_decoder = AudioDecoder(MyAudioDecoderCallback())
        # This interface does not support PCM RAW format for compression.
        # You can convert to WAV format for input.
        audio_decoder.decode_audio_in_blocks(file_path)

        # Stop recognition and wait for the final events to drain.
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
        session.close()
        client.close()

    return ''.join(recognized_text)


def multi_process_recognition():
    # Get the number of CPU cores available
    num_cores = multiprocessing.cpu_count()

    # Create a pool of processes with the number of available CPU cores
    process_pool = multiprocessing.Pool(processes=num_cores)

    # Please replace the path with your audio source
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_list = [
        os.path.join(current_dir, '../../..', 'sample-data',
                     'sample_video_story.mp4'),
        os.path.join(current_dir, '../../..', 'sample-data',
                     'sample_audio.mp3')
    ]

    # Use the map method to distribute tasks among the pool and collect the results
    process_pool.map(process_recognition, file_list)


if __name__ == '__main__':
    multi_process_recognition()
