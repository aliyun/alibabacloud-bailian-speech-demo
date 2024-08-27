# coding=utf-8
# !/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import sys
import json
import os
from http import HTTPStatus
import requests
import dashscope
from dashscope import Generation

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../utils/python'))
from AudioDecoder import AudioDecoder
# import ossUtil

transcription_result_file_path = './transcription_result.json'
temp_opus_file_path = './temp_decoded.opus'
llm_model = 'qwen-max'


def init_dashscope_api_key():
    """
        Set your DashScope API-key. More information:
        https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    """

    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ['DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually


def decode_mp4_to_opus_file(mp4_file_path: str) -> str:
    """
    Decodes an MP4 file to an OPUS file.
    Parameter:
    - mp4_file_path: Video File Path
    Return Value:
    OPUS File Path
    """

    print('Input video file is: %s' % mp4_file_path)
    decoded_file_path = os.path.join(current_dir, temp_opus_file_path)

    # Decode your audio/video file to 16k 16bit mono pcm file to current directory
    audio_decoder = AudioDecoder()
    audio_decoder.convert_to_opus_file(mp4_file_path, decoded_file_path)
    return decoded_file_path


def upload_audio_file_to_oss(audio_file_path: str) -> str:
    """
    Uploads an audio file to OSS.
    Parameter:
    - audio_file_path: Audio File Path
    Return Value:
    OSS URL
    """

    # To use the following code, you need to set up an OSS bucket and upload the file to it.
    # file_link = ossUtil.upload_file_and_get_link(audio_file_path, temp_opus_file_path)

    # We have returned a preprocessed file link to the sample temp_decoded.opus file.
    # You can use Aliyun OSS(https://help.aliyun.com/zh/oss/user-guide/upload-objects-to-oss)
    # to upload your file and generate an accessible link.
    return "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/sample_for_incalculable_value.opus"


def _download_file(url, local_path):
    """
        Downloads a file from a given URL to a local path.

        Parameters:
        - url: File URL Address
        - local_path: Local Path where the file will be saved

        Returns:
        None
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"File downloaded successfully and saved to: {local_path}")
    except requests.RequestException as e:
        print(f"Failed to download the file: {e}")


def call_llm_with_prompt(prompt: str) -> str:
    """
        Invokes an LLM Model with prompt

        Parameter:
        - prompt: Input Query String

        Return Value:LLM Response
    """

    # Prepare for the LLM call
    responses = Generation.call(
        model=llm_model,
        prompt=prompt,
        stream=True,  # enable stream output
        # incremental_output=True,  # enable incremental output
    )
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            if response.output.get('finish_reason') == 'stop':
                return response.output.get('text')
        else:
            print(
                'Request id: %s, Status code: %s, error code: %s, error message: %s'
                % (
                    response.request_id,
                    response.status_code,
                    response.code,
                    response.message,
                ))


def call_llm_with_messages(system_content: str, user_content: str):
    """
        Invokes an LLM Model with messages

        Parameter:
        - system_content: System Content
        - user_content: User Content

        Return Value: LLM Response
    """
    messages = [{'role': 'system', 'content': system_content},
                {'role': 'user', 'content': user_content}]

    response = dashscope.Generation.call(
        model=llm_model,
        messages=messages,
        result_format='message',  # 将返回结果格式设置为 message
    )
    if response.status_code == HTTPStatus.OK:
        return response.output.choices[0]['message']['content']
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


def transcribe_audio_file(file_link: str):
    """
        Transcribes an audio file.
        Parameter:
        - file_link: Audio File URL
        Return Value:
        None
    """

    # Submit the transcription task
    # the transcription api supports most of the common audio formats
    # you can check supported formats and other parameters here: https://help.aliyun.com/document_detail/2712535.html
    # transcription api supports 100 files at most in one job, and each file size should be less than 2GB
    task_response = dashscope.audio.asr.Transcription.async_call(
        model='paraformer-v1',
        file_urls=[file_link])
    # This is the description of 'file_urls'.
    # You need to provide a URL from which the file can be downloaded via HTTP.
    # Typically, we can **store these files in public cloud storage services (such as Alibaba Cloud OSS)**
    # and share a publicly accessible link.
    # Note that it is best to add an expiration time to these links,
    # to prevent third-party access if the file address is leaked.

    # get the transcription result
    transcribe_response = dashscope.audio.asr.Transcription.wait(
        task=task_response.output.task_id)
    if transcribe_response.status_code == HTTPStatus.OK:
        print(json.dumps(transcribe_response.output, indent=4, ensure_ascii=False))
        print('file transcription done!')
        # you will get the transcription result in the transcribe_response.output by param : transcription_url
        # transcription_url is a downloadable file of json format transcription result

        if transcribe_response.output.task_status == 'SUCCEEDED':
            transcription_result = transcribe_response.output.get('results')
            if transcription_result:
                transcription_url = json.loads(json.dumps(transcription_result))[0]['transcription_url']
                print("get transcription_url: ", transcription_url)
                if transcription_url:
                    # download the transcription result
                    _download_file(transcription_url, transcription_result_file_path)


if __name__ == '__main__':
    # Please replace the path with your audio file path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    video_file_path = os.path.join(current_dir, '../../..', 'sample-data',
                                   "sample_for_incalculable_value.mp4")

    # 0. init dashscope api key
    init_dashscope_api_key()
    # 1. decode mp4 file to opus audio file
    opus_file = decode_mp4_to_opus_file(video_file_path)
    # 2. upload audio file to oss, generate a file url
    audio_file_url = upload_audio_file_to_oss(opus_file)
    # TRANSCRIBE
    # 3. transcribe audio file
    transcribe_audio_file(audio_file_url)

    # 4. read the transcription result
    # 5. translate
    print("\n\n============= transcribe and translate === START ===")
    prompt_for_translate = ('Your role is a translator. '
                            'Please translate the inputted Chinese into English, '
                            'ensuring semantic coherence as much as possible. '
                            'Below is the original text:')
    with open(transcription_result_file_path, 'r', encoding='utf-8') as f:
        trans_result = f.read()
        # print("trans_result: ", trans_result)
        if trans_result:
            trans_result = json.loads(trans_result)
            trans_result_text = trans_result['transcripts'][0]['text']

            if trans_result['transcripts'][0]['sentences']:
                for sentence in trans_result['transcripts'][0]['sentences']:
                    text = sentence['text']
                    translate_result = call_llm_with_prompt(prompt_for_translate + text)
                    print("transcribe==>", text)
                    print("translate ==>", translate_result, "\n")

    print("============= transcribe and translate ===  END  ===")

    # 6. meeting summary
    prompt_for_summary = ('你的角色是文档总结助理。'
                          '请根据输入文本，从中给出重要摘要信息。摘要要至少列举出3个以上关键点,使用数字小标题并换行分隔，每个关键点一行即可,并给出全文总结。整体文本简略，总回复不超过80字。'
                          '以下是输入文本内容：')
    summary_result = call_llm_with_prompt(prompt_for_summary + trans_result_text)
    print("\n\n============= summary === START ===")
    print(summary_result)
    print("============= summary ===  END  ===")

    # 7. meeting QA
    content_for_system = ('你的角色是内容归纳专家。你需要理解输入的文本内容。并回答用户的问题。'
                          '以下是输入文本内容：') + trans_result_text
    question = '人类什么时候发明的电灯'
    content_for_user = f'用户的问题是：{question}'
    qa_result = call_llm_with_messages(content_for_system, content_for_user)
    print("\n\n============= QA === START ===")
    print(f"question is: {question}")
    print(f"result   is: {qa_result}")
    print("============= QA ===  END  ===")

    # remove temp files
    os.remove(temp_opus_file_path)
    os.remove(transcription_result_file_path)
