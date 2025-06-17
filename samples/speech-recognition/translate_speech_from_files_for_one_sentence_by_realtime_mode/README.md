[comment]: # (title and brief introduction of the sample)
## 批量音频文件一句话语音识别和翻译（实时模式）

简体中文 | [English](./README_EN.md)

本示例展示了如何批量的调用一句话语音翻译接口，实现多个文件流的输入，并实时返回多个文件对应的识别结果。

音频文件一句话语音识别和翻译的**实时模式**更适合对本地文件进行处理且即时返回结果，或搭建处理流式音频的服务端，收集前端的音频流，即时返回识别结果的场景。

如果您使用Java搭建语音服务，请参考[高并发示例文档](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-in-high-concurrency-scenarios)获得最佳的性能。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景     | 典型用法 | 使用说明 |
|----------| ----- | ----- |
| **入门场景** | 麦克风语音翻译 | *实时从麦克风录音并进行语音翻译* |
| **实时双语字幕** | 自动生成音视频不同语言字幕 | *实时对视频流进行语音识别和翻译，生成双语字幕* |
| **会议语音分析理解场景** | 实时会议语音识别	 | *实时对会议语音进行语音识别并翻译* |

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情

| 推荐模型 | API详情 |
| ----- | ----- |
| **gummy-chat-v1** | [Paraformer实时语音识别API详情（TODO：更新）](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-real-time-speech-recognition-api) |


### :point_right: 预期结果

运行示例，在控制台会输出流式识别结果。每个文件的识别对应一个[process id], 每个文件的结果会不断返回增量的结果。如
```
translation with file :asr_example_chat.wav
[process 92485] TranslationRecognizerCallback open.
translation with file :asr_example_chat.wav
[process 92483] TranslationRecognizerCallback open.
[process 92483] Transcript ==>  hello,word这里是阿里巴巴语音实验室。
[process 92483] Translate ==>  Hello world, this is the Alibaba Speech Lab.
[process 92483] Translation completed
[process 92485] Transcript ==>  hello,word,这里是阿里巴巴语音实验室。
[process 92485] Translate ==>  Hello, world. This is the Alibaba Speech Lab.
[process 92485] Translation completed
[process 92483] TranslationRecognizerCallback close.
[Metric] requestId: xxxxxxxx, first package delay ms: 444.7109375, last package delay ms: 665.9140625
[process 92485] TranslationRecognizerCallback close.
[Metric] requestId: xxxxxxxx, first package delay ms: 626.47509765625, last package delay ms: 963.182861328125
```

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
