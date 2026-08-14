[comment]: # (title and brief introduction of the sample)
## Qwen-Audio-3.0-TTS 指令控制语音合成详解

简体中文 | [English](./README_EN.md)

本示例**专门**演示 Qwen-Audio-3.0-TTS 的 **instruction 指令控制** 能力，覆盖以下四类用法：

### 一、风格指令（Style Instruction）

通过 `instruction` 参数传入一段自然语言描述，控制语音的**人设、语速、语调、情感基调**。模型会据此调整合成效果。

```python
instruction = '年轻活泼的女性声音，声音清脆甜美，语速很快，带有明显的上扬语调，适合介绍时尚产品'
synthesizer = SpeechSynthesizer(model=model, voice=voice, instruction=instruction, callback=callback)
```

示例中提供了 3 种风格对比：时尚产品主播、新闻播音员、温柔讲故事。

### 二、方言指令（Dialect Instruction）

同样使用 `instruction` 参数，直接告诉模型用哪种方言，如：

```python
instruction = '请用河南话表达'
```

支持的方言包括：河南话、粤语、四川话、吴语、闽南语等 30+ 方言，详见[API 文档](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)。

### 三、情感与富语言标签（Emotion & Rich-Language Tags）

在**待合成文本**中直接嵌入标签，**不需要设置 instruction 参数**。

#### 控制类标签（设定后续文本的情感）

| 标签 | 说明 | 标签 | 说明 |
| --- | --- | --- | --- |
| `[excited]` | 兴奋 | `[sad]` | 悲伤 |
| `[angry]` | 愤怒 | `[serious]` | 严肃 |
| `[whispers]` | 耳语 | `[asmr]` | ASMR 轻柔 |
| `[shouting]` | 大喊 | `[panicked]` | 恐慌 |
| `[bored]` | 无聊 | `[tired]` | 疲惫 |
| `[curious]` | 好奇 | `[sarcastic]` | 讽刺 |
| `[very slowly]` | 极慢语速 | `[very fast]` | 极快语速 |

#### 富语言类标签（在当前位置插入拟声效果）

| 标签 | 说明 | 标签 | 说明 |
| --- | --- | --- | --- |
| `[laughing]` | 大笑 | `[giggles]` | 咯咯笑 |
| `[sighing]` | 叹息 | `[gasp]` | 倒吸气 |
| `[cough]` | 咳嗽 | `[clears throat]` | 清嗓 |
| `[snorts]` | 哼声 | | |

使用示例：
```python
text = '[excited]今天的天气真不错！[laughing]我们一起出去玩吧！'
synthesizer.call(text)
```

### 四、组合使用（Instruction + Tags）

`instruction` 设定基础人设风格，文本中的标签在此基础上叠加情感变化：

```python
instruction = '温柔舒缓的女性声音，语速较慢'
text = '[whispers]听好了，[excited]惊喜来了！[laughing]生日快乐！'
```

---

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情
| 推荐模型 | API 文档 |
| --- | --- |
| **Qwen-Audio-3.0-TTS** (`qwen-audio-3.0-tts-flash` / `qwen-audio-3.0-tts-plus`) | [实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide) |

### :point_right: 预期结果

运行 `python run.py` 后会依次执行 4 个章节共 **11 个**合成场景，每个场景实时播放并保存对应的 mp3 文件：

| 章节 | 输出文件 |
| --- | --- |
| 风格指令 ×3 | `result_style_1.mp3` ~ `result_style_3.mp3` |
| 方言指令 ×3 | `result_dialect_1.mp3` ~ `result_dialect_3.mp3` |
| 情感标签 ×4 | `result_emotion_1.mp3` ~ `result_emotion_4.mp3` |
| 组合使用 ×1 | `result_combined.mp3` |

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../docs/image/group.png" width="400"/>
