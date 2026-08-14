#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

import os
import sys
import time

import dashscope
from dashscope.audio.asr import (Recognition, RecognitionCallback,
                                 RecognitionResult)

# This demo focuses on the conversation context (`context`) of
# qwen-audio-3.0-asr-flash-streaming. The context is passed through the
# `raw_input` parameter and helps the model recognize domain-specific words,
# proper nouns and follow-up utterances more accurately.
#
# Two ways to use the context are demonstrated:
#   1. dialog history  : previous user utterances and assistant replies
#   2. domain word list: a `user` message carrying domain terms only
#
# Constraints of the context (enforced by the service):
#   - at most 5 `input_text` messages and 5 `text` messages, the latest are kept
#   - the total text length of one round must not exceed 400 characters
#   - messages must be ordered by round, and the `user` message of one round
#     must come before its `assistant` message
#   - requires dashscope SDK >= 1.25.23
#
# for more information, please refer to https://help.aliyun.com/document_detail/2712536.html

# supported model : 'qwen-audio-3.0-asr-flash-streaming'
MODEL = 'qwen-audio-3.0-asr-flash-streaming'

# the service keeps at most 5 messages for each content type
MAX_MESSAGES_PER_TYPE = 5

# the total text length of one round must not exceed 400 characters
MAX_CONTEXT_TEXT_LENGTH = 400


def init_dashscope_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ[
            'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
    else:
        dashscope.api_key = '<your-dashscope-api-key>'  # set API-key manually


def init_dashscope_endpoint():
    '''
    The qwen-audio series models are served under a workspace-specific endpoint,
    so both the HTTP and the WebSocket base urls have to be redirected to
    https://{workspace_id}.cn-beijing.maas.aliyuncs.com . The workspace id can be
    found on the Alibaba Cloud Model Studio console.
    '''
    workspace_id = os.environ.get('DASHSCOPE_WORKSPACE_ID')
    if not workspace_id:
        print('the environment variable DASHSCOPE_WORKSPACE_ID is required, '
              'because the qwen-audio series models are served under a '
              'workspace-specific endpoint. Please set it to your Model Studio '
              'workspace id, for example: export DASHSCOPE_WORKSPACE_ID=llm-xxxxxx')
        sys.exit(1)
    dashscope.base_http_api_url = (
        f'https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1')
    dashscope.base_websocket_api_url = (
        f'wss://{workspace_id}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference'
    )


def build_context(history_messages):
    '''
    Convert a simple conversation history list into the `raw_input` structure
    required by the service:

        {
            "context": [
                {"role": "user",      "content": [{"type": "input_text", "text": "..."}]},
                {"role": "assistant", "content": [{"type": "text",       "text": "..."}]}
            ]
        }

    The `user` role carries the recognition result of previous rounds or a
    domain word list, the `assistant` role carries the replies of the LLM.
    Returns an empty dict when there is no valid history.
    '''
    if not history_messages:
        return {}

    # keep at most MAX_MESSAGES_PER_TYPE messages for each role, the latest win
    user_messages = [m for m in history_messages if m.get('role') == 'user']
    assistant_messages = [
        m for m in history_messages if m.get('role') == 'assistant'
    ]
    kept = set(
        id(m) for m in user_messages[-MAX_MESSAGES_PER_TYPE:] +
        assistant_messages[-MAX_MESSAGES_PER_TYPE:])

    context_list = []
    total_length = 0
    for msg in history_messages:
        if id(msg) not in kept:
            continue
        role = msg.get('role')
        text = msg.get('text', '')
        if not role or not text:
            continue

        # truncate from the tail once the total length limit is reached
        remaining = MAX_CONTEXT_TEXT_LENGTH - total_length
        if remaining <= 0:
            print('[context] total text length limit reached, '
                  'the remaining messages are dropped.')
            break
        if len(text) > remaining:
            text = text[:remaining]
            print('[context] message truncated to fit the 400-character limit.')
        total_length += len(text)

        # user -> input_text, assistant -> text
        content_type = 'input_text' if role == 'user' else 'text'
        context_list.append({
            'role': role,
            'content': [{
                'type': content_type,
                'text': text
            }]
        })

    if not context_list:
        return {}
    return {'context': context_list}


# Real-time speech recognition callback
class MyRecognitionCallback(RecognitionCallback):
    def on_open(self) -> None:
        print('RecognitionCallback open.')

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if not sentence or 'text' not in sentence:
            return
        if RecognitionResult.is_sentence_end(sentence):
            print('RecognitionCallback sentence end, text: ', sentence['text'])
        else:
            # partial recognition result
            print('RecognitionCallback text: ', sentence['text'])

    def on_complete(self) -> None:
        print('RecognitionCallback completed.')

    def on_error(self, result: RecognitionResult) -> None:
        print('RecognitionCallback error: ', result.message)

    def on_close(self) -> None:
        print('RecognitionCallback closed.')


def recognize_speech_with_context(audio_path, conversation_history=None):
    '''
    Recognize a local audio file, optionally carrying a conversation context.
    '''
    context = build_context(conversation_history)
    if context:
        print('[context] {} message(s) sent to the service.'.format(
            len(context['context'])))
    else:
        print('[context] no context is sent.')

    recognition = Recognition(
        model=MODEL,
        format='wav',  # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr'
        sample_rate=16000,  # supported 8000、16000
        callback=MyRecognitionCallback())

    # the context is passed through `raw_input`.
    # it can also be passed to recognition.call(raw_input=context)
    recognition.start(raw_input=context if context else None)

    chunk_size = 3200
    with open(audio_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            recognition.send_audio_frame(chunk)
            time.sleep(0.05)  # simulate the real-time audio stream

    recognition.stop()
    print('[Metric] requestId: {}, first package delay ms: {}'.format(
        recognition.get_last_request_id(),
        recognition.get_first_package_delay()))


# main function
if __name__ == '__main__':
    init_dashscope_api_key()
    init_dashscope_endpoint()

    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '../../..', 'sample-data',
        'hello_world_male_16k_16bit_mono.wav')
    file_path = os.path.normpath(file_path)
    if not os.path.exists(file_path):
        print('audio file not found: {}'.format(file_path))
        sys.exit(1)

    # ---- Example 1 : baseline, recognize without any context ----
    print('\n=== Example 1: without context (baseline) ===')
    recognize_speech_with_context(file_path)

    # ---- Example 2 : dialog history as context ----
    # the user utterances and the assistant replies of the previous rounds.
    # note the order: the `user` message of one round comes before its
    # `assistant` message.
    print('\n=== Example 2: dialog history as context ===')
    dialog_history = [
        {
            'role': 'user',
            'text': '你好啊'
        },
        {
            'role': 'assistant',
            'text': '你好啊，我是通义千问，有什么可以帮助你的？'
        },
        {
            'role': 'user',
            'text': '帮我看看今天的会议纪要'
        },
        {
            'role': 'assistant',
            'text': '好的，今天的会议主要讨论了语音识别模型的迭代计划。'
        },
    ]
    recognize_speech_with_context(file_path, dialog_history)

    # ---- Example 3 : domain word list as context ----
    # besides the dialog history, a single `user` message can also carry a list
    # of domain terms. This is useful when there is no dialog history but the
    # audio contains many proper nouns.
    print('\n=== Example 3: domain word list as context ===')
    domain_terms = [
        {
            'role':
            'user',
            'text':
            '相关术语：语音实验室、通义千问、百炼平台、声音复刻、热词表、说话人分离'
        },
    ]
    recognize_speech_with_context(file_path, domain_terms)

    # ---- Example 4 : context exceeding the limits is trimmed ----
    # 7 user messages and a very long text are provided on purpose to show how
    # build_context() keeps the latest 5 messages per type and truncates the
    # text to 400 characters.
    print('\n=== Example 4: context exceeding the limits is trimmed ===')
    oversized_history = [{
        'role': 'user',
        'text': '第{}轮的历史内容'.format(i)
    } for i in range(1, 8)]
    oversized_history.append({
        'role': 'assistant',
        'text': '这是一段很长的回复。' * 60  # far beyond 400 characters
    })
    recognize_speech_with_context(file_path, oversized_history)
