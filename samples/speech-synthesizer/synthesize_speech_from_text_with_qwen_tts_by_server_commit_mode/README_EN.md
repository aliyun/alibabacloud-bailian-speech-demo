## Text-to-Speech Synthesis and Playback (server commit mode)

English | [简体中文](./README.md)

This example demonstrates how to synthesize speech from a specified text, stream the returned audio, and play it in real time. This example also shows how to save the audio to a file during streaming callbacks.

### :point_right: Applicable Scenarios

| Application Scenario | Typical Use Case | Usage Description |
| ----- | ----- | ----- |
| **Call Center Scenario** | Agent Response to Speech | *Use text-to-speech to provide real-time voice announcements for customer service robot responses* |
| **Digital Human Scenario** | News Broadcasting | *In news scenarios, use speech synthesis to broadcast textual information* |

### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

### :point_right: Reference Details
| Recommended Model | API Details |
| --- | --- |
| **qwen-tts-realtime** | [官方文档](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime) |

### :point_right: Expected Results

When running this example, it will use the Chelsie voice to synthesize the sample text stream. The synthesized audio will be delivered in a streaming manner and played through the speaker.

During the streaming text synthesis, the `server_commit` mode is used, which allows the server to control the accumulation and submission logic of the text. Users only need to continuously input the text, and the system automatically determines when to start the synthesis, balancing synthesis quality and response latency. It is suitable for most developers.

### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
