# For prerequisites running the following sample, visit https://help.aliyun.com/zh/model-studio/getting-started/first-api-call-to-qwen

import multiprocessing
import os
import threading
import time

from dashscope import Client

target_language = 'en'


def get_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']
    return '<your-dashscope-api-key>'


def receive_events(session, sentence_finished):
    """Consume translation events until the first sentence finishes."""
    try:
        for event in session.events():
            kind = event.get('type')
            if kind == 'response.text.delta':
                print(event.get('delta', ''), end='', flush=True)
            elif kind == 'response.text.done':
                print('\n[translation done] ', event.get('text', ''))
                sentence_finished.set()
            elif kind == 'conversation.item.input_audio_transcription.completed':
                print('\n[transcript] ', event.get('transcript', ''))
            elif kind == 'response.done':
                sentence_finished.set()
    except Exception as e:
        print('receive error: {}'.format(e))


def process_translation(file_path):
    api_key = get_api_key()
    print(f'translation with file :{file_path}')

    client = Client(api_key=api_key)
    try:
        session = client.audio.realtime.connect(
            model='qwen3.8-livetranslate-flash-realtime',
        )
        session.connect()
        session.update_session(
            output_modalities=["text"],
            translation_params={"language": target_language},
        )

        sentence_finished = threading.Event()
        receiver = threading.Thread(target=receive_events,
                                    args=(session, sentence_finished))
        receiver.start()

        try:
            with open(file_path, 'rb') as f:
                if os.path.getsize(file_path):
                    while not sentence_finished.is_set():
                        audio_data = f.read(3200)
                        if not audio_data:
                            break
                        session.append_audio(audio_data)
                        time.sleep(0.01)
                else:
                    raise Exception('The supplied file was empty (zero bytes long)')
        finally:
            session.close()
            receiver.join(timeout=30)

        print(
            '[Metric] requestId: {}, first text delay ms: {}'.format(
                session.last_response_id,
                session.last_first_text_delay,
            ))
    finally:
        client.close()


def multi_process_recognition():
    # Get the number of CPU cores available
    num_cores = multiprocessing.cpu_count()

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


if __name__ == '__main__':
    multi_process_recognition()
