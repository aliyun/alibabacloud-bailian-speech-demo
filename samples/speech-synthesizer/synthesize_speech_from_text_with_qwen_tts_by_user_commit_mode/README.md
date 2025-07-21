[comment]: # (title and brief introduction of the sample)
## 语音合成并播放（commit模式）

简体中文 | [English](./README_EN.md)

本示例展示了如何合成指定文本的语音，流式获取返回音频并实时播放。本示例同时展示了如何在流式回调中保存音频到文件。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景 | 典型用法 | 使用说明 |
| ----- | ----- | ----- |
| **电话呼叫中心场景** | 客服回复转语音 | *使用文字转语音对客服机器人回复进行实时语音播报* |
| **数字人场景** | 新闻播报 | *新闻等场景，通过语音合成进行文本信息的播报* |

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情
| 推荐模型 | API详情 |
| --- | --- |
| **qwen-tts-realtime** | [官方文档](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime) |

### :point_right: 预期结果

示例运行时，将会使用 Chelsie 音色合成示例文本流，合成音频将按照流式方式下发，通过扬声器播放。

在合成流式文本时，使用`commit`模式，用户主动控制输入缓存提交的模式，适合高级用户或延迟要求极高的系统使用，但需自行控制句子完整性与合成点，可能影响合成质量。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
