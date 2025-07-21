[comment]: # (title and brief introduction of the sample)
## Text-to-speech synthesis and playback (server commit mode)

English | [简体中文](./README.md)

## Java

[comment]: # (prerequisites)
### :point_right: Prerequisites

1. #### Configure Alibaba Cloud BaiLian API-KEY

    Before running this example, you need to activate an Alibaba Cloud account, obtain the Alibaba Cloud BaiLian API_KEY, and perform necessary environment configurations. For detailed steps on configuring the API-KEY, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### Java runtime environment

   Before running this example, you need to install a Java runtime environment and the Maven build tool.

[comment]: # (how to run the sample and expected results)
### :point_right: Run the example

You can run this example by executing `run.sh` (for Linux and Mac systems) or `run.bat` (for Windows systems).

When the example runs, it will use the Chelsie voice to synthesize a stream of sample text. The synthesized audio will be delivered in a streaming manner and played through the speaker.

While synthesizing the stream of text, the `server_commit` mode is used. In this mode, the server controls the accumulation and submission logic. Users only need to continuously input text; the system automatically determines when to start the synthesis, balancing synthesis quality and response latency. This mode is suitable for most developers.

You can modify `text_to_synthesize` to synthesize specific text.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
