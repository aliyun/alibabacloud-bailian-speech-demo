# For prerequisites running the following sample, visit https://help.aliyun.com/zh/model-studio/getting-started/first-api-call-to-qwen

import os
import signal  # for keyboard events handling (press "Ctrl+C" to terminate recording and translation)
import sys

import dashscope
import pyaudio
from dashscope.audio.asr import *

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
    def on_open(self) -> None:
        global mic
        global stream
        print('TranslationRecognizerCallback open.')
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=16000,
                          input=True)

    def on_close(self) -> None:
        global mic
        global stream
        print('TranslationRecognizerCallback close.')
        stream.stop_stream()
        stream.close()
        mic.terminate()
        stream = None
        mic = None

    def on_complete(self) -> None:
        print('Translation completed.')  # translation completed

    def on_error(self, message) -> None:
        print('TranslationRecognizerCallback task_id: ', message.request_id)
        print('TranslationRecognizerCallback error: ', message.message)
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
        if transcription_result is not None:
            print('transcription: {}'.format(transcription_result.text))
            if transcription_result.stash is not None:
                print('transcription stash: {}'.format(transcription_result.stash.text))
            if transcription_result.is_sentence_end:
                print('request id: ', request_id)
                print('usage: ', usage)
        if translation_result is not None:
            # print(
            #     "translation_languages: ",
            #     translation_result.get_language_list(),
            # )
            translation = translation_result.get_translation(target_language)
            # print("sentence id: ", translation.sentence_id)
            print('translate to {}: {}'.format(target_language,
                                               translation.text))
            if translation.stash is not None:
                print('translate to {} stash: {}'.format(
                    target_language,
                    translation_result.get_translation('en').stash.text,
                ))
            if translation.is_sentence_end:
                print('request id: ', request_id)
                print('usage: ', usage)


def signal_handler(sig, frame):
    print('Ctrl+C pressed, stop translation ...')
    # Stop translation
    translator.stop()
    print('Translation stopped.')
    print(
        '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
        .format(
            translator.get_last_request_id(),
            translator.get_first_package_delay(),
            translator.get_last_package_delay(),
        ))
    # Forcefully exit the program
    sys.exit(0)


# main function
if __name__ == '__main__':
    init_dashscope_api_key()
    print('Initializing ...')

    # Create the translation callback
    callback = Callback()

    # Call translation service by async mode, you can customize the translation parameters, like model, format,
    # sample_rate For more information, please refer to https://help.aliyun.com/document_detail/2712536.html
    translator = TranslationRecognizerRealtime(
        model='gummy-realtime-v1',
        format='pcm',
        sample_rate=16000,
        transcription_enabled=False,
        translation_enabled=True,
        translation_target_languages=[target_language],
        callback=callback,
    )

    # Start translation
    translator.start()

    signal.signal(signal.SIGINT, signal_handler)
    print("Press 'Ctrl+C' to stop recording and translation...")
    # Create a keyboard listener until "Ctrl+C" is pressed

    while True:
        if stream:
            data = stream.read(3200, exception_on_overflow=False)
            translator.send_audio_frame(data)
        else:
            break

    translator.stop()
