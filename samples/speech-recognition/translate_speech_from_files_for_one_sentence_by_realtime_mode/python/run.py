# For prerequisites running the following sample, visit https://help.aliyun.com/zh/model-studio/getting-started/first-api-call-to-qwen

import multiprocessing
import os
import time

import dashscope
from dashscope.audio.asr import *

target_language = 'en'


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


class Callback(TranslationRecognizerCallback):
    def __init__(self, tag, file_path) -> None:
        super().__init__()
        self.tag = tag
        self.file_path = file_path
        self.text = ''
        self.translate_text = ''

    def on_open(self) -> None:
        print(f'[{self.tag}] TranslationRecognizerCallback open.')

    def on_close(self) -> None:
        print(f'[{self.tag}] TranslationRecognizerCallback close.')

    def on_event(
        self,
        request_id,
        transcription_result: TranscriptionResult,
        translation_result: TranslationResult,
        usage,
    ) -> None:
        if translation_result is not None:
            translation = translation_result.get_translation(target_language)
            # print(f'[{self.tag}]RecognitionCallback text: ', sentence['text']) partial recognition result
            if translation.is_sentence_end:
                self.translate_text = self.translate_text + translation.text
        if transcription_result is not None:
            if transcription_result.is_sentence_end:
                self.text = self.text + transcription_result.text

    def on_error(self, message) -> None:
        print('error: {}'.format(message))

    def on_complete(self) -> None:
        print(f'[{self.tag}] Transcript ==> ', self.text)
        print(f'[{self.tag}] Translate ==> ', self.translate_text)
        print(f'[{self.tag}] Translation completed')  # translation complete


def process_translation(file_path):
    init_dashscope_api_key()
    print(f'translation with file :{file_path}')
    # Create the translation callback
    callback = Callback(f'process {os.getpid()}', file_path)

    # Call translation service by async mode, you can customize the translation parameters, like model, format,
    # sample_rate For more information, please refer to https://help.aliyun.com/document_detail/2712536.html
    translator = TranslationRecognizerChat(
        model='gummy-chat-v1',
        format='pcm',
        sample_rate=16000,
        transcription_enabled=True,
        translation_enabled=True,
        translation_target_languages=[target_language],
        callback=callback,
    )

    # Start translation
    translator.start()

    try:
        audio_data: bytes = None
        f = open(file_path, 'rb')
        if os.path.getsize(file_path):
            while True:
                audio_data = f.read(3200)
                if not audio_data:
                    break
                else:
                    if translator.send_audio_frame(audio_data):
                        pass
                        # print("\t[log] send audio frame success")
                    else:
                        print('\t[log] sentence end, stop sending')
                        break
                time.sleep(0.01)
        else:
            raise Exception('The supplied file was empty (zero bytes long)')
        f.close()
    except Exception as e:
        raise e

    translator.stop()
    print(
        '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
        .format(
            translator.get_last_request_id(),
            translator.get_first_package_delay(),
            translator.get_last_package_delay(),
        ))
    return callback.text


def multi_process_recognition():
    # Get the number of CPU cores available
    num_cores = multiprocessing.cpu_count()
    # print(f"Number of CPU cores: {num_cores}")

    # Create a pool of processes with the number of available CPU cores
    process_pool = multiprocessing.Pool(processes=num_cores)

    # Please replace the path with your audio source
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_list = [
        os.path.join(current_dir, '../../..', 'sample-data',
                     'asr_example_chat.wav'),
        os.path.join(current_dir, '../../..', 'sample-data',
                     'asr_example_chat.wav')
    ]

    # Use the map method to distribute tasks among the pool and collect the results
    process_pool.map(process_translation, file_list)
    exit(0)


if __name__ == '__main__':
    multi_process_recognition()
