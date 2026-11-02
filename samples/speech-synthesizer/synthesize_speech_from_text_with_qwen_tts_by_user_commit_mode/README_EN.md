## Text-to-Speech Synthesis and Playback (commit mode)

English | [简体中文](./README.md)

This example demonstrates how to synthesize speech from specified text, stream the returned audio, and play it in real-time. This example also shows how to save the audio to a file during the streaming callback.

### :point_right: Applicable Scenarios

| Application Scenario | Typical Use | Usage Description |
| ----- | ----- | ----- |
| **Call Center Scenario** | Agent Response to Speech | *Use text-to-speech to convert customer service bot responses into real-time voice broadcasts* |
| **Digital Human Scenario** | News Broadcasting | *In news or similar scenarios, use speech synthesis to broadcast textual information* |

### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

### :point_right: Reference Details
| Language | Recommended Model | API Details |
| --- | --- | --- |
| Python | **qwen-audio-3.0-tts-flash** | [Official documentation](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime) |
| Java | **qwen-tts-realtime** | [Official documentation](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime) |

### :point_right: Expected Results

The Python example uses the `longanfengyue` voice, while the Java example uses `Chelsie`. The synthesized audio is streamed and played through the speaker.

When synthesizing streaming text, the `commit` mode is used, where users actively control when input buffers are submitted. This mode is suitable for advanced users or systems with extremely low latency requirements, but you need to manage sentence integrity and synthesis points yourself, which may affect synthesis quality.

### :point_right: Technical Support
<img src="../../../docs/image/group.png" width="400"/>
