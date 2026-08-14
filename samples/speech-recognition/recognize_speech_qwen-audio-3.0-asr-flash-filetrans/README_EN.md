[comment]: # (title and brief introduction of the sample)
## Long Audio Asynchronous Transcription with Speaker Diarization using Qwen-Audio-3.0-ASR-Flash-Filetrans

English | [简体中文](./README.md)

This example demonstrates how to perform **non-real-time (asynchronous)** speech recognition on **long audio files** using the **`qwen-audio-3.0-asr-flash-filetrans`** model on Alibaba Cloud Bailian. Based on the **HTTP** protocol, this model supports massive audio files up to **12 hours** or **2GB**, offers robust multilingual and dialect recognition, features built-in **Speaker Diarization**, and enhances accuracy via **Prompt Context** and **Hotwords**.

[comment]: # (list of scenarios of the sample)
### :point_right: Applicable Scenarios

| Application Scenario     | Typical Use      | Key Benefits            |
|----------|-----------|-----------------|
| **Ultra-Long Audio Offline Transcription** | All-day Meetings/Lectures/Court Recordings | *Supports huge audio files up to 12 hrs/2GB, asynchronous processing prevents blocking, providing high-accuracy text*  |
| **Multi-Speaker Dialogue Analysis** | Interviews/Roundtables/Customer Service QA | *Built-in **Speaker Diarization** automatically distinguishes different speakers (e.g., Speaker A, Speaker B), facilitating easy organization*  |
| **Vertical Domain High-Precision Transcription** | Medical/Legal/Financial Archive Digitization | *Supports custom Hotwords and Prompt Context to significantly improve accuracy for specialized terms*  |

[comment]: # (supported programming languages of the sample)
### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: Reference Details

| Recommended Model | Mode | API Type | Key Features |
| ----- | ----- | ----- | ----- |
| **qwen-audio-3.0-asr-flash-filetrans** | Non-Real-Time (Asynchronous) | HTTP | Hotwords, Prompt Context, **Speaker Diarization**, Multilingual/Dialects, Max 12 hrs/2GB |

🔗 **API Documentation**: [Qwen-Audio File Transcription API Reference](https://help.aliyun.com/en/model-studio/non-realtime-speech-recognition-user-guide)

### :point_right: Model Capabilities Overview

*   **Supported Languages**: 
    *   **Chinese & Dialects**: Mandarin, Cantonese, Wu, Minnan, Hakka, Gan, Xiang, Jin; covering Central Plains, Southwest, Jilu, Jianghuai, Lanyin, Jiaoliao, Northeast, Beijing, Hong Kong/Taiwan accents and regional official dialects.
    *   **Foreign Languages**: English, Japanese, Korean, Vietnamese, Thai, Indonesian, Malay, Filipino, Hindi, Arabic, French, German, Spanish, Portuguese, Russian, Italian, Dutch, Swedish, Danish, Finnish, Norwegian, Greek, Polish, Czech, Hungarian, Romanian, Bulgarian, Croatian, Slovak.
*   **Accuracy Enhancement**: Supports `hotwords` and `prompt` (context) parameters to optimize recognition for specific scenarios.
*   **Speaker Diarization**: Automatically identifies and labels segments from different speakers (e.g., `Speaker 1: ...`, `Speaker 2: ...`).
*   **Limits**: Maximum audio duration **12 hours** or maximum file size **2GB**.

### :point_right: Expected Results

#### 1. Basic Recognition Result (with Speaker Diarization)
After task completion, the console will print recognized text with speaker labels:

```text
✅ Asynchronous Task Completed!
📝 Recognized Text (with Speaker Diarization): 

[Speaker 1] Hello everyone, welcome to today's quarterly summary meeting.
[Speaker 2] Thank you, host. I'll start by reporting the sales department's data.
[Speaker 1] Okay, please proceed.
[Speaker 2] This quarter, our revenue grew by...

[Metric] Task ID: xxx-xxx, Duration: 45m, Status: SUCCEEDED
```

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../docs/image/group.png" width="400"/>