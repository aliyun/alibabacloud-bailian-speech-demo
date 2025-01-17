[comment]: # (title and brief introduction of the sample)
## 批量音频文件一句话语音识别和翻译（实时模式）
批量音频文件一句话语音识别和翻译（实时模式）是指并发的将多个音频文件通过实时的方式将语音数据发送给一句话语音翻译服务，并实时地返回翻译结果文本的过程。

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

[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例
- 您可以使用以下命令运行本示例：

```commandline
python3 run.py
```

   示例使用了multiprocessing实现并发运行。在示例运行时，程序会并发的读取您输入的多个音视频文件，将其独立的转为实时识别结果并分别以callback的方式回调识别结果。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>