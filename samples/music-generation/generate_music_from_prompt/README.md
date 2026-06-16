[comment]: # (title and brief introduction of the sample)
## 根据提示词生成音乐

简体中文 | [English](./README_EN.md)

本示例展示了如何通过提示词（prompt）描述音乐风格和场景，调用百聆音乐生成大模型（Fun-Music）自动生成歌词并生成完整歌曲，最后将生成的音频保存为文件。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景 | 典型用法 | 使用说明 |
| ----- | ----- | ----- |
| **入门场景** | 根据描述生成音乐 | *输入一段对音乐风格、情绪、场景的描述，自动生成并演唱歌曲* |
| **视频配乐场景** | Vlog/短视频背景音乐 | *根据视频主题和情绪生成匹配的背景音乐* |
| **创意辅助场景** | 音乐创作灵感 | *通过AI快速生成Demo，获取创作灵感* |

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情
| 推荐模型 | API详情 |
| --- | --- |
| **fun-music-v1** | [Fun-Music音乐生成API详情](https://help.aliyun.com/zh/model-studio/fun-music) |
| **fun-music-preview** | [Fun-Music音乐生成API详情](https://help.aliyun.com/zh/model-studio/fun-music) |

### :point_right: 预期结果

示例运行，将会根据提示词 "夏日清新民谣，木吉他与口琴伴奏，轻快节奏，适合旅行Vlog背景音乐" 生成一首女声演唱的歌曲，并保存在 `result.mp3` 文件中。

### :point_right: 参数说明

- **prompt**：描述音乐风格、场景、情绪的自然语言提示词。推荐具体描述，例如"悲伤钢琴曲，雨夜思念"，而非笼统的"悲伤音乐"。
- **gender**：演唱者性别，可选 `male`（男声）或 `female`（女声）。
- **model**：音乐生成模型，可选 `fun-music-v1` 或 `fun-music-preview`。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
