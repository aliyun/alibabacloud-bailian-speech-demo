[comment]: # (title and brief introduction of the sample)
## Batch Audio File Sentence-level Speech Recognition and Translation (Real-time Mode)

English | [简体中文](./README.md)

Batch audio file sentence-level speech recognition and translation in real-time mode refers to the process of concurrently sending multiple audio files to a sentence-level speech translation service in real-time and returning translated text results immediately.

If you use Java to build a speech service, refer to [High Concurrency Example Documentation](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-in-high-concurrency-scenarios) for optimal performance.

## Java

[comment]: # (prerequisites)
### :point_right: Prerequisites

1. #### Configure Alibaba Cloud Bailian API-KEY

    Before running this example, you need to create an Alibaba Cloud account, obtain the Alibaba Cloud Bailian API-KEY, and complete necessary environment configurations. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### Java Runtime Environment

   Before running this example, you need to install Java runtime environment and Maven build tools.

[comment]: # (how to run the sample and expected results)
### :point_right: Run Example

You can run this example by executing run.sh (Linux/Mac systems) or run.bat (Windows systems).

The example uses object pools and thread pools to achieve concurrent execution. During execution, the program will concurrently read multiple audio/video files you input, convert them into real-time recognition results independently, and callback each result separately through callback functions.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
