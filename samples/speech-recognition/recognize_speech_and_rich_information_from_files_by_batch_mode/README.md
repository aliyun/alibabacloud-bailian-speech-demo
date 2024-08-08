[comment]: # (title and brief introduction of the sample)
## 批量音视频文件富信息语音识别（批量模式）
本示例展示了如何批量的提交存储于云存储（例如OSS）中的音视频文件URL，并调用阿里云百炼语音识别大模型离线文件转写API，实现批量语音识别的过程。

通过使用SenseVoice语音大模型，可以对多语种语音进行识别，并同时返回情感、音频事件等富信息。音视频文件**富信息语音识别**更适合需要识别更丰富的语种、情感、音频事件等内容的场景。对一般的音视频文件语音识别场景，仍建议使用更具性价比的Paraformer模型，请参考示例：[批量音视频文件语音识别（批量模式）](../recognize_speech_from_files_by_batch_mode/)。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景           | 典型用法 | 使用说明                 |
|----------------| ----- |----------------------|
| **音视频语音分析理解场景**   | 音视频批量富文本语音识别 | *对音视频文件中的文本/情绪/事件进行识别* |


[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情

| 推荐模型 | API详情  | 模型特色                              |
| ----- |--------------------------|-----------------------------------|
| **sensevoice-v1** | [SenseVoice录音文件语音识别](https://help.aliyun.com/zh/model-studio/developer-reference/sensevoice-api) | 多达50+语种 <br/> 情感识别 <br/> 音频事件检测 |

### :point_right: 预期结果
运行示例，示例会访问文件转写服务，提交您输入的转写文件列表，等待识别结束。

识别结束，服务会以json列表的形式返回提交文件```file_url```和对应的识别结果文件链接```transcription_url```，您可以复制控制台打印链接到浏览器打开或下载。

在控制台，会打印每个文件对应的简略的识别结果。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../docs/image/groups.png" width="400"/>
