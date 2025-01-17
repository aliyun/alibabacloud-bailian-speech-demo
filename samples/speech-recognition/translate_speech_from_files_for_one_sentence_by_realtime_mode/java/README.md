[comment]: # (title and brief introduction of the sample)
## 批量音频文件一句话语音识别和翻译（实时模式）
批量音频文件一句话语音识别和翻译（实时模式）是指并发的将多个音频文件通过实时的方式将语音数据发送给一句话语音翻译服务，并实时地返回翻译结果文本的过程。

如果您使用Java搭建语音服务请参考[高并发示例文档](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-in-high-concurrency-scenarios)获得最佳的性能。

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

示例使用了对象池和线程池实现并发运行。在示例运行时，程序会并发的读取您输入的多个音视频文件，将其独立的转为实时识别结果并分别以callback的方式回调。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>

