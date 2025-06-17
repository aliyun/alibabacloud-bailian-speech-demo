## Clone Your Voice for Speech Synthesis and Playback (Streaming Mode)

English | [简体中文](./README.md)

## Java

### :point_right: Prerequisites

1. #### Configure Alibaba Cloud API-KEY

    Before running this example, you need to create an Alibaba Cloud account, obtain the API-KEY, and complete environment configuration. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### Java Runtime Environment

   Before running this example, you need to install Java runtime environment and Maven build tool.

### :point_right: How to Run the Example

You can run this example by executing `run.sh` (for Linux/Mac systems) or `run.bat` (for Windows systems).

When running the example, it will use the sample recording to create a cloned voice style and synthesize the sample text "Hello, welcome to use Alibaba Tongyi Voice Lab's voice cloning service~" using the cloned voice style. The synthesized audio will be streamed, played through the speaker, and saved to the file `result.mp3`.

You can replace the sample recording file with your own audio file by modifying `audioUrl`.

You can specify the text to be synthesized by modifying `textArray`.

You can batch delete voice styles with a specific prefix by executing `DeleteVoiceByPrefix`.

### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
