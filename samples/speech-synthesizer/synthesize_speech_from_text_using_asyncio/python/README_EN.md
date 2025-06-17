## Speech Synthesis Asynchronous I/O (Streaming Mode)

English | [简体中文](./README.md)

This example demonstrates how to synthesize speech from specified text, save audio to a file in the streaming callback, and asynchronously wait for synthesis completion within a coroutine.

### :point_right: Applicable Scenarios

This example demonstrates how to use Python's `asyncio` coroutine library to asynchronously wait for speech synthesis completion while avoiding blocking the current coroutine's EventLoop. It is suitable for calling CosyVoice large model speech synthesis in asynchronous I/O programs or systems.

### :point_right: Supported Programming Languages
- [Python](./python)

### :point_right: Reference Details
| Recommended Model | API Details |
| --- | --- |
| **cosyvoice-v1** | [CosyVoice Large Model Speech Synthesis API Details](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [Voice Style List](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#95303fd00f0ge) |
| **cosyvoice-v2** | [CosyVoice Large Model Speech Synthesis API Details](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [Voice Style List](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#da9ae03e5ek7b) |

### :point_right: Expected Results
When running the example, it will synthesize the sample text "Time flies so fast! Yesterday when we video chatted, seeing your proud and satisfied smile made my heart as sweet as drinking a bottle of honey! I'm truly happy for you!" using the longhua_v2 voice style. The synthesized audio will be streamed and saved to the file `result.mp3`.

### :point_right: Asynchronous Invocation Explanation
In this example, the `async_streaming_complete` function first sends the TTS completion signal, then uses the thread-safe `ThreadSafeAsyncioEvent` to asynchronously wait for the synthesis task completion.

### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
