[comment]: # (title and brief introduction of the sample)
## High-Precision Non-Streaming Speech Recognition with Qwen-Audio-3.0-ASR-Flash

English | [简体中文](./README.md)

This example demonstrates how to perform **non-streaming** speech recognition using the **`qwen-audio-3.0-asr-flash`** model on Alibaba Cloud Bailian. This model supports audio files up to **2GB** or **5 minutes** in length, offers robust multilingual and dialect recognition, and enhances accuracy via **Prompt Context** and **Hotwords**.

[comment]: # (list of scenarios of the sample)
### :point_right: Applicable Scenarios

| Application Scenario     | Typical Use      | Key Benefits            |
|----------|-----------|-----------------|
| **High-Precision Short Audio Transcription** | Meeting Recordings/Interviews/Podcast Clips | *Supports audio up to 5 mins/2GB, providing sentence-level timestamps and high-accuracy text*  |
| **Vertical Domain Optimization** | Medical/Legal/Financial Terminology | *Supports custom Hotwords and Prompt Context to significantly improve accuracy for specialized terms*  |
| **Multilingual/Dialect Processing** | International Meetings/Regional Dialects | *Supports 30+ languages including Chinese dialects (Cantonese, Wu, Sichuanese, etc.), English, Japanese, Korean, and more*  |

[comment]: # (supported programming languages of the sample)
### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: Reference Details

| Recommended Model | Mode | API Type | Key Features |
| ----- | ----- | ----- | ----- |
| **qwen-audio-3.0-asr-flash** | Non-Streaming | HTTP | Hotwords, Prompt Context, Multilingual/Dialects, Max 5 mins/2GB |

🔗 **API Documentation**: [Qwen-Audio-3.0  Speech Recognition API Reference](https://help.aliyun.com/en/model-studio/non-realtime-speech-recognition-user-guide#nrt02-funasr-flash-h2)

### :point_right: Model Capabilities Overview

*   **Supported Languages**: 
    *   **Chinese & Dialects**: Mandarin, Cantonese, Wu, Minnan, Hakka, Gan, Xiang, Jin; covering Central Plains, Southwest, Jilu, Jianghuai, Lanyin, Jiaoliao, Northeast, Beijing, Hong Kong/Taiwan accents and regional official dialects.
    *   **Foreign Languages**: English, Japanese, Korean, Vietnamese, Thai, Indonesian, Malay, Filipino, Hindi, Arabic, French, German, Spanish, Portuguese, Russian, Italian, Dutch, Swedish, Danish, Finnish, Norwegian, Greek, Polish, Czech, Hungarian, Romanian, Bulgarian, Croatian, Slovak.
*   **Accuracy Enhancement**: Supports `hotwords` and `prompt` (context) parameters to optimize recognition for specific scenarios.
*   **Limits**: Maximum audio duration **5 minutes** or maximum file size **2GB**.

### :point_right: Expected Results

#### 1. Basic Recognition Result
The console will print the recognized plain text and request latency:

```text
✅ Recognition Successful!
📝 Recognized Text: 
Hello, welcome to Alibaba Cloud Tongyi Qianwen Audio Large Model. This is a sample for testing high-precision synchronous recognition.

[Metric] RequestId: xxx-xxx, Latency: 1200ms
```


[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../docs/image/group.png" width="400"/>