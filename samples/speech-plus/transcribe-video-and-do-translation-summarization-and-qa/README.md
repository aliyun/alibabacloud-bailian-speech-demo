[comment]: # (title and brief introduction of the sample)
## 视频转写并进行翻译摘要和问答
本示例展示了将一个视频文件转码为opus音频文件，通过录音文件转写服务识别为文本，然后调用通义千问大模型进行翻译、内容摘要和问答的过程。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景           | 典型用法 | 使用说明                 |
|----------------| ----- |----------------------|
| **音视频语音分析理解**   | 音视频摘要与问答 | *对音视频文件进行语音识别，并使用大模型进行摘要总结和问答* |

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)


[comment]: # (model and interface of the sample)
### :point_right: 参考详情

| 推荐模型          | API详情                                                                                             |
|---------------|---------------------------------------------------------------------------------------------------|
| paraformer-v2 | [Paraformer录音文件识别](https://help.aliyun.com/zh/dashscope/developer-reference/api-details-13)|
| qwen-plus | [通义千问大语言模型](https://help.aliyun.com/zh/model-studio/developer-reference/what-is-qwen-llm?spm=a2c4g.11186623.0.0.5dbb76776EGFHK)|

[comment]: # (dependency of the sample)
### :point_right: 依赖说明

本示例中，我们首先展示了如何将一个视频文件转码为[OPUS](https://opus-codec.org/)格式的音频文件再上传到OSS调用。这个文件预处理的过程可以大幅减少您的存储成本和网络传输成本。同时节省的传输时间也能大大加快视频文件转写的吞吐效率。在这个过程中，我们使用了ffmpeg进行音频转码，使用了OSS作为云存储和网络分发服务。以下是具体说明：

1. 安装ffmpeg: 请前往[ffmpeg官方网站下载](https://www.ffmpeg.org/download.html)。
2. 使用OSS：请前往[阿里云OSS](https://help.aliyun.com/zh/oss/getting-started/getting-started-with-oss)开通服务并进行必要配置。本示例下提供了一个简单的工具类[ossUtil.py](./python/ossUtil.py) 用来上传文件到OSS并获得文件的分享链接。请配置您的鉴权和bucket等信息，才可以使用。



[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/cosyvoice/group-10241220.png" width="400"/>
