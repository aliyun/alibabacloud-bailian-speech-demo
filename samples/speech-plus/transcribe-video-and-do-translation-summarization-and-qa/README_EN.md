[comment]: # (title and brief introduction of the sample)
## Video Transcription with Translation, Summary, and Q&A

English | [简体中文](./README.md)

This example demonstrates converting a video file into an OPUS audio file, transcribing it through audio file recognition services, and then using the Qwen large language model for translation, content summarization, and question-answering.

[comment]: # (list of scenarios of the sample)
### :point_right: Applicable Scenarios

| Application Scenario           | Typical Use | Usage Description                 |
|----------------| ----- |----------------------|
| **Audio/Video Speech Analysis and Understanding**   | Audio/Video Summary and Q&A | *Perform speech recognition on audio/video files and use large models for summarization and Q&A* |

[comment]: # (supported programming languages of the sample)
### :point_right: Programming Languages
- [Python](./python)


[comment]: # (model and interface of the sample)
### :point_right: Reference Details

| Recommended Model          | API Details                                                                                             |
|---------------|---------------------------------------------------------------------------------------------------|
| paraformer-v2 | [Paraformer Audio File Recognition](https://help.aliyun.com/zh/dashscope/developer-reference/api-details-13)|
| qwen-plus | [Qwen Large Language Model](https://help.aliyun.com/zh/model-studio/developer-reference/what-is-qwen-llm?spm=a2c4g.11186623.0.0.5dbb76776EGFHK)|

[comment]: # (dependency of the sample)
### :point_right: Dependency Description

In this example, we first demonstrate converting a video file into an [OPUS](https://opus-codec.org/) format audio file and uploading it to OSS for service invocation. This preprocessing step significantly reduces storage and network transmission costs while improving transcription throughput efficiency. For this process, we use FFmpeg for audio encoding and OSS as cloud storage and distribution service. Below are the details:

1. Install FFmpeg: Please visit the [FFmpeg official website](https://www.ffmpeg.org/download.html) to download.
2. Use OSS: Please activate and configure the service at [Alibaba Cloud OSS](https://help.aliyun.com/zh/oss/getting-started/getting-started-with-oss). This example provides a simple utility class [ossUtil.py](./python/ossUtil.py) for uploading files to OSS and obtaining shared links. Configure your authentication and bucket information to use it.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
