## Batch Audio/Video File Rich Information Speech Recognition (Batch Mode)

English | [简体中文](./README.md)

This example demonstrates how to submit audio/video file URLs stored in cloud storage (e.g., OSS) and invoke the offline file transcription API of Alibaba Cloud's Bailian large speech recognition model to achieve batch speech recognition.

By using the SenseVoice large speech model, multi-language speech can be recognized while simultaneously returning rich information such as emotions and audio events. The **Rich Information Speech Recognition** for audio/video files is more suitable for scenarios requiring recognition of richer languages, emotions, audio events, etc. For general audio/video file speech recognition scenarios, it is recommended to use the more cost-effective Paraformer model. Please refer to the example: [Batch Audio/Video File Speech Recognition (Batch Mode)](../recognize_speech_from_files_by_batch_mode/).

> The Python example uses the DashScope SDK 2.0.2 `Client`/v2 API. Because the v2 batch transcription endpoint does not currently expose `sensevoice-v1`, it uses `qwen-audio-3.1-asr-flash-filetrans`, submits one URL per task, and demonstrates the file transcription flow. The Java example continues to use `sensevoice-v1` for rich-information recognition.

### :point_right: Applicable Scenarios

| Application Scenario           | Typical Use | Usage Description                 |
|----------------| ----- |----------------------|
| **Audio/Video Speech Analysis and Understanding Scenario**   | Batch Rich Text Speech Recognition | *Recognize text/emotions/events in audio/video files* |


### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

### :point_right: Reference Details

| Language | Recommended Model | API Details | Model Features |
| --- | --- | --- | --- |
| Python | **qwen-audio-3.1-asr-flash-filetrans** | File transcription `Client`/v2 API | One recorded-file URL per task |
| Java | **sensevoice-v1** | [SenseVoice Recording File Speech Recognition](https://help.aliyun.com/zh/model-studio/developer-reference/sensevoice-api) | Up to 50+ languages <br/> Emotion recognition <br/> Audio event detection |

### :point_right: Expected Results
The Python version submits a separate transcription task for each `file_url` and waits for completion; the Java version submits the file list.

After recognition completes, the service returns a `transcription_url` for each submitted file. The example downloads the result and prints each file's recognized content in the console.

### :point_right: Technical Support
<img src="../../../docs/image/group.png" width="400"/>
