[comment]: # (title and brief introduction of the sample)
## 语音合成并播放（流式模式）

简体中文 | [English](./README_EN.md)

## Python

[comment]: # (prerequisites)
### :point_right: 前提条件

1. #### 配置阿里云百炼API-KEY

    在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

1. #### 安装ffmpeg

    示例需要用到ffmpeg进行音视频解码。推荐从官方网站下载安装，并将ffmpeg安装路径配置进环境变量：[ffmpeg官方网站下载](https://www.ffmpeg.org/download.html)。也可以参考文档[如何安装ffmpeg](../../../docs/QA/ffmpeg.md)。

1. #### 安装Python依赖

    阿里云百炼SDK运行环境需要Python 3.8及以上版本。您可以使用以下命令来安装本示例的依赖：
    ```commandline
    pip3 install -r requirements.txt
    ```
    请参考[文档](https://github.com/kkroening/ffmpeg-python)安装ffmpeg

[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例
您可以使用以下命令运行本示例：

```commandline
python3 run.py
```

示例运行时，将会使用 longhua_v2 音色合成示例文本 “想不到时间过得这么快！昨天和你视频聊天，看到你那自豪又满意的笑容，我的心里呀，就如同喝了一瓶蜜一样甜呢！真心为你开心呢！” ，合成音频将按照流式方式下发，通过扬声器播放并保存到文件`result.mp3`中。

您可以通过修改`text_to_synthesize`合成指定的文本。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
