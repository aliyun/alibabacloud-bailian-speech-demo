[comment]: # (title and brief introduction of the sample)
## Qwen-Audio-3.0-TTS All-in-One Multilingual Speech Synthesis

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

The sample uses **one single voice** `longanhuan_mtlv7` to synthesize the same greeting in 16 languages, playing each back in real time and saving them as `result_<language-code>.mp3`.

Functionally identical to the [Python version](../python). For the full 16-language table, `languageHints` + `instruction` usage and round-trip verification results, see the [parent README](../README_EN.md).

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../../docs/image/group.png" width="400"/>
