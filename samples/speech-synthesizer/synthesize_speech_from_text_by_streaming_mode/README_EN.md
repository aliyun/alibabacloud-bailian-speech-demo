## Speech Synthesis and Playback (Streaming Mode)

English | [简体中文](./README.md)

This example demonstrates how to synthesize speech from specified text, stream the returned audio in real-time for playback. It also demonstrates how to save audio to a file during the streaming callback.

### :point_right: Applicable Scenarios

| Application Scenario | Typical Usage | Usage Instructions |
| ----- | ----- | ----- |
| **Call Center Scenario** | Convert customer service replies to voice | *Use text-to-speech to provide real-time voice announcements for customer service bots* |
| **Digital Human Scenario** | News broadcasting | *In news scenarios, use speech synthesis to broadcast text information* |

### :point_right: Supported Programming Languages
- [Python](./python)
- [Java](./java)

### :point_right: Reference Details
| Recommended Model | API Details |
| --- | --- |
| **cosyvoice-v1** | [CosyVoice Large Model Speech Synthesis API Details](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [Voice Style List](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#915a935d871ak) |
| **cosyvoice-v2** | [CosyVoice Large Model Speech Synthesis API Details](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [Voice Style List](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#da9ae03e5ek7b) |
| **cosyvoice-v3-flash** | [CosyVoice LLM Speech Synthesis API](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [Voice Tone List](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#95303fd00f0ge) |
| **cosyvoice-v3-plus** | [CosyVoice LLM Speech Synthesis API](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [Voice Tone List](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#95303fd00f0ge) |

### :point_right: Expected Results
When running the example, it will synthesize the sample text "Time flies so fast! Yesterday when we video chatted, seeing your proud and satisfied smile made my heart as sweet as drinking a bottle of honey! I'm truly happy for you!" using the longanhuan voice style. The synthesized audio will be streamed, played through the speaker, and saved to the file `result.mp3`.

### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
