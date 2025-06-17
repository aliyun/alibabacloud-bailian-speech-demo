## Batch Audio/Video File Rich Information Speech Recognition (Batch Mode)

English | [简体中文](./README.md)

This example demonstrates how to submit audio/video file URLs stored in cloud storage (e.g., OSS) and invoke the offline file transcription API of Alibaba Cloud's Bailian large speech recognition model to achieve batch speech recognition.

By using the SenseVoice large speech model, multi-language speech can be recognized while simultaneously returning rich information such as emotions and audio events. The **Rich Information Speech Recognition** for audio/video files is more suitable for scenarios requiring recognition of richer languages, emotions, audio events, etc. For general audio/video file speech recognition scenarios, it is recommended to use the more cost-effective Paraformer model. Please refer to the example: [Batch Audio/Video File Speech Recognition (Batch Mode)](../recognize_speech_from_files_by_batch_mode/).

### :point_right: Applicable Scenarios

| Application Scenario           | Typical Use | Usage Description                 |
|----------------| ----- |----------------------|
| **Audio/Video Speech Analysis and Understanding Scenario**   | Batch Rich Text Speech Recognition | *Recognize text/emotions/events in audio/video files* |


### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

### :point_right: Reference Details

| Recommended Model | API Details  | Model Features                              |
| ----- |--------------------------|-----------------------------------|
| **sensevoice-v1** | [SenseVoice Recording File Speech Recognition](https://help.aliyun.com/zh/model-studio/developer-reference/sensevoice-api) | Up to 50+ languages <br/> Emotion recognition <br/> Audio event detection |

### :point_right: Expected Results
Running the example will access the file transcription service, submit the list of transcription files you input, and wait for the recognition to complete.

Upon completion, the service will return the submitted files ```file_url``` and corresponding transcription result file links ```transcription_url``` in a JSON list format. You can copy the printed links from the console to open or download them in your browser.

In the console, brief recognition results for each file will be printed.

### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
