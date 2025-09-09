[comment]: # (title and brief introduction of the sample)
## 语音合成实时LLM输出并播放（流式模式）

简体中文 | [English](./README_EN.md)

本示例展示了如何将大语言模型（LLM）生成的文本流合成为语音流，并且通过扬声器播放。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景 | 典型用法 | 使用说明 |
| ----- | ----- | ----- |
| **语音播报场景** | 信息播报 | *将大语言模型生成的新闻、概要等信息实时播报* |
| **电话呼叫中心场景** | 客服回复转语音 | *通过大语言模型生成客服回复并实时播报* |
| **数字人场景** | 新闻播报、数字人直播、在线教育、voice chat | *通过大语言模型驱动数字人播报新闻、虚拟数字人直播、在线教育、语言学习、语音聊天等场景* |

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情
| 推荐模型 | API详情 |
| --- | --- |
| **cosyvoice-v1** | [CosyVoice大模型语音合成API详情](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#915a935d871ak) |
| **cosyvoice-v2** | [CosyVoice大模型语音合成API详情](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#da9ae03e5ek7b) |
| **cosyvoice-v3** | [CosyVoice大模型语音合成API详情](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#95303fd00f0ge) |

注：⚠️ cosyvoice-v3系列模型开放邀测（所有人可见，申请使用），[申请](https://bailian.console.aliyun.com/?tab=model#/model-market/detail/group-cosyvoice?modelGroup=group-cosyvoice)通过后发放免费额度。

### :point_right: 预期结果

示例运行时，将会调用阿里云百炼平台大语言模型千问（qwen-plus）回答提问：“番茄炒鸡蛋怎么做？”，并使用 longhua_v2 音色，按照流式方式发送大模型回答的文本并合成，将音频按照流式方式下发并通过扬声器播放。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
