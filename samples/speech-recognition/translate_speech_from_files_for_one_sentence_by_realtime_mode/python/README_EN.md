[comment]: # (title and brief introduction of the sample)
## Batch Audio File Sentence-level Speech Recognition and Translation (Real-time Mode)

English | [简体中文](./README.md)

Batch audio file sentence-level speech recognition and translation in real-time mode refers to the process of concurrently sending multiple audio files to a sentence-level speech translation service in real-time and returning translated text results immediately.

## Python

[comment]: # (prerequisites)
### :point_right: Prerequisites

1. #### Configure Alibaba Cloud Bailian API-KEY

    Before running this example, you need to create an Alibaba Cloud account, obtain the Alibaba Cloud Bailian API-KEY, and complete necessary environment configurations. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### Install ffmpeg

    This example requires ffmpeg for audio/video decoding. It is recommended to download and install it from the official website, and add the ffmpeg installation path to your environment variables: [ffmpeg official website download](https://www.ffmpeg.org/download.html). You can also refer to the documentation [How to Install ffmpeg](../../../docs/QA/ffmpeg_en.md).

3. #### Install Python Dependencies

    The Alibaba Cloud Bailian SDK requires Python 3.8 or higher. You can install the dependencies for this example using the following command:
    ```commandline
    pip3 install -r requirements.txt
    ```

[comment]: # (how to run the sample and expected results)
### :point_right: Run Example
- You can run this example using the following command:

```commandline
python3 run.py
```

This example uses multiprocessing to achieve concurrent execution. During execution, the program will concurrently read multiple audio/video files you input, convert them into real-time recognition results independently, and callback each result separately through callback functions.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>