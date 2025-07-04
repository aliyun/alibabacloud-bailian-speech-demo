[comment]: # (title and brief introduction of the sample)
## 视频文件的实时语音识别

简体中文 | [English](./README_EN.md)

## Python

[comment]: # (prerequisites)
### :point_right: 前提条件

1. #### 配置阿里云百炼API-KEY

    在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)。

1. #### 安装ffmpeg

    示例需要用到ffmpeg进行音视频解码。推荐从官方网站下载安装，并将ffmpeg安装路径配置进环境变量：[ffmpeg官方网站下载](https://www.ffmpeg.org/download.html)。也可以参考文档[如何安装ffmpeg](../../../docs/QA/ffmpeg.md)。

1. #### 安装Python依赖

    阿里云百炼SDK运行环境需要Python 3.8及以上版本。您可以使用以下命令来安装本示例的依赖：
    ```commandline
    pip3 install -r requirements.txt
    ```

[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例
您可以使用以下命令运行本示例：

```commandline
python3 run.py
```

示例运行时，本地视频文件会被通过ffmpeg实时转为16k opus音频格式，之后再被实时转写为文字，并通过控制台打印结果。

本示例引入了AudioDecoder类，使用ffmpeg实现了音视频文件的转码，借助于ffmpeg丰富的格式支持，示例支持目前市面上大多数的音视频文件格式转换为适用于语音识别的音频。

### :point_right: 预期结果

完整的识别结果会以json格式保存在```result.json```文件中。完整结果包含句级别和字级别的时间戳信息等。语音识别的纯文本会同时在控制台打印：
```text
The brief result is:
横看成岭侧成峰，远近高低各不同。不识庐山真面目，只缘身在此山中。
```

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>

