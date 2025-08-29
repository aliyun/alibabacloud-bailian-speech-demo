# 在网页中录音并进行语音识别

简体中文 | [English](./README_EN.md)

本项目在本地搭建了http服务和websocket语音识别服务，在网页中录音并实时显示识别结果。您可以参考这个示例项目在自己的网页中加入语音识别功能。

## 前提条件

#### 安装 Python 依赖

阿里云百炼SDK运行环境需要Python3.8及以上版本。
运行本场景DEMO依赖的环境可以通过[PyPI](https://pypi.org/)安装。

您可以使用`pip install -r requirements.txt` 命令来安装本文件夹下的requirements依赖文件。或者手动安装下方的依赖。

- 导入百炼SDK
```commandline
pip3 install dashscope //安装阿里云百炼SDK
pip3 install websockets //安装websocket服务依赖
```

#### 配置阿里云百炼API-KEY

在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

## 运行示例

本目录展示了前后端分离的语音识别示例，通过websocket连接前后端，以及如何处理实时更新识别结果。


当您点击“开始录音”按钮后，网页会和python websocket服务创建连接，开始从麦克风录制音频，并将录音实时的发送给websocket服务。服务器会调用paraformer-realtime-v2语音识别模型，并将实时语音识别结果返回给网页展示。实时识别每一句的结果会在同一行内不断更新，直到分句后进入下一行。

首先，请在环境变量中配置好百炼API-KEY，并运行`demo_server.py`，默认会在本地的9090端口运行websocket服务。
```
export DASHSCOPE_API_KEY=xxxxxxx
python server.py
```

之后请在本目录运行一个http服务，用于支持通过浏览器访问当前目录的文件。
```
python -m http.server 9000
```

之后您可以在浏览器输入`http://localhost:9000`打开测试网页。输入提问并点击`开始录音`按钮发送消息后对麦克风说话。

<img src="../../../../docs/image/html-asr.png" width="400"/>

## 关于录音的说明

在`audio_recorder.js`中，我们使用 Web Audio API 开发了 PCMAudioRecorder 录制PCM格式的音频，并通过 AudioWorkletNode 异步将采样点从浮点数转化为16bit的Int16Array并通过回调返回。buffer默认大小为1600采样点，即100ms。
