## 实时语音识别
实时语音识别（Real-Time Speech Recognition）是指通过实时的方式将语音数据发送给语音识别服务，并实时地将语音转换为文字的过程。
实时语音识别适用于对时效性要求比较高的语音识别场景，如电话客服、语音对话聊天、会议字幕等。

## 前提条件
本目录下提供了通过读取音频文件进行实时语音识别的示例。在运行代码之前请确保您已安装依赖并配置好必要的环境变量。

### 安装 Python 依赖

阿里云百炼SDK运行环境需要Python3.8及以上版本。
运行本场景DEMO依赖的环境可以通过[PyPI](https://pypi.org/)安装。

- 导入百炼SDK
```commandline
pip3 install dashscope //安装阿里云百炼SDK
```


### 配置阿里云百炼API-KEY
在使用百炼SDK进行语音识别之前，您需要先在阿里云控制台创建语音识别服务并获取API-KEY。
- 在[百炼控制台](https://bailian.console.aliyun.com/)界面右上角头像位置，鼠标悬浮后，展示API-KEY，点击后进入API-KEY管理页面。
- 点击【创建新的API-KEY】，会自动创建一条属于这个账号的API-KEY。列表上展示API-KEY密文，点击【查看】可以看到API-KEY的明文信息。请注意保存API-KEY的明文信息，后续使用API-KEY时需要用到。
- 更多百炼配置信息请参考：[PREREQUISITES.md](../../../../../PREREQUISITES.md)
