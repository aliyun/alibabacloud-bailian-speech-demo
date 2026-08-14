## Qwen-Audio-3.0-TTS Instruction-Controlled Speech Synthesis

English | [简体中文](./README.md)

This example demonstrates how to use the Qwen-Audio-3.0-TTS model for speech synthesis, covering:

1. **Default style** — synthesize with the voice's native style
2. **Style instruction** — control speaking persona, speed, and tone via a natural-language instruction
3. **Dialect instruction** — synthesize text in a specified dialect (e.g. Henan dialect, Cantonese)
4. **Emotion & rich-language tags** — embed tags like `[excited]`, `[laughing]` in text to control emotion and sound effects

### :point_right: Applicable Scenarios

| Application Scenario | Typical Use Case | Usage Description |
| ----- | ----- | ----- |
| **Call Center** | Agent Response to Speech | *Real-time voice announcements for customer service bots* |
| **Digital Human** | News / Audiobook | *Control emotion and speed via instruction for natural broadcasting* |
| **Dialect** | Regional content / dubbing | *Specify dialect via instruction* |
| **Emotional Interaction** | Gaming / Education / Companion | *Use emotion tags for expressive speech* |

### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

### :point_right: Reference Details
| Recommended Model | API Details |
| --- | --- |
| **Qwen-Audio-3.0-TTS** | [Official Documentation](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide) |

### :point_right: Expected Results

The example runs 4 scenarios in sequence:

1. **Default style** — synthesizes with longanfengyue voice, outputs `result_default.mp3`
2. **Style instruction** — "young, lively female voice" style, outputs `result_instruction_style.mp3`
3. **Dialect instruction** — synthesizes in Henan dialect, outputs `result_instruction_dialect.mp3`
4. **Emotion tags** — uses `[excited]` and `[laughing]` tags, outputs `result_emotion_tags.mp3`

Each scenario streams audio to the speaker and saves the corresponding mp3 file.

### :point_right: Technical Support
<img src="../../../docs/image/group.png" width="400"/>
