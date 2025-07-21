[comment]: # (title and brief introduction of the sample)
## 语音合成并播放（commit 模式）

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

示例运行时，将会使用 Chelsie 音色合成示例文本流，合成音频将按照流式方式下发，通过扬声器播放。

在合成流式文本时，使用`commit`模式，用户主动控制输入缓存提交的模式，适合高级用户或延迟要求极高的系统使用，但需自行控制句子完整性与合成点，可能影响合成质量。

您可以通过修改`text_to_synthesize`合成指定的文本。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>

