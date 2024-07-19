#!/usr/bin/env python3
# Copyright (c) alibaba.. All Rights Reserved.
#  MIT License  (https://opensource.org/licenses/MIT)
import json
import os
from http import HTTPStatus
import requests
import dashscope
from dashscope import Generation

# Set your DashScope API key. More information: https://help.aliyun.com/document_detail/2712195.html
if 'DASHSCOPE_API_KEY' in os.environ:
    dashscope.api_key = os.environ['DASHSCOPE_API_KEY']
    # in fact,if you have set DASHSCOPE_API_KEY in your environment variable,
    # you can ignore this, and the sdk will automatically get the api_key from the environment variable
else:
    dashscope.api_key = '<your-dashscope-api-key>'
    # if you can not set api_key in your environment variable,
    # you can set it here by code

# Submit the transcription task files list
# the transcription api supports most of the common audio formats
# you can check supported formats and other parameters here: https://help.aliyun.com/document_detail/2712535.html
# transcription api supports 100 files at most in one job, and each file size should be less than 2GB
file_path = './transcription_result.json'


def download_file(url, local_path):
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


def read_file_get_content(file_path):
    """
        Reads a file and retrieves its content.

        Parameter:
        - file_path: File Path

        Return Value:
        String representation of file content.
    """
    with open(file_path, 'r') as f:
        trans_result = f.read()
        print("trans_result: ", trans_result)
        if trans_result:
            trans_result = json.loads(trans_result)
            text = trans_result['transcripts'][0]['text']
            print("transcript_result: ", text)
            return text


def call_llm(query: str):
    """
        Invokes an LLM Model for Quality Assurance Tasks.

        Parameter:
        - query: Input Query String

        Return Value:
        None
    """
    prompt = ('你的角色是一个客服质检员，你需要根据输入文本，根据规定格式给出结果。'
              '请根据输入文本，检测其中是否包含打招呼的词，如"你好"。'
              '如果包含，返回"包含"'
              '如果不包含，返回"不包含"。'
              '如果包含，给出包含的原始片段。'
              '以下是输入文本：')
    prompt += query
    messages = [{'role': 'user', 'content': prompt}]


    # Prepare for the LLM call
    responses = Generation.call(
        model='qwen-turbo',
        messages=messages,
        stream=True,  # enable stream output
        # incremental_output=True,  # enable incremental output
    )
    for response in responses:
        if response.status_code == HTTPStatus.OK :
            if response.output.get('finish_reason') == 'stop':
                print("perform_quality_assurance result:",response.output)
        else:
            print(
                'Request id: %s, Status code: %s, error code: %s, error message: %s'
                % (
                    response.request_id,
                    response.status_code,
                    response.code,
                    response.message,
                ))

def transcript_audo_file():
    # Submit the transcription task
    task_response = dashscope.audio.asr.Transcription.async_call(
        model='paraformer-v1',
        file_urls=[
            'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav'])
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
                    transcription_result = download_file(transcription_url, "./transcription_result.json")
                    print("transcription_result: ", transcription_result)
                    return transcription_result


if __name__ == '__main__':
    # 1. transcribe audio file
    trans_result_link = transcript_audo_file()
    # 2. download the transcription result
    if trans_result_link:
        download_file(trans_result_link, file_path)
    # 3. read the transcription result
    trans_result_text = read_file_get_content(file_path)
    # 4. do perform quality assurance with the transcription result
    call_llm(trans_result_text)