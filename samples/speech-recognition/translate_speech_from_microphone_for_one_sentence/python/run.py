# For prerequisites running the following sample, visit https://help.aliyun.com/zh/model-studio/getting-started/first-api-call-to-qwen

import os
import sys
from datetime import datetime

import dashscope
import pyaudio
from dashscope.audio.asr import *


def get_timestamp():
    """return timestamp in milliseconds"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


mic = None
stream = None
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
    def __init__(self):
        super().__init__()
        self.pre_end_detected = False

    def on_open(self) -> None:
        global mic
        global stream
        print('\t[log] TranslationRecognizerCallback open.')
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=16000,
                          input=True)
        print('\t[log] Recording...')

    def on_close(self) -> None:
        global mic
        global stream
        print('\t[log] TranslationRecognizerCallback close.')
        stream.stop_stream()
        stream.close()
        mic.terminate()
        stream = None
        mic = None

    def on_complete(self) -> None:
        print('\t[log] Translation completed.')  # translation completed

    def on_error(self, message) -> None:
        print('\t[log] TranslationRecognizerCallback task_id: ',
              message.request_id)
        print('\t[log] TranslationRecognizerCallback error: ', message.message)
        # Stop and close the audio stream if it is running
        if 'stream' in globals() and stream.active:
            stream.stop()
            stream.close()
        # Forcefully exit the program
        sys.exit(1)

    def on_event(
        self,
        request_id,
        transcription_result: TranscriptionResult,
        translation_result: TranslationResult,
        usage,
    ) -> None:
        print('- - - - - - - - - - -')
        if transcription_result is not None:
            print('[{}] transcript : {}'.format(get_timestamp(),
                                                transcription_result.text))

        if translation_result is not None:
            translation: Translation = translation_result.get_translation(
                target_language)
            if self.pre_end_detected:
                if translation.pre_end_failed:
                    print('[{}] <=== [vad pre_end failed] ===>'.format(
                        get_timestamp()))
                    self.pre_end_detected = False
            if translation.vad_pre_end:
                print('[{}] <=== [vad pre_end] ===>'.format(get_timestamp()))
                self.pre_end_detected = True
            # print("sentence id: ", translation.sentence_id)
            print('[{}] translate to {}: {}'.format(get_timestamp(),
                                                    target_language,
                                                    translation.text))
            if translation.is_sentence_end:
                print('request id: {} usage: {}'.format(request_id, usage))


# main function
if __name__ == '__main__':
    init_dashscope_api_key()
    print('\t[log] Initializing ...')

    # Create the translation callback
    callback = Callback()

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
    print('\t[log] Translation started')

    print('translation will stop after recording one sentence...')
    # Create a keyboard listener until "Ctrl+C" is pressed

    # save recorded audio
    audio_buffer = []
    while True:
        if stream:
            data = stream.read(3200, exception_on_overflow=False)
            audio_buffer.append(data)
            if translator.send_audio_frame(data):
                pass
                # print("\t[log] send audio frame success")
            else:
                print('\t[log] sentence end, stop sending')
                break
        else:
            break

    translator.stop()

    with open('{}_record.pcm'.format(translator.last_request_id), 'wb') as f:
        for audio in audio_buffer:
            f.write(audio)
    print('\t[log] Recorded audio saved to {}_record.pcm')
    print(
        '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
        .format(
            translator.get_last_request_id(),
            translator.get_first_package_delay(),
            translator.get_last_package_delay(),
        ))
