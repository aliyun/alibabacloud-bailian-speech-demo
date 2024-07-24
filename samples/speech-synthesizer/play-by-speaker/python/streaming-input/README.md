## 流式语音合成 
流式语音合成是指支持重复输入合成文本的语音合成服务。
相对于一句话语音合成能力，流式语音合成更适合结果大模型能力，对于在生成式AI场景中，对一段一段输出的文本进行合成更加优化。
流式语音合成也适用于长文本场景，如绘本小说等有声读物，通过分句的方式进行调用，可以大幅提升合成效率。

## 前提条件
本目录提供的是流式语音合成的示例。示例展示了调用CosyVoice 大模型语音合成音频并进行播放。


在运行代码之前请确保您已安装依赖并配置好必要的环境变量。

[多句文本流式调用示例](./stream_synthesize_text_to_speech.py)  | [结合千问大模型生成的文本流式调用示例](./stream_synthesize_llm_response_to_speech.py)

### 安装 Python 依赖

阿里云百炼SDK运行环境需要Python3.8及以上版本。
运行本场景DEMO依赖的环境可以通过[PyPI](https://pypi.org/)安装。

您可以使用`pip install -r requirements.txt` 命令来安装本文件夹下的requirements依赖文件。或者手动安装下方的依赖。

- 三方SDK
```commandline
pip3 install pyaudio //用于实时播放音频
pip3 install ffmpeg-python //python的ffmpeg绑定, 用于实时解码mp3音频。
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

### 运行

- 运行多句文本流式调用示例

```commandline
python stream_synthesize_text_to_speech.py
```

- 运行结合千问大模型生成的文本流式调用示例

```commandline
python stream_synthesize_llm_response_to_speech.py
```
    
