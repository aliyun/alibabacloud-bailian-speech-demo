[comment]: # (title and brief introduction of the sample)
## 并发调用语音合成

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

运行示例。使用 longanhuan 音色并发合成 “欢迎体验阿里云百炼大模型语音合成服务！” 并保存在 `<requestId>.mp3` 文件中。

在java并发示例中，使用了连接池、对象池、线程池三种资源池。当对象和连接复用时可以有效降低建立连接的时间开销。

您可以通过修改`task_list`中增加/删除任务合成指定数量的文本。通过`peakThreadNum`参数修改最大进程数。建议不超过机器的cpu核心数。通过`runTimes`参数设定任务执行次数。

:information_source: **注意**：个人账号的appkey当前仅支持 3 并发，如需开通多并发请联系我们。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>

