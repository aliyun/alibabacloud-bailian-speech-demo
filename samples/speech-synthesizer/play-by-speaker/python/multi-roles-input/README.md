## 多角色语音合成 
本示例是一个多角色语音合成调用的原型（Prototype）。
在有声读物场景，通常会有多角色参与，而通义语音大模型服务提供了丰富的说话人音色，能够很好的完成分角色语音合成。
在这个示例中，我们将导入一个json格式的多角色故事，通过调用不同角色选择不同的发音人，生成了一个多角色的语音绘本故事。

## 前提条件
在运行代码之前请确保您已安装依赖并配置好必要的环境变量。

[多角色语音合成示例](./synthesize_multi_roles_text_to_speech.py)  

### 安装 Python 依赖

阿里云百炼SDK运行环境需要Python3.8及以上版本。
运行本场景DEMO依赖的环境可以通过[PyPI](https://pypi.org/)安装。

- 三方SDK
```commandline
pip3 install ffmpeg-python //python的ffmpeg绑定, 用于实时解码mp3音频。
pip3 install pyaudio //用于实时播放音频
```
在安装ffmpeg-python时请参考对应[官方文档](https://github.com/kkroening/ffmpeg-python)安装ffmpeg

- 百炼SDK
```commandline
pip3 install dashscope //安装阿里云百炼SDK
```


### 配置阿里云百炼API-KEY
在使用百炼SDK进行语音识别之前，您需要先在阿里云控制台创建语音识别服务并获取API-KEY。
- 在[百炼控制台](https://bailian.console.aliyun.com/)界面右上角头像位置，鼠标悬浮后，展示API-KEY，点击后进入API-KEY管理页面。
- 点击【创建新的API-KEY】，会自动创建一条属于这个账号的API-KEY。列表上展示API-KEY密文，点击【查看】可以看到API-KEY的明文信息。请注意保存API-KEY的明文信息，后续使用API-KEY时需要用到。
- 更多百炼配置信息请参考：[PREREQUISITES.md](../../../../../PREREQUISITES.md)
