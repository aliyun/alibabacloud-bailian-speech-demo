[comment]: # (title and brief introduction of the sample)
## Batch Audio/Video File Speech Translation (Real-time Mode)

English | [简体中文](./README.md)

This example demonstrates how to batch call real-time speech translation interfaces, process multiple file streams, and return translation results for each file in real-time.

The **real-time mode** of audio/video file speech translation is more suitable for processing local files with immediate result returns, or building streaming audio services that collect frontend audio streams and return translation results instantly.

[comment]: # (list of scenarios of the sample)
### :point_right: Applicable Scenarios

| Application Scenario     | Typical Use | Usage Description |
|----------| ----- | ----- |
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

Running the example will output streaming translation results in the console. Each file's translation corresponds to a [process id], and incremental results will be returned continuously. For example:

```
translation with file :hello_world_male_16k_16bit_mono.wav
[process 94459] TranslationRecognizerCallback open.
translation with file :hello_world_male_16k_16bit_mono.wav
[process 94461] TranslationRecognizerCallback open.
[process 94459] Transcript ==>  hello ,word,这里是阿里巴巴语音实验室。
[process 94459] Translate ==>  Hello, world. This is Alibaba's voice lab.
[process 94459] Translation completed
[process 94459] TranslationRecognizerCallback close.
[Metric] requestId: xxxxxxxxx, first package delay ms: 448.789794921875, last package delay ms: 1169.598876953125
[process 94461] Transcript ==>  hello ,word,这里是阿里巴巴语音实验室。
[process 94461] Translate ==>  Hello, world. This is Alibaba's voice lab.
[process 94461] Translation completed
[process 94461] TranslationRecognizerCallback close.
[Metric] requestId: xxxxxxxxx, first package delay ms: 409.506103515625, last package delay ms: 1175.384033203125
```


[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
