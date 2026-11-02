#!/usr/bin/env python3
# Copyright (C) Alibaba Group. All Rights Reserved.
# MIT License (https://opensource.org/licenses/MIT)

"""
Qwen-Audio-3.1-TTS Instruction-Controlled Speech Synthesis Demo

This demo showcases the full range of instruction control capabilities
supported by the Qwen-Audio-3.1-TTS model:

  1. Style instruction   — describe the desired voice persona (tone, speed, emotion)
  2. Dialect instruction — synthesize in a specific Chinese dialect
  3. Emotion tags        — embed [tag] in text to control emotion for following text
  4. Rich-language tags  — embed [tag] in text to insert sound effects at that position
  5. Combined usage      — mix instruction + emotion tags for advanced expressiveness

For the full list of supported tags, see:
  https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9
"""

import os
import sys
import threading

from dashscope import Client

sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../../utils/python'))

from RealtimeMp3Player import RealtimeMp3Player

# ===========================================================================
# Configuration
# ===========================================================================
# Supported models: 'qwen-audio-3.1-tts-flash', 'qwen-audio-3.1-tts-plus'
MODEL = 'qwen-audio-3.1-tts-flash'
DEFAULT_VOICE = 'longanfengyue_v3.1'


def get_api_key():
    '''
    Set your DashScope API-key. More information:
    https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
    '''
    if 'DASHSCOPE_API_KEY' in os.environ:
        return os.environ['DASHSCOPE_API_KEY']
    else:
        return '<your-dashscope-api-key>'


def synthesize(text: str,
               instruction: str = None,
               voice: str = DEFAULT_VOICE,
               model: str = MODEL,
               output_file: str = None):
    """Synthesize speech and play via speaker. Optionally save to file."""
    player = RealtimeMp3Player()
    player.start()

    complete_event = threading.Event()
    parameters = {}
    if instruction is not None:
        parameters['instruction'] = instruction

    with open(output_file, 'wb') as audio_file:
        with Client(api_key=get_api_key()) as client:
            with client.audio.tts.connect(
                    model=model,
                    voice=voice,
                    format='mp3',
                    parameters=parameters if parameters else None) as session:

                def read_audio():
                    for chunk in session.audio_chunks():
                        player.write(chunk)
                        audio_file.write(chunk)
                    complete_event.set()

                reader_thread = threading.Thread(target=read_audio)
                reader_thread.start()

                session.send_text(text)
                session.stop()
                complete_event.wait()
                reader_thread.join()

                request_id = session.session.request_id
                first_package_delay = session.first_package_delay

    player.stop()

    print(f'  requestId: {request_id}, '
          f'first_package_delay: {first_package_delay:.0f}ms')
    if output_file:
        print(f'  saved to: {output_file}')


# ===========================================================================
# Instruction Examples
# ===========================================================================

# --- Style Instructions ---
# Describe the desired persona, tone, speed, emotion in natural language.
STYLE_INSTRUCTIONS = [
    {
        'name': '时尚产品主播',
        'instruction': '年轻活泼的女性声音，声音清脆甜美，语速很快，带有明显的上扬语调，适合介绍时尚产品',
        'text': '这款新出的口红颜色真的太好看了！姐妹们赶紧冲！',
    },
    {
        'name': '新闻播音员',
        'instruction': '沉稳专业的男性播音员声音，语速适中，字正腔圆，适合新闻播报',
        'text': '今天的天气真不错！我们一起出去玩吧！',
    },
    {
        'name': '温柔讲故事',
        'instruction': '温柔舒缓的女性声音，语速较慢，声音轻柔，适合睡前故事',
        'text': '在很久很久以前，有一座美丽的小村庄，村庄里住着一只可爱的小兔子。',
    },
]

# --- Dialect Instructions ---
# Simply tell the model which dialect to use.
DIALECT_INSTRUCTIONS = [
    {
        'name': '河南话',
        'instruction': '请用河南话表达',
        'text': '今天的天气真不错！我们一起出去玩吧！',
    },
    {
        'name': '粤语',
        'instruction': '请用粤语表达',
        'text': '今天的天气真不错！我们一起出去玩吧！',
    },
    {
        'name': '四川话',
        'instruction': '请用四川话表达',
        'text': '今天的天气真不错！我们一起出去玩吧！',
    },
]

# --- Emotion Control Tags (embedded in text) ---
# Control tags: set emotion for all following text until the next control tag.
# Rich-language tags: insert a sound effect at that exact position.
EMOTION_TAG_EXAMPLES = [
    {
        'name': '兴奋 + 笑声',
        'text': '[excited]今天的天气真不错！[laughing]我们一起出去玩吧！',
        'note': '[excited]=控制标签(后续文本带兴奋情感), [laughing]=富语言标签(插入笑声)',
    },
    {
        'name': '严肃 → 兴奋切换',
        'text': '[serious]请注意安全事项。[excited]好了，现在让我们开始吧！',
        'note': '同一段文本中切换不同情感',
    },
    {
        'name': '悲伤 + 叹息',
        'text': '[sad]他离开了这座城市，再也没有回来。[sighing]也许这就是命运吧。',
        'note': '[sad]=悲伤情感, [sighing]=插入叹息声',
    },
    {
        'name': '耳语 ASMR',
        'text': '[asmr]现在请闭上眼睛，深呼吸，感受这一刻的宁静。',
        'note': '[asmr]=ASMR轻柔耳语风格',
    },
]

# --- Combined: instruction + emotion tags ---
COMBINED_EXAMPLE = {
    'name': '指令 + 情感标签组合',
    'instruction': '温柔舒缓的女性声音，语速较慢',
    'text': '[whispers]听好了，[excited]惊喜来了！[laughing]生日快乐！',
    'note': 'instruction 设定基础音色风格，标签在此基础上叠加情感变化',
}


def main():
    # ----- Section 1: Style Instructions -----
    print('=' * 60)
    print(' Section 1: Style Instructions (风格指令)')
    print(' Describe the desired voice persona in natural language.')
    print('=' * 60)
    for i, ex in enumerate(STYLE_INSTRUCTIONS, 1):
        print(f'\n[1-{i}] {ex["name"]}')
        print(f'  instruction: {ex["instruction"]}')
        print(f'  text: {ex["text"]}')
        synthesize(text=ex['text'],
                   instruction=ex['instruction'],
                   output_file=f'result_style_{i}.mp3')

    # ----- Section 2: Dialect Instructions -----
    print('\n' + '=' * 60)
    print(' Section 2: Dialect Instructions (方言指令)')
    print(' Tell the model which dialect to speak.')
    print('=' * 60)
    for i, ex in enumerate(DIALECT_INSTRUCTIONS, 1):
        print(f'\n[2-{i}] {ex["name"]}')
        print(f'  instruction: {ex["instruction"]}')
        print(f'  text: {ex["text"]}')
        synthesize(text=ex['text'],
                   instruction=ex['instruction'],
                   output_file=f'result_dialect_{i}.mp3')

    # ----- Section 3: Emotion & Rich-Language Tags -----
    print('\n' + '=' * 60)
    print(' Section 3: Emotion & Rich-Language Tags (情感与富语言标签)')
    print(' Embed [tag] directly in text. No instruction needed.')
    print('=' * 60)
    for i, ex in enumerate(EMOTION_TAG_EXAMPLES, 1):
        print(f'\n[3-{i}] {ex["name"]}')
        print(f'  text: {ex["text"]}')
        print(f'  note: {ex["note"]}')
        synthesize(text=ex['text'],
                   output_file=f'result_emotion_{i}.mp3')

    # ----- Section 4: Combined -----
    print('\n' + '=' * 60)
    print(' Section 4: Combined (指令 + 标签组合使用)')
    print('=' * 60)
    ex = COMBINED_EXAMPLE
    print(f'\n[4-1] {ex["name"]}')
    print(f'  instruction: {ex["instruction"]}')
    print(f'  text: {ex["text"]}')
    print(f'  note: {ex["note"]}')
    synthesize(text=ex['text'],
               instruction=ex['instruction'],
               output_file='result_combined.mp3')

    print('\n' + '=' * 60)
    print(' All done! Check the generated mp3 files.')
    print('=' * 60)


if __name__ == '__main__':
    main()
