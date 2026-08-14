[comment]: # (title and brief introduction of the sample)
## Qwen-Audio-3.0-TTS Text Normalization (TN) Showcase

[简体中文](./README.md) | English

## Java

[comment]: # (prerequisites)
### :point_right: Prerequisites

1. #### Configure the Alibaba Cloud Model Studio API-KEY

    Before running this sample you need an Alibaba Cloud account, an Alibaba Cloud Model Studio API_KEY and the necessary environment configuration. For the detailed steps see: [PREREQUISITES_EN.md](../../../../PREREQUISITES_EN.md)

[comment]: # (how to run the sample and expected results)
### :point_right: Run the sample

```commandline
mvn clean package
java -jar target/alibabacloud-bailian-speech-demo-java-1.0-SNAPSHOT.jar
```

The sample synthesizes 3 deliberately hard Chinese passages, plays each through the speaker in real time and saves them as `result_tn_1.mp3` ~ `result_tn_3.mp3`, printing checkpoints to the terminal.

Functionally identical to the [Python version](../python). See the [parent README](../README_EN.md) for checkpoint details.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../../docs/image/group.png" width="400"/>
