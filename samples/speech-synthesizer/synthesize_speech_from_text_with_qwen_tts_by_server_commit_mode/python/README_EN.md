[comment]: # (title and brief introduction of the sample)
## Text-to-speech synthesis and playback (server commit mode)

English | [简体中文](./README.md)

## Python

[comment]: # (prerequisites)
### :point_right: Prerequisites

1. #### Configure Alibaba Cloud BaiLian API-KEY

    Before running this example, you need to activate an Alibaba Cloud account, obtain the Alibaba Cloud BaiLian API_KEY, and perform necessary environment configurations. For detailed steps on configuring the API-KEY, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

1. #### Install ffmpeg

    This example requires ffmpeg for audio/video decoding. It is recommended to download and install it from the official website, and configure the ffmpeg installation path in the system environment variables: [Download from ffmpeg's official website](https://www.ffmpeg.org/download.html). You can also refer to the document [How to install ffmpeg](../../../docs/QA/ffmpeg.md).

1. #### Install Python dependencies

    The Alibaba Cloud BaiLian SDK requires Python 3.8 or higher. You can use the following command to install the dependencies for this example:
    ```commandline
    pip3 install -r requirements.txt
    ```
    Please refer to the [documentation](https://github.com/kkroening/ffmpeg-python) to install ffmpeg.

[comment]: # (how to run the sample and expected results)
### :point_right: Run the example
You can run this example using the following command:

```commandline
python3 run.py
```

When the example runs, it will synthesize a sample text stream using the Chelsie voice. The synthesized audio will be delivered in a streaming manner and played through the speaker.

While synthesizing the text stream, the `server_commit` mode is used, which allows the server to control the accumulation and submission logic. Users only need to continuously input text; the system automatically determines when to start the synthesis, balancing synthesis quality and response latency. This mode is suitable for most developers.

You can modify the `text_to_synthesize` variable to synthesize specific text.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
