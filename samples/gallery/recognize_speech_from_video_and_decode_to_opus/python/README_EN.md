## Real-Time Speech Recognition for Video Files

English | [简体中文](./README.md)

## Python

### :point_right: Prerequisites

1. #### Configure Alibaba Cloud Tongyi Lab API-KEY

    Before running this example, you need to activate an Alibaba Cloud account, obtain the Tongyi Lab API-KEY, and perform necessary environment configurations. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md).

1. #### Install ffmpeg

    This example requires ffmpeg for audio/video decoding. It is recommended to download and install from the official website, and add the ffmpeg installation path to the environment variables: [ffmpeg official website download](https://www.ffmpeg.org/download.html). You can also refer to the document [How to install ffmpeg](../../../docs/QA/ffmpeg_en.md).

1. #### Install Python Dependencies

    The Alibaba Cloud Tongyi Lab SDK requires Python 3.8 or higher. You can install the dependencies for this example using the following command:
    ```commandline
    pip3 install -r requirements.txt
    ```

### :point_right: Run Example
You can run this example using the following command:

```commandline
python3 run.py
```

When the example runs, the local video file will be converted in real-time to 16k opus audio format using ffmpeg, then transcribed to text in real-time, and the results will be printed to the console.

This example introduces the AudioDecoder class, which uses ffmpeg for audio/video file transcoding. Leveraging ffmpeg's rich format support, the example supports converting most common audio/video file formats into audio suitable for speech recognition.

### :point_right: Expected Results

The complete recognition results will be saved in the `result.json` file in JSON format. The complete results include timestamp information at both sentence and character levels. The plain text of the speech recognition will also be printed to the console:

```text
The brief result is:
横看成岭侧成峰，远近高低各不同。不识庐山真面目，只缘身在此山中。
```

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>