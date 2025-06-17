[comment]: # (title and brief introduction of the sample)
## Microphone Real-time Speech Translation

English | [简体中文](./README.md)

This example demonstrates how to record audio from a microphone, send the captured audio stream to Alibaba Cloud's Bailian model service for real-time speech translation. When running the example, what the user says into the microphone will be translated to English and displayed on the screen in real-time.

[comment]: # (list of scenarios of the sample)
### :point_right: Applicable Scenarios

| Application Scenario     | Typical Use | Usage Description |
|----------| ----- | ----- |
| **Getting Started Scenario** | Microphone Speech Translation | *Real-time recording from microphone and speech translation* |
| **Real-time Bilingual Subtitles** | Automatically Generate Audio/Video Subtitles in Different Languages | *Perform real-time speech recognition and translation on video streams to generate bilingual subtitles* |
| **Meeting Speech Analysis Understanding Scenario** | Real-time Meeting Speech Recognition | *Perform real-time speech recognition and translation on meeting audio* |

[comment]: # (supported programming languages of the sample)
### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: Reference Details

| Recommended Model | API Details |
| ----- | ----- |
| **gummy-realtime-v1** | [Paraformer Real-time Speech Recognition API Details (TODO: Update)](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-real-time-speech-recognition-api) |

### :point_right: Expected Results

Running the example will prompt you to start speaking in the console. Enter 'Ctrl+C' in the console to stop recording and recognition. The recognition results will be printed in the console:
```text
Press 'Ctrl+C' to stop recording and recognition
RecognitionCallback text:  一
translate to en: The.
translate to en: The.
translate to en: The.
translate to en: The.
translate to en: This is
translate to en: This is a sentence
translate to en: This is a test audio.
translate to en: This is a test audio.
```

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>