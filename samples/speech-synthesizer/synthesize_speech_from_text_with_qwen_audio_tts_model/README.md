[comment]: # (title and brief introduction of the sample)
## Qwen-Audio-3.0-TTS 指令控制语音合成

简体中文 | [English](./README_EN.md)

本示例展示了如何使用 Qwen-Audio-3.0-TTS 模型进行语音合成，包括：

1. **默认风格合成** — 使用音色原生风格将文本转为语音
2. **指令控制风格** — 通过自然语言指令（instruction）描述期望的说话风格、语速、语调等
3. **方言指令** — 通过指令将文本以指定方言朗读（如河南话、粤语等）
4. **情感与富语言标签** — 在文本中嵌入 `[excited]`、`[laughing]` 等标签控制情感和拟声效果

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景 | 典型用法 | 使用说明 |
| ----- | ----- | ----- |
| **电话呼叫中心场景** | 客服回复转语音 | *使用文字转语音对客服机器人回复进行实时语音播报* |
| **数字人场景** | 新闻播报 / 有声读物 | *通过指令控制情感、语速，使播报更自然* |
| **方言场景** | 方言配音 / 地方性内容 | *通过 instruction 指定方言进行合成* |
| **情感交互场景** | 游戏 / 教育 / 陪伴 | *使用情感标签使语音富有表现力* |

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情
| 推荐模型 | API详情 |
| --- | --- |
| **Qwen-Audio-3.0-TTS** | [官方文档](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime) |

### :point_right: 预期结果

示例运行时会依次执行 4 个场景：

1. **默认风格** — 使用 longanfengyue 音色合成文本并播放，输出 `result_default.mp3`
2. **风格指令** — 通过 instruction 控制为"年轻活泼的女性声音"风格合成，输出 `result_instruction_style.mp3`
3. **方言指令** — 通过 instruction 以河南话合成同一段文本，输出 `result_instruction_dialect.mp3`
4. **情感标签** — 使用 `[excited]` 和 `[laughing]` 标签合成带情感的语音，输出 `result_emotion_tags.mp3`

每个场景的音频都会流式播放并同时保存到对应的 mp3 文件。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../docs/image/group.png" width="400"/>
