[comment]: # (title and brief introduction of the sample)
## Batch Audio/Video File Speech Translation (Real-time Mode)

English | [简体中文](./README.md)

Batch audio/video file speech translation in real-time mode refers to the process of concurrently sending multiple audio files to a speech translation service in real-time and returning translated text results immediately.

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
- You can run this example using the following command:

```commandline
python3 run.py
```

This example uses multiprocessing to achieve concurrent execution. During execution, the program will concurrently read multiple audio files you input, convert them into real-time recognition results independently, and callback each result separately through callback functions.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
