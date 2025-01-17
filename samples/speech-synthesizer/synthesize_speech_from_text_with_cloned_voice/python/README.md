[comment]: # (title and brief introduction of the sample)
## 复刻你的音色进行语音合成并播放（流式模式）
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

#### 录制音频
您可以首先使用以下命令按照提示录制一段音频用于克隆，并储存在`your_record_file.wav`中。请您使用阿里云oss或其他云存储方法获取可下载http链接。

```commandline
python3 record.py
```

#### 克隆音色并合成语音

在获取可下载http链接后，您可以使用以下命令，将参数替换为您的录音http链接，运行本示例：

```commandline
python3 run.py <your-record-http-link>
```

示例运行时，将会根据您提供的录音创建复刻音色，并使用复刻音色合成示例文本 “你好，欢迎使用阿里巴巴通义语音实验室的音色复刻服务～” ，合成音频将按照流式方式下发，通过扬声器播放并保存到文件`result.mp3`中。

如果没有填写`<your-record-http-link>`参数，将会使用示例录音复刻音频。

您可以通过修改`text_to_synthesize`合成指定的文本。

您可以通过执行`delete_voice_by_prefix`批量删除指定前缀的音色。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
