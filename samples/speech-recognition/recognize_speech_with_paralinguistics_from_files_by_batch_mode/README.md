[comment]: # (title and brief introduction of the sample)
## 批量音视频文件富文本语音识别（批量模式）
本示例展示了如何大批量的提交存储于OSS等云存储中的音视频文件链接，并调用支持富文本识别的[SenseVoice](https://help.aliyun.com/zh/dashscope/developer-reference/quick-start-sensevoice)模型进行文件转写服务实现批量语音转写。

相对于实时语音识别，录音文件识别提供了更多语音格式、以及信息更丰富的结果供用户选择。同时批量音视频文件语音识别，相对于实时语音识别更适合时效性要求不高批量的任务处理。


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
| sensevoice-v1| [SenseVoice 录音文件语音识别](https://help.aliyun.com/zh/model-studio/developer-reference/sensevoice-api) | 多达50+语种识别 <br/> 情感识别 <br/> 音频事件检测 |

### :point_right: 预期结果
运行示例，示例会访问文件转写服务，提交您输入的转写文件列表，等待识别结束。

识别结束，服务会以json列表的形式返回提交文件"file_url" 和对应的识别结果文件链接 "transcription_url" ,您可以复制控制台打印链接到浏览器打开或下载。

在控制台，会打印每个文件对应的简略的识别结果。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../docs/image/groups.png" width="400"/>
