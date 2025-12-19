[comment]: # (title and brief introduction of the sample)
## 批量音视频文件语音识别（实时模式）
本示例展示了如何批量的调用实时语音识别接口，实现多个文件流的输入，并实时返回多个文件对应的识别结果。

音视频文件语音识别的**实时模式**更适合对本地文件进行处理且即时返回结果，或搭建处理流式音频的服务端，收集前端的音频流，即时返回识别结果的场景。

如果您使用Java搭建语音服务，请参考[高并发示例文档](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-in-high-concurrency-scenarios)获得最佳的性能。

如果您需要对大批量云端文件进行生产任务处理、且不需要即时返回结果，请参考示例：[批量音视频文件语音识别（批量模式）](../recognize_speech_from_files_by_batch_mode//)。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景    | 典型用法    | 使用说明              |
|---------|---------|-------------------|
| **入门场景**| 音视频文件语音识别	 | *批量对音视频文件进行语音识别*  |

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情

| 推荐模型 | API详情 |
| ----- | ----- |
| **fun-asr-realtime** | [Fun-ASR 实时语音识别API详情](https://help.aliyun.com/zh/model-studio/fun-asr-real-time-speech-recognition-api-reference/) |
| **paraformer-realtime-v2**<br>paraformer-realtime-v1<br>paraformer-realtime-8k-v1 | [Paraformer实时语音识别API详情](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-real-time-speech-recognition-api) |


### :point_right: 预期结果

运行示例，在控制台会输出流式识别结果。每个文件的识别对应一个[process id], 每个文件的结果会不断返回增量的结果。如
```
    //process: 51389 对应sample_audio.mp3的识别结果1
    [process 51389]RecognitionCallback text:  那河畔的金柳是夕阳中的

    //process: 51392 对应sample_video_story.mp4的识别结果
    [process 51392]RecognitionCallback text:  在一个阳光明媚的早晨，鸭妈妈决定带着小鸭子们

    //process: 51389 对应sample_audio.mp3的识别结果2
    [process 51389]RecognitionCallback text:  那河畔的金柳是夕阳中的新娘。
```

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
