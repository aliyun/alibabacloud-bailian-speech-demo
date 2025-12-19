[comment]: # (title and brief introduction of the sample)
## 语音合成异步IO（流式模式）

简体中文 | [English](./README_EN.md)

本示例展示了如何合成指定文本的语音，在流式回调中保存音频到文件，并且在协程中异步等待合成结束。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

本示例旨在演示如何利用Python的协程库 `asyncio`异步等待语音合成结束，并且避免阻塞当前协程的EventLoop。适用于在异步I/O程序或系统下调用CosyVoice大模型语音合成的场景。

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情
| 推荐模型 | API详情 |
| --- | --- |
| **cosyvoice-v1** | [CosyVoice大模型语音合成API详情](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#95303fd00f0ge) |
| **cosyvoice-v2** | [CosyVoice大模型语音合成API详情](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#da9ae03e5ek7b) |
| **cosyvoice-v3-flash** | [CosyVoice大模型语音合成API详情](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#95303fd00f0ge) |
| **cosyvoice-v3-plus** | [CosyVoice大模型语音合成API详情](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#95303fd00f0ge) |


### :point_right: 预期结果

示例运行时，将会使用 longanhuan 音色合成示例文本 “想不到时间过得这么快！昨天和你视频聊天，看到你那自豪又满意的笑容，我的心里呀，就如同喝了一瓶蜜一样甜呢！真心为你开心呢！” ，合成音频将按照流式方式下发，并保存到文件`result.mp3`中。

### :point_right: 异步调用说明

在本示例中，首先通过`async_streaming_complete`函数发送TTS结束信号，之后利用线程安全的 `ThreadSafeAsyncioEvent` 异步的等待合成任务结束。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
