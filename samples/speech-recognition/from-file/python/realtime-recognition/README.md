## 实时语音识别
实时语音识别（Real-Time Speech Recognition）是指通过实时的方式将语音数据发送给语音识别服务，并实时地将语音转换为文字的过程。
实时语音识别适用于对时效性要求比较高的语音识别场景，如电话客服、语音对话聊天、会议字幕等。

## 前提条件
本目录下提供了通过读取音频文件进行实时语音识别的示例。在运行代码之前请确保您已安装依赖并配置好必要的环境变量。


除了使用实时文件转写接口外，我们还提供了模拟会议场景中并发处理多路语音音频的示例：[并发实时语音识别](./multi_process_realtime_recognize_to_text.py)

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

### 运行示例

- 运行同步语音识别示例
    
    同步调用中，recognition.call(file_path)一次性将语音音频发送给服务，同步等待服务返回识别结果。
```commandline
python recognize_speech_to_text_by_sync_realtime_api
```

- 运行异步语音识别示例

    本示例中，识别启动后，不断调用recognition.send_audio_frame(chunk)输入音频片段，通过RecognitionCallback回调函数接收识别结果。
```commandline
python recognize_speech_to_text_by_async_realtime_api.py
```
    
- 运行多并发语音识别示例

    本示例展示通过multiprocessing并发的方式调用语音识别的过程。
```commandline
python batch_synthesized_text_to_speech_and_save_in_files.py
```
    