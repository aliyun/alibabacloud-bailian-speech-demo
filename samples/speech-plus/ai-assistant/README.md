[comment]: # (title and brief introduction of the sample)
## AI Assistant网页版
AI Assistant网页版模拟了目前主流的大模型网站提供的交互服务，在多轮对话的基础上增加了实时、低延迟朗读大模型输出的能力。您可以参考这个示例项目搭建自己的Chatgpt网站。

<!-- [comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景         | 典型用法   | 使用说明                |
|--------------|--------|---------------------| -->


## Python

[comment]: # (prerequisites)
### :point_right: 前提条件

1. #### 配置阿里云百炼API-KEY

    在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

1. #### 安装Python依赖

    阿里云百炼SDK运行环境需要Python 3.8及以上版本。您可以使用以下命令来安装本示例的依赖：
    ```commandline
    pip3 install -r requirements.txt
    ```

[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例
本目录下下提供了调用通义Speech语音合成以及通义千问两个服务接口，实现的AI Assistant场景示例。

本示例提供了一个简化的GUI 界面，用来交互。
首先，请运行`demo_server.py`，默认会在本地的11111端口运行websocket服务。

之后可以双击在浏览器打开`interface.html`网页，输入提问并点击`Send`按钮发送消息后，会自动调用百炼SDK的接口，并在收到大模型的回复并且立刻朗读。本示例可以支持多轮交互，默认缓存五轮历史对话消息。

<img src="../../../docs/image/ai-assistant.png" width="400"/>

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../docs/image/groups.png" width="400"/>

    