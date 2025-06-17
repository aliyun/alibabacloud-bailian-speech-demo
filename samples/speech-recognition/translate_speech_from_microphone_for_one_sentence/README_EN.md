[comment]: # (title and brief introduction of the sample)
## Microphone Real-time Sentence-level Speech Recognition and Translation

English | [简体中文](./README.md)

This example demonstrates how to record audio from a microphone, send the captured audio stream to Alibaba Cloud's Bailian model service for real-time sentence-level speech translation. When running the example, the first sentence spoken into the microphone will be translated to English and displayed on the screen in real-time.

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

Running the example will prompt you to start speaking in the console. The service will use VAD (Voice Activity Detection) to determine when to stop recording - recording will automatically stop when you finish speaking. Recognition results will be printed in the console, and the recorded audio will be saved to a `request_id_record.pcm` file.
```text
	[log] Initializing ...
	[log] TranslationRecognizerCallback open.
	[log] Recording...
	[log] Translation started, request_id: a66eac0a04a24dddadeca3acc4a64c01
translation will stop after recording one sentence...
- - - - - - - - - - -
[2024-12-19 14:00:06.757] transcript : 测试一
[2024-12-19 14:00:06.757] translate to en: Test
- - - - - - - - - - -
[2024-12-19 14:00:06.956] transcript : 测试一
[2024-12-19 14:00:06.956] translate to en: Test
- - - - - - - - - - -
[2024-12-19 14:00:07.154] transcript : 测试一
[2024-12-19 14:00:07.154] translate to en: Test
- - - - - - - - - - -
[2024-12-19 14:00:07.353] transcript : 测试一句话识别。
[2024-12-19 14:00:07.353] translate to en: Test sentence recognition.
- - - - - - - - - - -
[2024-12-19 14:00:07.553] transcript : 测试一句话识别。
[2024-12-19 14:00:07.554] <=== [vad pre_end] silence start at 1560 ms, detected at 2000 ms ===>
[2024-12-19 14:00:07.554] translate to en: Test sentence recognition.
- - - - - - - - - - -
[2024-12-19 14:00:07.955] transcript : 测试一句话识别。
[2024-12-19 14:00:07.955] translate to en: Test sentence recognition.
- - - - - - - - - - -
[2024-12-19 14:00:08.157] transcript : 测试一句话识别。
[2024-12-19 14:00:08.157] translate to en: Test sentence recognition.
request id: a66eac0a04a24dddadeca3acc4a64c01 usage: {'duration': 4}
	[log] sentence end, stop sending
	[log] Translation completed.
	[log] TranslationRecognizerCallback close.
    [log] Recorded audio saved to a66eac0a04a24dddadeca3acc4a64c01_record.pcm
```

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>