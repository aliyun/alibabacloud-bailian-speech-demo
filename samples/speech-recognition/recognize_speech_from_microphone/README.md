[comment]: # (title and brief introduction of the sample)
## 麦克风实时语音识别
本示例展示了如何从麦克风录制音频，并将获取的音频流发送至阿里云百炼模型服务进行实时语音识别。运行示例时，用户对麦克风所说的内容会被实时显示在屏幕上。我们使用VAD断句从而获得更块的响应速度。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景     | 典型用法 | 使用说明 |
|----------| ----- | ----- |
| **入门场景** | 麦克风语音识别 | *实时从麦克风录音并进行语音识别* |
| **电话客服中心机器人及对话分析理解场景** | 实时通话语音识别 | *实时对电话系统通话进行语音识别* |
| **会议语音分析理解场景** | 实时会议语音识别	 | *实时对会议语音进行语音识别* |

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情

| 推荐模型 | API详情 |
| ----- | ----- |
| **paraformer-realtime-v2**<br>paraformer-realtime-v1<br>paraformer-realtime-8k-v1 | [Paraformer实时语音识别API详情](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-real-time-speech-recognition-api) |

### :point_right: 预期结果

运行示例，在控制台会提示您开始说话，控制台输入'Ctrl+C' 即可结束识别。识别结果文本会在控制台打印。
```text
Press 'Ctrl+C' to stop recording and recognition
RecognitionCallback text:  一
RecognitionCallback text:  1234
```

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
