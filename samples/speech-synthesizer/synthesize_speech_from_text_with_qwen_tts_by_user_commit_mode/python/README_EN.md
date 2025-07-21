## Text-to-Speech Synthesis and Playback (commit mode)

English | [简体中文](./README.md)

## Python

### :point_right: Prerequisites

1. #### Configure Alibaba Cloud Bailing API-KEY

    Before running this example, you need to create an Alibaba Cloud account, obtain the Alibaba Cloud Bailing API_KEY, and perform necessary environment configuration. For detailed steps on configuring the API-KEY, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### Install ffmpeg

    This example requires ffmpeg for audio/video decoding. It is recommended to download and install it from the official website and add the ffmpeg installation path to your system environment variables: [Download from ffmpeg's official website](https://www.ffmpeg.org/download.html). You can also refer to the document [How to install ffmpeg](../../../docs/QA/ffmpeg.md).

3. #### Install Python dependencies

    The Alibaba Cloud Bailing SDK requires Python 3.8 or higher. You can use the following command to install the dependencies for this example:
    [code]commandline
    pip3 install -r requirements.txt
    [code]
    Please refer to the [documentation](https://github.com/kkroening/ffmpeg-python) to install ffmpeg.

### :point_right: How to Run the Sample

You can run this example using the following command:

[code]commandline
python3 run.py
[code]

When running the example, it will use the Chelsie voice to synthesize a stream of sample text. The synthesized audio will be delivered in a streaming manner and played through the speaker.

When synthesizing streaming text, the `commit` mode is used, where users actively control when input buffers are submitted. This mode is suitable for advanced users or systems with extremely low latency requirements, but you need to manage sentence integrity and synthesis points yourself, which may affect synthesis quality.

You can modify the `text_to_synthesize` variable to specify the text to be synthesized.

### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
