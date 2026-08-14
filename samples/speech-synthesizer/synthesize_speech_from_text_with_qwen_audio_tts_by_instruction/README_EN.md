[comment]: # (title and brief introduction of the sample)
## Qwen-Audio-3.0-TTS Instruction-Controlled Speech Synthesis (Detailed)

English | [简体中文](./README.md)

This example **specifically** demonstrates the **instruction control** capabilities of the Qwen-Audio-3.0-TTS model, covering four categories:

### 1. Style Instruction

Pass a natural-language description via the `instruction` parameter to control **persona, speed, tone, and emotional baseline**.

```python
instruction = '年轻活泼的女性声音，声音清脆甜美，语速很快，带有明显的上扬语调，适合介绍时尚产品'
synthesizer = SpeechSynthesizer(model=model, voice=voice, instruction=instruction, callback=callback)
```

### 2. Dialect Instruction

Use `instruction` to specify a dialect:

```python
instruction = '请用河南话表达'  # Henan dialect
```

Supports 30+ Chinese dialects including Cantonese, Sichuan, Wu, Hokkien, etc.

### 3. Emotion & Rich-Language Tags

Embed tags directly in the **text** parameter (no `instruction` needed):

- **Control tags** (e.g. `[excited]`, `[sad]`) — set emotion for all following text
- **Rich-language tags** (e.g. `[laughing]`, `[sighing]`) — insert sound effects at that position

### 4. Combined Usage

Set a base persona via `instruction`, then overlay emotion shifts via inline tags.

---

### :point_right: Programming Languages
- [Python](./python)

### :point_right: Reference
| Model | Documentation |
| --- | --- |
| **Qwen-Audio-3.0-TTS** (`qwen-audio-3.0-tts-flash` / `qwen-audio-3.0-tts-plus`) | [Realtime TTS Guide](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide) |

### :point_right: Expected Results

Running `python run.py` executes 4 sections with **11 synthesis scenarios**, each playing audio in real-time and saving an mp3 file.

### :point_right: Technical Support
<img src="../../../docs/image/group.png" width="400"/>
