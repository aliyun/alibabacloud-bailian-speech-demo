#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import json
import os
import sys
import threading

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../../utils/python'))

from dashscope import Client
from AudioDecoder import AudioDecoder


def get_api_key():
    """
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']
    return '<your-dashscope-api-key>'


class RecognizeSpeechFromSingleFile:
    def __init__(self):
        pass

    def recognize_file(self, file_path: str):
        # Initialize recognition service by sync call
        # you can customize the recognition parameters, like model, format, sample_rate
        # for more information, please refer to https://help.aliyun.com/document_detail/2712536.html
        api_key = get_api_key()
        client = Client(api_key=api_key)
        recognition = None
        try:
            recognition = client.audio.asr.recognize(
                model='fun-asr-realtime',
                # 'paraformer-realtime-v2' is also supported by the V2 SDK
                format='opus',
                # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
                sample_rate=16000,  # supported 8000、16000
            )
            recognition.start()

            sentences = []

            def consume_results():
                for result in recognition.results():
                    sentence = result.get_sentence()
                    if sentence and sentence.get('text'):
                        sentences.append(sentence)

            consumer = threading.Thread(target=consume_results)
            consumer.start()

            chunk_size = 3200
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    recognition.send_audio_frame(chunk)

            recognition.stop()
            consumer.join(timeout=30)

            print(
                '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
                .format(
                    recognition.request_id,
                    recognition.first_package_delay,
                    recognition.last_package_delay,
                ))
            return sentences
        finally:
            if recognition is not None:
                recognition.close()
            client.close()


# main function
if __name__ == '__main__':
    # Please replace the path with your audio file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '../../..', 'sample-data',
                             'sample_video_poetry.mp4')
    print('Input file is: %s' % file_path)

    decoded_file_path = os.path.join(current_dir, 'temp_decoded.opus')

    # Suggest decode your audio/video file to 16k 16bit mono opus format file to current directory
    audio_decoder = AudioDecoder()
    audio_decoder.convert_to_opus_file(file_path, decoded_file_path)

    # Initialize recognition
    speech_recognizer = RecognizeSpeechFromSingleFile()
    print('Recognizing speech ...')
    sentence_list = speech_recognizer.recognize_file(decoded_file_path)

    # Check the result
    with open('result.json', 'wb') as file_json:
        file_json.write(
            json.dumps(sentence_list, indent=4,
                       ensure_ascii=False).encode('utf-8'))
    print('Full recognition result is saved into file: result.json')
    print('\nThe brief result is:')

    for sent in sentence_list:
        print(sent.get('text', ''), end='')
    print()

    # Remove the decoded file
    os.remove(decoded_file_path)
