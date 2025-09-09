## Clone Your Voice for Speech Synthesis and Playback (Streaming Mode)

English | [简体中文](./README.md)

This example demonstrates how to record audio according to instructions, clone your own voice style, and synthesize speech from specified text. The example will stream the returned audio for real-time playback. It also demonstrates how to save audio to a file during the streaming callback.

### :point_right: Applicable Scenarios

| Application Scenario | Typical Usage | Usage Instructions |
| ----- | ----- | ----- |
| **Call Center Scenario** | Convert customer service replies to voice | *Use custom voice style text-to-speech for real-time voice announcements of customer service bots* |
| **Digital Human Scenario** | News broadcasting | *Use custom voice style in news scenarios, use speech synthesis to broadcast text information* |

### :point_right: Supported Programming Languages
- [Python](./python)
- [Java](./java)

### :point_right: Reference Details
| Recommended Model | API Details |
| --- | --- |
| **cosyvoice-v1** | [CosyVoice Large Model Speech Synthesis API Details](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [Voice Style List](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#915a935d871ak) |
| **cosyvoice-v2** | [CosyVoice Large Model Speech Synthesis API Details](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [Voice Style List](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#da9ae03e5ek7b) |
| **cosyvoice-v3** | [CosyVoice Large Model Speech Synthesis API Details](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [Voice Style List](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#95303fd00f0ge) |

Note: ⚠️ The cosyvoice-v3 model series is currently in open beta (visible to all, requires application) - [Apply here](https://bailian.console.aliyun.com/?tab=model#/model-market/detail/group-cosyvoice?modelGroup=group-cosyvoice). Free quotas will be granted upon approval.


### :point_right: Expected Results

This example consists of two parts: recording audio and cloning voice style.

#### Audio Recording
When running the example, it will start recording. Please follow the prompts to record an audio clip for cloning, which will be saved in `your_record_file.wav`. Please use Alibaba Cloud OSS or other cloud storage methods to obtain a downloadable HTTP link.

#### Voice Style Cloning
When running the example, it will create a cloned voice style based on your recording, and use the cloned voice style to synthesize the sample text "Hello, I'm now reading this paragraph with your cloned voice~". The synthesized audio will be streamed, played through the speaker, and saved to the file `result.mp3`.

### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
