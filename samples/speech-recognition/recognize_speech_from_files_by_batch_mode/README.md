[comment]: # (title and brief introduction of the sample)
## 批量音视频文件语音识别（批量模式）
本示例展示了如何大批量的提交存储于OSS等云存储中的音视频文件链接，并调用[Paraformer录音文件识别](https://help.aliyun.com/zh/dashscope/developer-reference/api-details-13)服务实现批量语音识别的过程。

相对于实时语音识别，录音文件识别提供了更多语音格式、以及信息更丰富的结果供用户选择。同时批量音视频文件语音识别，相对于实时语音识别更适合时效性要求不高批量的任务处理。


[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景           | 典型用法 | 使用说明                 |
|----------------| ----- |----------------------|
| **音视频语音分析理解场景**   | 音视频批量语音识别 | *对音视频文件进行批量语音识别* |
| **会议语音分析理解场景** | 会议录音批量语音识别	 | *对会议录音文件进行批量语音识别*    |
| **电话客服中心机器人及对话分析理解场景**| 通话录音批量语音识别		 | *对客服中心通话录音文件进行批量语音识别*     |

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情

| 推荐模型                                                        | API详情                                                                                             |
|-------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| paraformer-v1<br/> paraformer-8k-v1 <br/>paraformer-mtl-v1  | [Paraformer录音文件识别](https://help.aliyun.com/zh/dashscope/developer-reference/api-details-13)|

### :point_right: 预期结果
运行示例，示例会访问文件转写服务，提交您输入的转写文件列表，等待识别结束。

识别结束，服务会以json列表的形式返回提交文件"file_url" 和对应的识别结果文件链接 "transcription_url" ,您可以复制控制台打印链接到浏览器打开或下载。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../docs/image/groups.png" width="400"/>
