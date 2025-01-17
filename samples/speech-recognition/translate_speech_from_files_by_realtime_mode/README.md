[comment]: # (title and brief introduction of the sample)
## 批量音视频文件语音翻译（实时模式）
本示例展示了如何批量的调用实时语音翻译接口，实现多个文件流的输入，并实时返回多个文件对应的翻译结果。

音视频文件语音翻译的**实时模式**更适合对本地文件进行处理且即时返回结果，或搭建处理流式音频的服务端，收集前端的音频流，即时返回翻译结果的场景。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景     | 典型用法 | 使用说明 |
|----------| ----- | ----- |
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
| **gummy-realtime-v1** | [Paraformer实时语音识别API详情（TODO：更新）](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-real-time-speech-recognition-api) |


### :point_right: 预期结果

运行示例，在控制台会输出流式识别结果。每个文件的识别对应一个[process id], 每个文件的结果会不断返回增量的结果。如
```
translation with file :hello_world_male_16k_16bit_mono.wav
[process 94459] TranslationRecognizerCallback open.
translation with file :hello_world_male_16k_16bit_mono.wav
[process 94461] TranslationRecognizerCallback open.
[process 94459] Transcript ==>  hello ,word,这里是阿里巴巴语音实验室。
[process 94459] Translate ==>  Hello, world. This is Alibaba's voice lab.
[process 94459] Translation completed
[process 94459] TranslationRecognizerCallback close.
[Metric] requestId: xxxxxxxxx, first package delay ms: 448.789794921875, last package delay ms: 1169.598876953125
[process 94461] Transcript ==>  hello ,word,这里是阿里巴巴语音实验室。
[process 94461] Translate ==>  Hello, world. This is Alibaba's voice lab.
[process 94461] Translation completed
[process 94461] TranslationRecognizerCallback close.
[Metric] requestId: xxxxxxxxx, first package delay ms: 409.506103515625, last package delay ms: 1175.384033203125
```

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
