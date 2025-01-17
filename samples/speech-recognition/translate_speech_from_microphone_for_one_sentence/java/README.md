[comment]: # (title and brief introduction of the sample)
## 麦克风实时一句话语音识别和翻译
## Java

[comment]: # (prerequisites)
### :point_right: 前提条件

1. #### 配置阿里云百炼API-KEY

    在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### Java运行环境

   在运行本示例之前，您需要安装Java运行环境和Maven构建工具。


[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例

您可以通过运行run.sh (Linux, Mac系统)或run.bat (Windows系统)来运行本示例。

运行后将会从麦克风录制您说的第一句话，并实时翻译成英文。这些文本会打印在屏幕上。示例采用了VAD判停，当您停止说话后会自动停止录制。录制的音频会被保存到`request_id_record.pcm`文件中。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>

