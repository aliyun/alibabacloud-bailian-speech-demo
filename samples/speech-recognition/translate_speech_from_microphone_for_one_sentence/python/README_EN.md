[comment]: # (title and brief introduction of the sample)
## Microphone Real-time Sentence-level Speech Recognition and Translation

English | [简体中文](./README.md)

## Python

[comment]: # (prerequisites)
### :point_right: Prerequisites

1. #### Configure Alibaba Cloud Bailian API-KEY

    Before running this example, you need to create an Alibaba Cloud account, obtain the Alibaba Cloud Bailian API-KEY, and complete necessary environment configurations. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### Install Python Dependencies

    The Alibaba Cloud Bailian SDK requires Python 3.8 or higher. You can install the dependencies for this example using the following command:
    ```commandline
    pip3 install -r requirements.txt
    ```

[comment]: # (how to run the sample and expected results)
### :point_right: Run Example
You can run this example using the following command:

```commandline
python3 run.py
```

After execution, the program will record your first spoken sentence from the microphone and translate it to English in real-time. The text will be printed on the screen. The example uses VAD (Voice Activity Detection) to automatically stop recording after you finish speaking. The recorded audio will be saved to a `request_id_record.pcm` file.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
