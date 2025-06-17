[comment]: # (title and brief introduction of the sample)
## 语音合成并保存文件（简单模式）

简体中文 | [English](./README_EN.md)

本示例展示了如何合成指定文本的语音，并将语音保存为文件。语音合成**简单模式**将合成语音保存为文件，适合不需要实时播放的场景。如需实时播放，请参考[语音合成并播放（流式模式）](../synthesize_speech_from_text_by_streaming_mode/)。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景 | 典型用法 | 使用说明 |
| ----- | ----- | ----- |
| **入门场景** | 一句话合成 | *将一段文本转化为语音* |
| **视频配音场景** | 视频配音、新闻配音 | *通过语音合成播报视频中字幕等文本内容* |
| **有声读物场景** | 小说配音、绘本配音 | *通过多种音色对应不同角色，朗读小说、绘本等有声读物* |

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情
| 推荐模型 | API详情 |
| --- | --- |
| **cosyvoice-v1** | [CosyVoice大模型语音合成API详情](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#95303fd00f0ge) |
| **cosyvoice-v2** | [CosyVoice大模型语音合成API详情](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#da9ae03e5ek7b) |

### :point_right: 预期结果

示例运行，将会使用 longhua_v2 音色合成示例文本 “想不到时间过得这么快！昨天和你视频聊天，看到你那自豪又满意的笑容，我的心里呀，就如同喝了一瓶蜜一样甜呢！真心为你开心呢！” 保存在 `result.mp3` 文件中。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
