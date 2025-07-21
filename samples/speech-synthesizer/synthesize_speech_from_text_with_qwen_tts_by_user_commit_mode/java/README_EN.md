## Text-to-Speech Synthesis and Playback (commit mode)

English | [简体中文](./README.md)

## Java

### :point_right: Prerequisites

1. #### Configure Alibaba Cloud Bailing API-KEY

    Before running this example, you need to create an Alibaba Cloud account, obtain the Alibaba Cloud Bailing API_KEY, and perform necessary environment configuration. For detailed steps on configuring the API-KEY, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### Java Runtime Environment

   Before running this example, you need to install the Java runtime environment and the Maven build tool.

### :point_right: How to Run the Sample

You can run this example by executing `run.sh` (for Linux and Mac systems) or `run.bat` (for Windows systems).

When running the example, it will use the Chelsie voice to synthesize a stream of sample text. The synthesized audio will be delivered in a streaming manner and played through the speaker.

When synthesizing streaming text, the `commit` mode is used, where users actively control when input buffers are submitted. This mode is suitable for advanced users or systems with extremely low latency requirements, but you need to manage sentence integrity and synthesis points yourself, which may affect synthesis quality.

You can modify the `text_to_synthesize` variable to specify the text to be synthesized.

### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
