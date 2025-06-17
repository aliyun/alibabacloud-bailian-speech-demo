[comment]: # (title and brief introduction of the sample)
## 复刻你的音色进行语音合成并播放（流式模式）

简体中文 | [English](./README_EN.md)

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

运行示例。使用示例录音创建复刻音色，并使用复刻音色合成示例文本 “你好，欢迎使用阿里巴巴通义语音实验室的音色复刻服务～” ，合成音频将按照流式方式下发，通过扬声器播放并保存到文件`result.mp3`中。

您可以通过修改`audioUrl`替换示例录音文件为您自己的音频文件。

您可以通过修改`textArray`合成指定的文本。

您可以通过执行`DeleteVoiceByPrefix`批量删除指定前缀的音色。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>

