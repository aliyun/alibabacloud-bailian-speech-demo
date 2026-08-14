#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)
"""
Qwen-Audio-3.0-TTS All-in-One Multilingual Speech Synthesis Demo

The `longanhuan_mtlv7` voice is an *all-in-one* multilingual voice: one single
voice id speaks 16 languages, so you do not have to switch voices — and the
speaker timbre stays recognizably the same across all of them. This is what
makes it suitable for one brand voice serving a global audience.

Two parameters drive the language selection:

  language_hints=[lid]   tells the model which language the input text is in
  instruction='请讲日语。'  explicitly asks the model to speak that language

Chinese and English need `language_hints` only. Every other language also needs
the matching `instruction`, otherwise the model may fall back to reading the
text with Chinese or English pronunciation.

By default this demo walks through all 16 languages with the same greeting so
you can hear one voice switch languages back to back. Use the command line
options to synthesize your own text in a single language instead.
"""

import argparse
import os
import sys
import threading

import dashscope
from dashscope.audio.tts_v2 import ResultCallback, SpeechSynthesizer

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../../utils/python'))

from RealtimeMp3Player import RealtimeMp3Player

# ===========================================================================
# Configuration
# ===========================================================================
# Supported models: 'qwen-audio-3.0-tts-flash', 'qwen-audio-3.0-tts-plus'
MODEL = 'qwen-audio-3.0-tts-flash'

# The all-in-one multilingual voice: one voice id, 16 languages.
VOICE = 'longanhuan_mtlv7'

# The 16 supported languages. `instruction` is None for Chinese and English,
# because those two are recognized from `language_hints` alone. For every other
# language the instruction has to be sent as well.
LANGUAGES = [
    {
        'lid': 'zh',
        'name': '中文',
        'instruction': None,
        'text': '你好，欢迎使用阿里云百炼语音合成服务。',
    },
    {
        'lid': 'en',
        'name': '英语 English',
        'instruction': None,
        'text': 'Hello, welcome to the Alibaba Cloud Model Studio '
                'speech synthesis service.',
    },
    {
        'lid': 'ja',
        'name': '日语 日本語',
        'instruction': '请讲日语。',
        'text': 'こんにちは、アリババクラウドの音声合成サービスへようこそ。',
    },
    {
        'lid': 'ko',
        'name': '韩语 한국어',
        'instruction': '请讲韩语。',
        'text': '안녕하세요, 알리바바 클라우드 음성 합성 서비스에 오신 것을 '
                '환영합니다.',
    },
    {
        'lid': 'fr',
        'name': '法语 Français',
        'instruction': '请讲法语。',
        'text': 'Bonjour, bienvenue au service de synthèse vocale '
                "d'Alibaba Cloud.",
    },
    {
        'lid': 'de',
        'name': '德语 Deutsch',
        'instruction': '请讲德语。',
        'text': 'Hallo, willkommen beim Sprachsynthese-Service von '
                'Alibaba Cloud.',
    },
    {
        'lid': 'ru',
        'name': '俄语 Русский',
        'instruction': '请讲俄语。',
        'text': 'Здравствуйте, добро пожаловать в сервис синтеза речи '
                'Alibaba Cloud.',
    },
    {
        'lid': 'it',
        'name': '意大利语 Italiano',
        'instruction': '请讲意大利语。',
        'text': 'Ciao, benvenuto al servizio di sintesi vocale di '
                'Alibaba Cloud.',
    },
    {
        'lid': 'es',
        'name': '西班牙语 Español',
        'instruction': '请讲西班牙语。',
        'text': 'Hola, bienvenido al servicio de síntesis de voz de '
                'Alibaba Cloud.',
    },
    {
        'lid': 'pt',
        'name': '葡萄牙语 Português',
        'instruction': '请讲葡萄牙语。',
        'text': 'Olá, bem-vindo ao serviço de síntese de voz da '
                'Alibaba Cloud.',
    },
    {
        'lid': 'ar',
        'name': '阿拉伯语 العربية',
        'instruction': '请讲阿拉伯语。',
        'text': 'مرحبًا، أهلاً بك في خدمة تحويل النص إلى كلام من علي بابا كلاود.',
    },
    {
        'lid': 'th',
        'name': '泰语 ไทย',
        'instruction': '请讲泰语。',
        'text': 'สวัสดีค่ะ ยินดีต้อนรับสู่บริการสังเคราะห์เสียงของอาลีบาบาคลาวด์',
    },
    {
        'lid': 'vi',
        'name': '越南语 Tiếng Việt',
        'instruction': '请讲越南语。',
        'text': 'Xin chào, chào mừng bạn đến với dịch vụ tổng hợp giọng nói '
                'của Alibaba Cloud.',
    },
    {
        'lid': 'id',
        'name': '印尼语 Bahasa Indonesia',
        'instruction': '请讲印尼语。',
        'text': 'Halo, selamat datang di layanan sintesis suara Alibaba Cloud.',
    },
    {
        'lid': 'ms',
        'name': '马来语 Bahasa Melayu',
        'instruction': '请讲马来语。',
        'text': 'Helo, selamat datang ke perkhidmatan sintesis pertuturan '
                'Alibaba Cloud.',
    },
    {
        'lid': 'tl',
        'name': '菲律宾语 Filipino',
        'instruction': '请讲菲律宾语。',
        'text': 'Kumusta, maligayang pagdating sa serbisyo ng speech '
                'synthesis ng Alibaba Cloud.',
    },
]

LANGUAGE_MAP = {item['lid']: item for item in LANGUAGES}


def init_dashscope_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ['DASHSCOPE_API_KEY']
    else:
        dashscope.api_key = '<your-dashscope-api-key>'


class SpeechSynthesisCallback(ResultCallback):
    """Callback that plays audio in real-time and optionally saves to file."""

    def __init__(self, player: RealtimeMp3Player, output_file: str = None):
        self.player = player
        self.output_file = output_file
        self.file = None
        self.complete_event = threading.Event()

    def on_open(self):
        if self.output_file:
            self.file = open(self.output_file, 'wb')

    def on_complete(self):
        self.complete_event.set()

    def on_error(self, message: str):
        print(f'  [ERROR] {message}')
        self.complete_event.set()

    def on_close(self):
        if self.file:
            self.file.close()

    def on_event(self, message):
        pass

    def on_data(self, data: bytes) -> None:
        self.player.write(data)
        if self.file:
            self.file.write(data)

    def wait_for_complete(self):
        self.complete_event.wait()


def synthesize(text: str,
               lid: str,
               instruction: str = None,
               output_file: str = None):
    """Synthesize one sentence in the given language and play it."""
    player = RealtimeMp3Player()
    player.start()

    callback = SpeechSynthesisCallback(player, output_file)

    # `instruction` is only sent for languages that need it. Passing None is
    # also accepted by the SDK, but keeping it out of the call makes it obvious
    # which languages rely on the instruction and which do not.
    kwargs = {
        'model': MODEL,
        'voice': VOICE,
        'language_hints': [lid],
        'callback': callback,
    }
    if instruction is not None:
        kwargs['instruction'] = instruction

    synthesizer = SpeechSynthesizer(**kwargs)
    synthesizer.call(text)
    callback.wait_for_complete()
    player.stop()

    print(f'  requestId: {synthesizer.get_last_request_id()}, '
          f'first_package_delay: {synthesizer.get_first_package_delay():.0f}ms')
    if output_file:
        print(f'  saved to: {output_file}')


def run_all_languages():
    """Walk through all 16 languages using the same greeting."""
    print('=' * 70)
    print(f' All-in-One 多语言语音合成：单一音色 {VOICE} 连说 '
          f'{len(LANGUAGES)} 种语言')
    print(' 请留意切换语种时，说话人的音色始终保持一致。')
    print('=' * 70)

    for i, item in enumerate(LANGUAGES, 1):
        output_file = f'result_{item["lid"]}.mp3'
        print(f'\n[{i}/{len(LANGUAGES)}] {item["name"]} ({item["lid"]})')
        print(f'  instruction: {item["instruction"]}')
        print(f'  text: {item["text"]}')
        synthesize(text=item['text'],
                   lid=item['lid'],
                   instruction=item['instruction'],
                   output_file=output_file)

    print('\n' + '=' * 70)
    print(' 全部完成，生成的 mp3 文件可用于对比同一音色在各语种下的表现。')
    print('=' * 70)


def run_single(lid: str, text: str, output_file: str):
    """Synthesize custom text in a single language."""
    item = LANGUAGE_MAP[lid]
    instruction = item['instruction']

    print(f'language : {item["name"]} ({lid})')
    print(f'voice    : {VOICE}')
    print(f'instruction: {instruction}')
    print(f'text     : {text}')
    synthesize(text=text,
               lid=lid,
               instruction=instruction,
               output_file=output_file)


def main():
    parser = argparse.ArgumentParser(
        description='All-in-one multilingual speech synthesis with the '
                    f'{VOICE} voice.')
    parser.add_argument(
        '-l',
        '--lid',
        choices=sorted(LANGUAGE_MAP.keys()),
        help='language id. When omitted, all 16 languages are demonstrated.')
    parser.add_argument(
        '-t',
        '--text',
        help='text to synthesize. Defaults to the built-in greeting of the '
             'selected language.')
    parser.add_argument('-o',
                        '--output',
                        help='path of the mp3 file to save.')
    args = parser.parse_args()

    if args.text is not None and args.lid is None:
        parser.error('--text requires --lid, so that the model knows which '
                     'language the text is in.')

    init_dashscope_api_key()

    if args.lid is None:
        run_all_languages()
        return

    text = args.text if args.text is not None else LANGUAGE_MAP[
        args.lid]['text']
    output_file = args.output if args.output else f'result_{args.lid}.mp3'

    if os.path.dirname(output_file):
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

    run_single(args.lid, text, output_file)


if __name__ == '__main__':
    main()
