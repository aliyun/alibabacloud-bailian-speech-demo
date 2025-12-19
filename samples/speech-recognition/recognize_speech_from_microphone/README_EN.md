[comment]: # (title and brief introduction of the sample)
## Microphone Real-time Speech Recognition

English | [简体中文](./README.md)

This example demonstrates how to record audio from a microphone, send the captured audio stream to Alibaba Cloud's Bailian model service for real-time speech recognition. When running the example, what the user says into the microphone will be displayed on the screen in real-time. We use VAD (Voice Activity Detection) sentence segmentation to achieve faster response speed.

[comment]: # (list of scenarios of the sample)
### :point_right: Applicable Scenarios

| Application Scenario     | Typical Use | Usage Description |
|----------| ----- | ----- |
| **Getting Started Scenario** | Microphone Speech Recognition | *Real-time recording from microphone and speech recognition* |
| **Call Center Robot and Dialogue Analysis Understanding Scenario** | Real-time Call Speech Recognition | *Real-time speech recognition for call system conversations* |
| **Meeting Speech Analysis Understanding Scenario** | Real-time Meeting Speech Recognition	 | *Real-time speech recognition for meeting audio* |

[comment]: # (supported programming languages of the sample)
### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: Reference Details

| Recommended Model | API Details |
| ----- | ----- |
| **fun-asr-realtime** | [Fun-ASR Real-time Speech Recognition API Details](https://help.aliyun.com/zh/model-studio/fun-asr-real-time-speech-recognition-api-reference/) |
| **paraformer-realtime-v2**<br>paraformer-realtime-v1<br>paraformer-realtime-8k-v1 | [Paraformer Real-time Speech Recognition API Details](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-real-time-speech-recognition-api) |

### :point_right: Expected Results

Running the example will prompt you to start speaking. Enter 'Ctrl+C' in the console to stop recording and recognition. The recognized text will be printed in the console:
```text
Press 'Ctrl+C' to stop recording and recognition
RecognitionCallback text:  一
RecognitionCallback text:  1234
```

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>