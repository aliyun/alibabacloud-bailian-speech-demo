## Speech Synthesis and Save File (Simple Mode)

English | [简体中文](./README.md)

## Python

### :point_right: Prerequisites

1. #### Configure Alibaba Cloud API-KEY

    Before running this example, you need to create an Alibaba Cloud account, obtain the API-KEY, and complete environment configuration. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

1. #### Install Python dependencies

    The Alibaba Cloud SDK requires Python 3.8 or higher. You can use the following command to install dependencies for this example:
    ```commandline
    pip3 install -r requirements.txt
    ```
    Please refer to [documentation](https://github.com/kkroening/ffmpeg-python) for ffmpeg installation

### :point_right: How to Run the Example
You can use the following command to run this example:

```commandline
python3 run.py
```

When running the example, it will synthesize the sample text "欢迎体验阿里云百炼大模型语音合成服务！" using the longanhuan voice style and save it to the result.mp3 file. You can modify text_to_synthesize to specify the text for synthesis.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>