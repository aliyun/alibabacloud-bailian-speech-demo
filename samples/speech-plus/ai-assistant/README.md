## AI Assistant网页版
AI Assistant网页版模拟了目前主流的大模型网站提供的交互服务，在多轮对话的基础上增加了实时、低延迟朗读大模型输出的能力。您可以参考这个示例项目搭建自己的Chatgpt网站。

## 前提条件
本目录下下提供了调用通义Speech语音合成以及通义千问两个服务接口，实现的AI Assistant场景示例。

本示例提供了一个简化的GUI 界面，用来交互。
首先，请运行`demo_server.py`，默认会在本地的11111端口运行websocket服务。

之后可以双击在浏览器打开`interface.html`网页，输入提问并点击`Send`按钮发送消息后，会自动调用百炼SDK的接口，并在收到大模型的回复并且立刻朗读。本示例可以支持多轮交互，默认缓存五轮历史对话消息。

<img src="../../../docs/image/ai-assistant.png" width="400"/>

### 安装 Python 依赖

阿里云百炼SDK运行环境需要Python3.8及以上版本。
运行本场景DEMO依赖的环境可以通过[PyPI](https://pypi.org/)安装。

您可以使用`pip install -r requirements.txt` 命令来安装本文件夹下的requirements依赖文件。或者手动安装下方的依赖。

- 导入百炼SDK
```commandline
pip3 install dashscope //安装阿里云百炼SDK
```

### 配置阿里云百炼API-KEY
在使用百炼SDK进行语音识别之前，您需要先在阿里云控制台创建语音识别服务并获取API-KEY。
- 在[百炼控制台](https://bailian.console.aliyun.com/)界面右上角头像位置，鼠标悬浮后，展示API-KEY，点击后进入API-KEY管理页面。
- 点击【创建新的API-KEY】，会自动创建一条属于这个账号的API-KEY。列表上展示API-KEY密文，点击【查看】可以看到API-KEY的明文信息。请注意保存API-KEY的明文信息，后续使用API-KEY时需要用到。
- 更多百炼配置信息请参考：[PREREQUISITES.md](../../../../../PREREQUISITES.md)
