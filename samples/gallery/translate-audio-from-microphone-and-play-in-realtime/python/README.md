
[comment]: # (title and brief introduction of the sample)
## 中文语音翻译成英文并实时播放

本示例展示了通过调用百炼平台的 Gummy 实时语音翻译模型和 Cosyvoice 流式语音合成模型，实现低延迟、实时的同声传译和实时双语字幕。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景           | 典型用法 | 使用说明                 |
|----------------| ----- |----------------------|
| **实时翻译**   | 同声传译，实时双语字幕 | *对音视频文件进行语音翻译，并显示朗读翻译结果* |

[comment]: # (prerequisites)
### :point_right: 前提条件

1. #### 配置阿里云百炼API-KEY

    在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### 安装Python依赖

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
在示例运行后，将会开通过麦克风录制语音并识别、翻译成英文，并将翻译结果使用 loongbella 音色朗读出来。同时将打开一个简单的GUI界面，用来显示实时双语字幕。

<img src="../../../../docs/image/translator.png" width="400"/>

示例会开启两个线程执行语音任务：
- 语音翻译线程：在while循环中通过麦克风获取音频数据，并发送给百炼平台实时翻译服务，通过回调收到实时结果并储存在队列中。
- 语音合成线程：在while循环中从队列取出实时翻译结果，并且通过流式语音合成服务生成音频，通过回调收到合成结果并播放。
SubtitleFrame是双语字幕GUI界面，他会扫描队列中的文本并追加显示到界面上。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>

