[comment]: # (title and brief introduction of the sample)
## Batch Audio/Video File Speech Recognition (Batch Mode)

English | [简体中文](./README.md)

This example demonstrates how to submit a large number of audio/video file URLs stored in cloud storage (e.g., OSS) and invoke Alibaba Cloud's Bailian speech recognition large model offline file transcription API to achieve batch speech recognition.

The audio file recognition service supports more audio/video formats and provides more accurate, information-rich recognition results for users. The **batch mode** of audio/video file speech recognition is more suitable for scenarios involving production tasks with large volumes of cloud files where immediate results are not required. If you need to process local files and expect immediate results, please refer to the example: [Batch Audio/Video File Speech Recognition (Real-time Mode)](../recognize_speech_from_files_by_realtime_mode/).

[comment]: # (list of scenarios of the sample)
### :point_right: Applicable Scenarios

| Application Scenario           | Typical Use | Usage Description                 |
|----------------| ----- |----------------------|
| **Audio/Video Speech Analysis and Understanding Scenario**   | Batch Speech Recognition for Audio/Video | *Perform batch speech recognition on audio/video files* |
| **Meeting Speech Analysis and Understanding Scenario** | Batch Speech Recognition for Meeting Recordings	 | *Perform batch speech recognition on meeting recording files*    |
| **Call Center Robot and Dialogue Analysis Understanding Scenario**| Batch Speech Recognition for Call Recordings		 | *Perform batch speech recognition on call center recording files*     |

[comment]: # (supported programming languages of the sample)
### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: Reference Details

| Recommended Model                                                        | API Details                                                                                             |
|-------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| **fun-asr**  | [Fun-ASR Audio File Recognition API Details](https://help.aliyun.com/zh/model-studio/fun-asr-recorded-speech-recognition-api-reference/)|
| **paraformer-v2**<br/> paraformer-v1<br/> paraformer-8k-v1 <br/>paraformer-mtl-v1  | [Audio File Recognition API Details](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-api)|

### :point_right: Expected Results

Running the example will access the file transcription service, submit your input file list, and wait for recognition completion.

Upon completion, the service will return submitted files ```file_url``` and corresponding recognition result file links ```transcription_url``` in JSON list format. You can copy the printed links from the console to open or download them in your browser.

[comment]: # (best practices)
### :point_right: Best Practices

Although Alibaba Cloud's Bailian speech recognition large model file transcription API supports multiple audio/video formats, since video files are typically large and transmission is time-consuming, it is recommended to preprocess them by extracting only the required audio tracks and compressing them reasonably to significantly reduce file size. This will greatly improve the throughput efficiency of video file transcription. The following steps demonstrate how to use ffmpeg for such preprocessing:

1. Install ffmpeg: Please visit the [official ffmpeg website](https://www.ffmpeg.org/download.html). Also refer to the documentation [How to Install ffmpeg](../../../docs/QA/ffmpeg_en.md).

2. Preprocess video files: Use ffmpeg to extract audio tracks, downsample to 16kHz 16bit Mono, and compress encode as opus files:
    ```
    ffmpeg -i input-video-file -ac 1 -ar 16000 -acodec libopus output-audio-file.opus
    ```

3. Upload the compressed pure audio file ```output-audio-file.opus``` to cloud storage and obtain its URL. Submit this URL to Alibaba Cloud Bailian file transcription service.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
