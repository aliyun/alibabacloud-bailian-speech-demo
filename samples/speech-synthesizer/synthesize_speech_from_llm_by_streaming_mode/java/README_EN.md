## Real-time LLM Output Synthesis and Playback (Streaming Mode)

English | [简体中文](./README.md)

## Java

### :point_right: Prerequisites

1. #### Configure Alibaba Cloud API-KEY

    Before running this example, you need to create an Alibaba Cloud account, obtain the API-KEY, and complete environment configuration. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### Java Runtime Environment

   Before running this example, you need to install Java runtime environment and Maven build tool.

### :point_right: How to Run the Example

You can run this example by executing run.sh (for Linux/Mac systems) or run.bat (for Windows systems).

Run the example. It will call the Alibaba Cloud Qwen (qwen-turbo) large language model to answer the question: "How to cook tomatoes with eggs?" and use the longanhuan voice to send the model's response text in streaming mode for synthesis, then stream and play the audio through the speaker.

You can modify `query_to_llm` to change the question content.

### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
