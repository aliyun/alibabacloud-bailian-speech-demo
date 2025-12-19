## Speech Synthesis and Playback (Streaming Mode)

English | [简体中文](./README.md)

## Python

### :point_right: Prerequisites

1. #### Configure Alibaba Cloud API-KEY

    Before running this example, you need to create an Alibaba Cloud account, obtain the API-KEY, and complete environment configuration. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

1. #### Install ffmpeg

    This example requires ffmpeg for audio/video decoding. It is recommended to download and install it from the official website, and configure the ffmpeg installation path in the environment variables: [ffmpeg official website download](https://www.ffmpeg.org/download.html). You can also refer to the document [How to install ffmpeg](../../../docs/QA/ffmpeg_en.md).

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

When running the example, it will synthesize the sample text "Time flies so fast! Yesterday when we video chatted, seeing your proud and satisfied smile made my heart as sweet as drinking a bottle of honey! I'm truly happy for you!" using the longanhuan voice style. The synthesized audio will be streamed, played through the speaker, and saved to the file result.mp3.

You can modify `text_to_synthesize` to specify the text for synthesis.


[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
