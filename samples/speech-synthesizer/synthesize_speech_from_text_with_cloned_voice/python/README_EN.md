## Clone Your Voice for Speech Synthesis and Playback (Streaming Mode)

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

#### Record Audio
First, you can use the following command to record an audio clip according to the prompts for cloning, which will be saved in `your_record_file.wav`. Please use Alibaba Cloud OSS or other cloud storage methods to obtain a downloadable HTTP link.

```commandline
python3 record.py
```

#### Clone Voice and Synthesize Speech

After obtaining the downloadable HTTP link, you can use the following command to run this example by replacing the parameter with your audio HTTP link:

```commandline
python3 run.py <your-record-http-link>
```

When running the example, it will create a cloned voice style based on your recording and use the cloned voice style to synthesize the sample text "Hello, welcome to use Alibaba Tongyi Voice Lab's voice cloning service~". The synthesized audio will be streamed, played through the speaker, and saved to the file result.mp3.

If the `<your-record-http-link>` parameter is not provided, the example will use the sample recording for voice cloning.

You can modify `text_to_synthesize` to specify the text for synthesis.

You can batch delete voice styles with a specific prefix by executing `delete_voice_by_prefix`.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>