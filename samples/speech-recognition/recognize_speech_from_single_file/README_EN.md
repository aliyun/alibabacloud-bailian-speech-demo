[comment]: # (title and brief introduction of the sample)
## Speech Recognition of a Local Single File

English | [简体中文](./README.md)

This example demonstrates how to perform speech recognition on a local audio/video file. The example reads a local WAV format audio file and calls the Alibaba Cloud Bailian speech recognition large model API to achieve speech-to-text conversion.

[comment]: # (list of scenarios of the sample)
### :point_right: Applicable Scenarios

| Application Scenario     | Typical Use      | Usage Description            |
|----------|-----------|-----------------|
| **Getting Started Scenario** | Audio/Video File Speech Recognition | *Perform speech recognition on audio/video files*  |

[comment]: # (supported programming languages of the sample)
### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: Reference Details

| Recommended Model | API Details |
| ----- | ----- |
| **fun-asr-realtime** | [Fun-ASR Real-time Speech Recognition API Details](https://help.aliyun.com/zh/model-studio/fun-asr-real-time-speech-recognition-api-reference/) |
| **paraformer-realtime-v2**<br>paraformer-realtime-v1<br>paraformer-realtime-8k-v1 | [Paraformer Real-time Speech Recognition API Details](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-real-time-speech-recognition-api) |

### :point_right: Expected Results

The complete recognition results will be saved in the ```result.json``` file in JSON format. The full results include timestamp information at both sentence and character levels. The pure text of the speech recognition will also be printed in the console:
```text
The brief result is:
Hello world, 这里是阿里巴巴语音实验室。
[Metric] requestId: 3d53b7bf-0bb2-4b4d-96e2-f42caa3eab92, first package delay ms: 1505, last package delay ms: 244
```

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>