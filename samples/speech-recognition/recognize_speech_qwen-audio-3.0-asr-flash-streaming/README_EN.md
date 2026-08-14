[comment]: # (title and brief introduction of the sample)
## Real-Time Streaming Speech Recognition with Qwen-Audio-3.0-ASR-Flash-Streaming

English | [简体中文](./README.md)

This example demonstrates how to perform **real-time streaming** speech recognition using the **`qwen-audio-3.0-asr-flash-streaming`** model on Alibaba Cloud Bailian. Based on the **WebSocket** protocol, this model supports **unlimited duration** audio streams, offers robust multilingual and dialect recognition, and enhances accuracy via **Prompt Context** and **Hotwords**, making it ideal for low-latency scenarios like live captions and real-time meeting transcription.

[comment]: # (list of scenarios of the sample)
### :point_right: Applicable Scenarios

| Application Scenario     | Typical Use      | Key Benefits            |
|----------|-----------|-----------------|
| **Real-Time Live/Meeting Captions** | Live Streaming/Remote Meetings/Classroom Recording | *WebSocket-based long connection with millisecond-level latency, supporting unlimited audio duration*  |
| **Vertical Domain Real-Time Interaction** | Smart Customer Service/Voice Assistant | *Supports custom Hotwords and Prompt Context to significantly improve real-time accuracy for specialized terms*  |
| **Multilingual/Dialect Real-Time Transcription** | International Broadcasts/Dialect Communication | *Supports real-time mixed recognition of 30+ languages including Chinese dialects (Cantonese, Wu, Sichuanese, etc.), English, Japanese, Korean, and more*  |

[comment]: # (supported programming languages of the sample)
### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

### :point_right: Related Examples

This example shows **only the most basic streaming recognition**: read a local audio file, send it frame by frame, and print the result in real time. Two advanced capabilities have been split into dedicated examples:

| Capability | Example |
| --- | --- |
| **Conversation Context** | [Pass dialog history or a domain word list to improve accuracy, with limit-aware trimming](../recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-context) |
| **Precompiled Vocabulary** | [Create a vocabulary once, reuse by id, manage its full lifecycle](../recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-vocabulary) |

> :warning: **This example requires the `DASHSCOPE_WORKSPACE_ID` environment variable.** The qwen-audio series models are served under the workspace-specific endpoint `https://{WORKSPACE_ID}.cn-beijing.maas.aliyuncs.com`; without it the example prints a hint and exits.

[comment]: # (model and interface of the sample)
### :point_right: Reference Details

| Recommended Model | Mode | API Type | Key Features |
| ----- | ----- | ----- | ----- |
| **qwen-audio-3.0-asr-flash-streaming** | Real-Time | WebSocket | Hotwords, Prompt Context, Multilingual/Dialects, **Unlimited Duration** |

🔗 **API Documentation**: [Qwen-Audio Real-Time Speech Recognition API Reference](https://help.aliyun.com/en/model-studio/real-time-speech-recognition-user-guide)

### :point_right: Model Capabilities Overview

*   **Supported Languages**: 
    *   **Chinese & Dialects**: Mandarin, Cantonese, Wu, Minnan, Hakka, Gan, Xiang, Jin; covering Central Plains, Southwest, Jilu, Jianghuai, Lanyin, Jiaoliao, Northeast, Beijing, Hong Kong/Taiwan accents and regional official dialects.
    *   **Foreign Languages**: English, Japanese, Korean, Vietnamese, Thai, Indonesian, Malay, Filipino, Hindi, Arabic, French, German, Spanish, Portuguese, Russian, Italian, Dutch, Swedish, Danish, Finnish, Norwegian, Greek, Polish, Czech, Hungarian, Romanian, Bulgarian, Croatian, Slovak.
*   **Accuracy Enhancement**: Supports `hotwords` and `prompt` (context) parameters to optimize recognition for specific scenarios.
*   **Duration Limit**: **Unlimited** (Subject to network stability and session keep-alive policies).

### :point_right: Expected Results

#### 1. Real-Time Streaming Result
The console will print incremental recognition text in real-time, eventually merging into complete sentences:

```text
 Starting Real-Time Streaming Recognition...
[Stream] Hello
[Stream] , welcome
[Stream] to Alibaba Cloud
[Stream] Tongyi Qianwen
[Stream] ...
✅ Recognition Ended!
📝 Final Full Text: 
Hello, welcome to Alibaba Cloud Tongyi Qianwen Audio Large Model. This is a sample for testing real-time streaming recognition.

[Metric] RequestId: xxx-xxx, First Token Latency: 150ms
```


[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../docs/image/group.png" width="400"/>