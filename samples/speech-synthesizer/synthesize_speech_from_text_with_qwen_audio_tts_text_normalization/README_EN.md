[comment]: # (title and brief introduction of the sample)
## Qwen-Audio-3.0-TTS Text Normalization (TN) Showcase

[简体中文](./README.md) | English

**Text Normalization (TN)** is the stage where speech synthesis converts the *written form* into the *spoken form*. Digits, units, symbols and abbreviations all have to be expanded into the words a human would actually say before the acoustic model can pronounce them. It is the single most audible source of glitches in synthesized speech:

| Written form | Possible TN failure | Correct spoken form |
| --- | --- | --- |
| `20%` | twenty **percent-sign** | twenty percent (百分之二十) |
| `4～30` | four **tilde** thirty | four **to** thirty (四到三十) |
| `965113` | nine hundred sixty-five thousand ... | digit by digit (九六五一一三) |
| `150石` | 一百五十 **shí** | 一百五十 **dàn** |

This sample feeds Qwen-Audio-3.0-TTS three **deliberately difficult** Chinese passages, densely packed with quantities, rare measure words, polyphonic characters, percent signs, full-width tilde ranges, hotline numbers and time spans.

### :point_right: The three passages and what to listen for

#### 1. Ancient official salaries: quantities + rare measure words + polyphones

> 正一品官，月领禄米150石，俸钱12万文，外加每年绫20匹，罗1匹，绵50两;从九品官，月禄米5石，俸钱8000文，加每年绵12两。

| Written form | Expected reading |
| --- | --- |
| `150石` | 一百五十石 (**dàn**) — as a volume unit it is not read *shí* |
| `12万文` | 十二万文 — the 万 group must be merged |
| `1匹` | 一匹 — the digit 1 before a measure word reads 「一」, not 「幺」 |
| `;` | a half-width semicolon must still act as an in-sentence pause |
| `8000文` | 八千文 — not 「八零零零」 |

#### 2. Pharmaceutical inspection: percent sign + tilde range + units

> 在一次检测中，1毫升20%甘露醇药液中可查出粒径4～30微米的微粒598个。

| Written form | Expected reading |
| --- | --- |
| `20%` | 百分之二十 |
| `4～30微米` | 四**到**三十微米 — the full-width tilde reads as 「到」, never as the symbol name |
| `1毫升` | 一毫升 |
| `598个` | 五百九十八个 |

#### 3. Service hotline: digit-by-digit numbers + time spans

> 965113供水服务热线24小时受理用户来电、来访、报修、报漏、投诉，做到用户反映的问题件件有落实、件件有反馈。

| Written form | Expected reading |
| --- | --- |
| `965113` | 九六五一一三 — phone numbers are read **digit by digit** |
| `24小时` | 二十四小时 — time spans use cardinal numbers |

### :point_right: A note on how this can be verified

TN quality **can ultimately only be judged by ear**. Differences such as polyphone tones or digit grouping cannot be reliably recovered even by feeding the synthesized audio back into ASR — the recognizer's own inverse text normalization rewrites 「百分之二十」 back into `20%`, and tone differences never surface in text at all.

This sample therefore makes no automatic assertions. Instead it prints a **checkpoint list** for every passage so you can compare against what you hear while it plays.

> :bulb: In our own testing, a round trip through `paraformer-realtime-v2` did confirm that `4～30微米` is normalized to 「四到三十微米」 (recognized back as `4到30微米`). The first passage, however, uses classical Chinese vocabulary that ASR itself transcribes poorly, so it cannot be judged this way and has to be listened to directly.

---

[comment]: # (supported programming languages of the sample)
### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: Reference
| Recommended Model | API Documentation |
| --- | --- |
| **Qwen-Audio-3.0-TTS** (`qwen-audio-3.0-tts-flash` / `qwen-audio-3.0-tts-plus`) | [Realtime Speech Synthesis](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide) |

### :point_right: Expected Results

Running `python run.py` synthesizes the three passages in order. Each one is played back in real time, saved to its own mp3 file, and accompanied by its checkpoint list in the terminal:

| Passage | Output file |
| --- | --- |
| Ancient official salaries | `result_tn_1.mp3` |
| Pharmaceutical inspection | `result_tn_2.mp3` |
| Service hotline | `result_tn_3.mp3` |

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../docs/image/group.png" width="400"/>
