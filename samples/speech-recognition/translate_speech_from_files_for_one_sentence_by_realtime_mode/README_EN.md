[comment]: # (title and brief introduction of the sample)
## Batch Audio File Sentence-level Speech Recognition and Translation (Real-time Mode)

English | [简体中文](./README.md)

This example demonstrates how to batch call a sentence-level speech translation interface to process multiple file streams and return recognition results for each file in real-time.

The **real-time mode** of audio file sentence-level speech recognition and translation is more suitable for processing local files with immediate result returns, or building streaming audio services that collect frontend audio streams and return recognition results instantly.

If you use Java to build a speech service, refer to [High Concurrency Example Documentation](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-in-high-concurrency-scenarios) for optimal performance.

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
| **gummy-chat-v1** | [Paraformer Real-time Speech Recognition API Details (TODO: Update)](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-real-time-speech-recognition-api) |


### :point_right: Expected Results

Running the example will output streaming recognition results in the console. Each file's recognition corresponds to a [process id], and incremental results will be returned continuously. For example:

```
translation with file :asr_example_chat.wav
[process 92485] TranslationRecognizerCallback open.
translation with file :asr_example_chat.wav
[process 92483] TranslationRecognizerCallback open.
[process 92483] Transcript ==>  hello,word这里是阿里巴巴语音实验室。
[process 92483] Translate ==>  Hello world, this is the Alibaba Speech Lab.
[process 92483] Translation completed
[process 92485] Transcript ==>  hello,word,这里是阿里巴巴语音实验室。
[process 92485] Translate ==>  Hello, world. This is the Alibaba Speech Lab.
[process 92485] Translation completed
[process 92483] TranslationRecognizerCallback close.
[Metric] requestId: xxxxxxxx, first package delay ms: 444.7109375, last package delay ms: 665.9140625
[process 92485] TranslationRecognizerCallback close.
[Metric] requestId: xxxxxxxx, first package delay ms: 626.47509765625, last package delay ms: 963.182861328125
```

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>