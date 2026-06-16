[comment]: # (title and brief introduction of the sample)
## 根据歌词生成音乐

简体中文 | [English](./README_EN.md)

本示例展示了如何传入自定义歌词，调用百聆音乐生成大模型（Fun-Music）根据歌词谱曲并演唱，最后将生成的音频保存为文件。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景 | 典型用法 | 使用说明 |
| ----- | ----- | ----- |
| **入门场景** | 根据自定义歌词生成音乐 | *提供自己编写的歌词，由AI谱曲并演唱* |
| **音乐创作场景** | 词曲创作辅助 | *已有歌词，快速生成Demo试听效果* |
| **个性化场景** | 定制歌曲 | *为特定场合（生日、纪念日等）创作专属歌曲* |

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

示例运行，将会根据提供的自定义歌词生成一首女声演唱的歌曲，并保存在 `result.mp3` 文件中。

### :point_right: 歌词规范

歌词可以使用以下结构标签来组织歌曲结构：

| 标签 | 说明 |
| --- | --- |
| `[intro]` | 前奏，引入氛围 |
| `[verse]` | 主歌，叙述故事 |
| `[chorus]` | 副歌，情感高潮 |
| `[bridge]` | 桥段，视角转换 |
| `[outro]` | 尾奏，渐弱收尾 |

### :point_right: 参数说明

- **lyrics**：自定义歌词内容。支持中文或英文，需遵循原创性原则和内容安全要求。
- **gender**：演唱者性别，可选 `male`（男声）或 `female`（女声）。
- **model**：音乐生成模型，可选 `fun-music-v1` 或 `fun-music-preview`。

**注意**：`lyrics` 和 `prompt` 参数必须至少提供一个，不可同时为空。当同时传入两个参数时，仅 `lyrics` 生效，`prompt` 将被忽略。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
