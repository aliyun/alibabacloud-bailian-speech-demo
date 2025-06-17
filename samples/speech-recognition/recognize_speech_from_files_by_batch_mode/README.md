[comment]: # (title and brief introduction of the sample)
## 批量音视频文件语音识别（批量模式）

简体中文 | [English](./README_EN.md)

本示例展示了如何大批量的提交存储于云存储（例如OSS）中的音视频文件URL，并调用阿里云百炼语音识别大模型离线文件转写API，实现批量语音识别的过程。

录音文件识别提供了更多音视频格式，以及更准确、信息更丰富的识别结果供用户使用。音视频文件语音识别的**批量模式**更适合对大批量云端文件进行生产任务处理、且不需要即时返回结果的场景。如果您需要对本地文件进行处理，且希望即时返回结果，请参考示例：[批量音视频文件语音识别（实时模式）](../recognize_speech_from_files_by_realtime_mode/)。

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
| **paraformer-v2**<br/> paraformer-v1<br/> paraformer-8k-v1 <br/>paraformer-mtl-v1  | [录音文件识别API详情](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-api)|

### :point_right: 预期结果

运行示例，示例会访问文件转写服务，提交您输入的转写文件列表，等待识别结束。

识别结束，服务会以json列表的形式返回提交文件```file_url```和对应的识别结果文件链接```transcription_url```，您可以复制控制台打印链接到浏览器打开或下载。

[comment]: # (best practices)
### :point_right: 最佳实践

虽然阿里云百炼语音识别大模型的文件转写API可以兼容多种格式的音视频文件，但由于视频文件尺寸通常较大、传输较为耗时，建议对其进行预处理，仅提取需要进行语音识别的音轨，并进行合理压缩，从而显著降低文件尺寸。这样做将大大加快视频文件转写的吞吐效率。以下步骤展示了如何使用ffmpeg进行有关的预处理。

1. 安装ffmpeg：请前往[ffmpeg官方网站下载](https://www.ffmpeg.org/download.html)。也可以参考文档[如何安装ffmpeg](../../../docs/QA/ffmpeg.md)。

1. 预处理视频文件：使用ffmpeg提取视频文件中的音轨、降采样到16kHz 16bit Mono、并压缩编码为opus文件进行存储。
    ```
    ffmpeg -i input-video-file -ac 1 -ar 16000 -acodec libopus output-audio-file.opus
    ```

1. 将压缩后的纯音频文件```output-audio-file.opus```上载到云存储并获取其URL。向阿里云百炼文件转写服务提交该URL。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
