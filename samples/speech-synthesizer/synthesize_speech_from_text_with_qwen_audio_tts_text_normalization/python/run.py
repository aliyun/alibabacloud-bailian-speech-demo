#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)
"""
Qwen-Audio-3.0-TTS Text Normalization (TN) Demo

Text Normalization is the step that turns "written form" into "spoken form"
before acoustic synthesis: digits, units, symbols and abbreviations all have to
be expanded into the words a human would actually say. It is one of the most
common sources of audible errors in speech synthesis, e.g.

  "20%"      read as "twenty percent-sign"   instead of "twenty percent"
  "4~30"     read as "four tilde thirty"     instead of "four to thirty"
  "965113"   read as one huge cardinal number instead of digit by digit

This demo feeds Qwen-Audio-3.0-TTS three deliberately hard Chinese passages that are
dense with quantities, units, symbols, hotline numbers and polyphonic
characters, then prints the expected spoken form of each tricky span so that you
can compare it against what you hear.

Note: whether every span is rendered correctly can only be judged by listening.
The checkpoints below tell you exactly what to listen for.
"""

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
VOICE = 'longanfengyue'


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
    """Callback that plays audio in real-time and saves it to a file."""

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


def synthesize(text: str, output_file: str):
    """Synthesize speech, play it through the speaker and save it to a file."""
    player = RealtimeMp3Player()
    player.start()

    callback = SpeechSynthesisCallback(player, output_file)
    synthesizer = SpeechSynthesizer(model=MODEL, voice=VOICE, callback=callback)

    synthesizer.call(text)
    callback.wait_for_complete()
    player.stop()

    print(f'  requestId: {synthesizer.get_last_request_id()}, '
          f'first_package_delay: {synthesizer.get_first_package_delay():.0f}ms')
    print(f'  saved to: {output_file}')


# ===========================================================================
# Test Passages
# ===========================================================================
# Each case carries the raw text plus the spans that TN has to get right.
# 'checkpoints' maps the written form to the spoken form you should hear.
TN_CASES = [
    {
        'name': '古代官俸：数量词 + 生僻量词 + 多音字',
        'text': '正一品官，月领禄米150石，俸钱12万文，外加每年绫20匹，'
                '罗1匹，绵50两;从九品官，月禄米5石，俸钱8000文，加每年绵12两。',
        'checkpoints': [
            ('150石', '一百五十石(dàn) —— 作为容量单位读 dàn，不读 shí'),
            ('12万文', '十二万文 —— 万位要合并，不是"一二万"'),
            ('1匹', '一匹 —— 量词前的 1 读"一"，不读"幺"'),
            (';', '半角分号也要当作句中停顿处理'),
            ('8000文', '八千文 —— 不读"八零零零"'),
        ],
    },
    {
        'name': '医药检测：百分号 + 波浪范围符 + 单位',
        'text': '在一次检测中，1毫升20%甘露醇药液中可查出粒径4～30微米的微粒598个。',
        'checkpoints': [
            ('20%', '百分之二十 —— 而不是"二十百分号"'),
            ('4～30微米', '四到三十微米 —— 全角波浪号读作"到"，不能读出符号名'),
            ('1毫升', '一毫升'),
            ('598个', '五百九十八个'),
        ],
    },
    {
        'name': '服务热线：号码逐位读 + 时间量',
        'text': '965113供水服务热线24小时受理用户来电、来访、报修、报漏、投诉，'
                '做到用户反映的问题件件有落实、件件有反馈。',
        'checkpoints': [
            ('965113', '九六五一一三 —— 电话号码要逐位读，'
                       '而不是"九十六万五千一百一十三"'),
            ('24小时', '二十四小时 —— 时间量要按基数词读'),
        ],
    },
]


def main():
    init_dashscope_api_key()

    print('=' * 70)
    print(' Qwen-Audio-3.0-TTS 文本正则化（TN）能力演示')
    print(' 以下 3 段文本密集包含数量词、单位、符号、号码与多音字，')
    print(' 请边听边对照每段列出的检查点。')
    print('=' * 70)

    for i, case in enumerate(TN_CASES, 1):
        output_file = f'result_tn_{i}.mp3'
        print(f'\n[{i}] {case["name"]}')
        print(f'  原文: {case["text"]}')
        print('  检查点（应当听到的读法）:')
        for written, spoken in case['checkpoints']:
            print(f'    - {written:<10} -> {spoken}')
        synthesize(case['text'], output_file)

    print('\n' + '=' * 70)
    print(' 全部完成，生成的 mp3 文件可反复回听比对。')
    print('=' * 70)


if __name__ == '__main__':
    main()
