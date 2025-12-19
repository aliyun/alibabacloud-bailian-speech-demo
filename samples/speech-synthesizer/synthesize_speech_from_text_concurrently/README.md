[comment]: # (title and brief introduction of the sample)

简体中文 | [English](./README_EN.md)

## 并发调用语音合成
本示例展示了如何并发合成多个文本的语音，并将语音保存为单独的文件。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景 | 典型用法 | 使用说明 |
| ----- | ----- | ----- |
| **入门场景**| 并发调用语音合成	 | *并发地将文本合成为语音*  |

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
| **cosyvoice-v3-flash** | [CosyVoice大模型语音合成API详情](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#95303fd00f0ge) |
| **cosyvoice-v3-plus** | [CosyVoice大模型语音合成API详情](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#95303fd00f0ge) |


### :point_right: 预期结果

示例运行时，将使用三种不同的音色并发合成 “我是<音色名>，欢迎体验阿里云百炼大模型语音合成服务！” 并保存在 `results/result_v<音色名>_p<线程号>.mp3` 文件中。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
