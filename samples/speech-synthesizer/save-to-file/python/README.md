## 离线语音合成 
离线语音合成是指通过语音合成服务将合成的语音保存为文件的使用方式。通常这种方式用于非实时的场景。
离线语音合成适用于配音、有声读物等场景。

## 前提条件
本目录提供的是离线语音合成的示例。示例展示了调用CosyVoice 大模型语音合成音频并保存为音频文件的过程。


在运行代码之前请确保您已安装依赖并配置好必要的环境变量。

以下是两种不同接口的调用示例。

[流式语音合成并保存示例](./stream_synthesize_text_to_speech_and_save_in_file.py)  | [同步语音合成并保存示例](./sync_synthesize_text_to_speech_and_save_in_file.py)

### 安装 Python 依赖

阿里云百炼SDK运行环境需要Python3.8及以上版本。
运行本场景DEMO依赖的环境可以通过[PyPI](https://pypi.org/)安装。

- 百炼SDK
```commandline
pip3 install dashscope //安装阿里云百炼SDK
```


### 配置阿里云百炼API-KEY
在使用百炼SDK进行语音识别之前，您需要先在阿里云控制台创建语音识别服务并获取API-KEY。
- 在[百炼控制台](https://bailian.console.aliyun.com/)界面右上角头像位置，鼠标悬浮后，展示API-KEY，点击后进入API-KEY管理页面。
- 点击【创建新的API-KEY】，会自动创建一条属于这个账号的API-KEY。列表上展示API-KEY密文，点击【查看】可以看到API-KEY的明文信息。请注意保存API-KEY的明文信息，后续使用API-KEY时需要用到。
- 更多百炼配置信息请参考：[PREREQUISITES.md](../../../../../PREREQUISITES.md)
