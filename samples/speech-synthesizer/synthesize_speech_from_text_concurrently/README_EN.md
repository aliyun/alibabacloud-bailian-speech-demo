## Concurrent Speech Synthesis Invocation

English | [简体中文](./README.md)

This example demonstrates how to concurrently synthesize speech from multiple texts and save them as separate files.

### :point_right: Applicable Scenarios

| Application Scenario | Typical Usage | Usage Instructions |
| ----- | ----- | ----- |
| **Entry-level Scenario** | Concurrent speech synthesis invocation | *Concurrently convert text to speech* |

### :point_right: Supported Programming Languages
- [Python](./python)
- [Java](./java)

### :point_right: Reference Details
| Recommended Model | API Details |
| --- | --- |
| **cosyvoice-v1** | [CosyVoice Large Model Speech Synthesis API Details](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [Voice Style List](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#95303fd00f0ge) |
| **cosyvoice-v2** | [CosyVoice Large Model Speech Synthesis API Details](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [Voice Style List](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#da9ae03e5ek7b) |

### :point_right: Expected Results
When running the example, it will concurrently synthesize "I am <voice_style>, welcome to experience Alibaba Cloud Qwen large model speech synthesis service!" using three different voice styles and save them to `results/result_v<voice_style>_p<thread_id>.mp3` files.

### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
