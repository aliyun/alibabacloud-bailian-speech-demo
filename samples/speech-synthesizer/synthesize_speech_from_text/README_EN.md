## Speech Synthesis and Save File (Simple Mode)

English | [简体中文](./README.md)

This example demonstrates how to synthesize speech from specified text and save it as a file. The **simple mode** of speech synthesis saves the synthesized speech as a file, suitable for scenarios without real-time playback requirements. For real-time playback, please refer to [Speech Synthesis and Playback (Streaming Mode)](../synthesize_speech_from_text_by_streaming_mode/).

### :point_right: Applicable Scenarios

| Application Scenario | Typical Usage | Usage Instructions |
| ----- | ----- | ----- |
| **Entry-level Scenario** | Single-sentence synthesis | *Convert a text segment into speech* |
| **Video Dubbing Scenario** | Video dubbing, news narration | *Use speech synthesis to broadcast subtitles or text content in videos* |
| **Audiobook Scenario** | Novel dubbing, picture book narration | *Assign different voice styles to characters, read novels/picture books as audiobooks* |

### :point_right: Programming Languages
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
When running the example, it will synthesize the sample text "想不到时间过得这么快！昨天和你视频聊天，看到你那自豪又满意的笑容，我的心里呀，就如同喝了一瓶蜜一样甜呢！真心为你开心呢！" using the longanhuan voice style and save it to the `result.mp3` file.

### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
