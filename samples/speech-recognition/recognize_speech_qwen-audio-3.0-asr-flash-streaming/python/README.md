[comment]: # (title and brief introduction of the sample)
## 语音识别本地的单个文件

简体中文 | [English](./README_EN.md)

## Python

[comment]: # (prerequisites)
### :point_right: 前提条件

1. #### 配置阿里云百炼API-KEY

    在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)。

2. #### 配置 Workspace ID

    qwen-audio 系列模型使用 workspace 专属接入点 `https://{WORKSPACE_ID}.cn-beijing.maas.aliyuncs.com`，因此**必须**设置环境变量：

    ```commandline
    export DASHSCOPE_WORKSPACE_ID=llm-xxxxxx
    ```

    workspace id 可在阿里云百炼控制台获取。未设置时示例会打印提示并退出。

3. #### 安装Python依赖

    阿里云百炼SDK运行环境需要Python 3.8及以上版本。您可以使用以下命令来安装本示例的依赖：
    ```commandline
    pip3 install -r requirements.txt
    ```

[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例
您可以使用以下命令运行本示例：

```commandline
python3 run.py

```

示例运行时，会通过同步接口识别本地wav音频文件，并通过控制台打印结果。完整的识别结果会以json格式保存在```result.json```文件中。完整结果包含句级别和字级别的时间戳信息等。

> **进阶能力**已拆分为独立示例：
> - [对话上下文（Context）](../../recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-context)
> - [预创建热词表（Vocabulary）](../../recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-vocabulary)

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../../docs/image/group.png" width="400"/>

