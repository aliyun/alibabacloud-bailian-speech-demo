[comment]: # (title and brief introduction of the sample)
## Precompiled Vocabulary for Streaming Speech Recognition

English | [简体中文](./README.md)

## Java

[comment]: # (prerequisites)
### :point_right: Prerequisites

1. #### Configure the Alibaba Cloud Model Studio API-KEY

    Before running this example, you need to activate an Alibaba Cloud account, obtain the Model Studio API_KEY, and complete the required environment configuration. For detailed steps, see: [PREREQUISITES_EN.md](../../../../PREREQUISITES_EN.md)

1. #### Configure the Workspace ID

    :warning: The qwen-audio series models are served under the workspace-specific endpoint `https://{WORKSPACE_ID}.cn-beijing.maas.aliyuncs.com`, so you **must** set:

    ```commandline
    export DASHSCOPE_WORKSPACE_ID=llm-xxxxxx
    ```

    The workspace id can be found on the Alibaba Cloud Model Studio console. Without it the example prints a hint and exits. The Python version requires this variable as well.

1. #### Java environment and dependencies

    This example requires JDK 1.8 or later and the Maven build tool.

[comment]: # (how to run the sample and expected results)
### :point_right: Run the Example

You can run this example by executing run.sh (Linux/Mac systems) or run.bat (Windows systems).

The example walks through the whole vocabulary lifecycle: **create → query status → recognize by id → delete**.

```java
VocabularyService service = new VocabularyService(apiKey);
Vocabulary vocabulary = service.createVocabulary(MODEL, "testpfx", vocabularyJson);

RecognitionParam param = RecognitionParam.builder()
    .model(MODEL)
    .format("wav")
    .sampleRate(16000)
    .vocabularyId(vocabulary.getVocabularyId())   // only the id
    .build();

service.deleteVocabulary(vocabulary.getVocabularyId());   // always delete
```

You can edit `vocabularyJson` in `RecognizeSpeechVocabulary.java` to test your own hotwords. `weight` accepts **[1, 5]** (4 recommended) **or 50**:

> :fire: **Super hotword (weight = 50)**: **boosts recall dramatically**, for terms that must be transcribed correctly. :warning: **At most 50 of them**, and **only the Qwen-Audio-3.0-ASR-Flash-Streaming / Filetrans / Flash series support it**. In this example `通义千问` is configured as a super hotword for demonstration.

See the "Format and Weight" section of [the example overview](../README_EN.md) for the full weight table and hotword text limits.

> :warning: The vocabulary quota is limited. The example uses `try / finally` so the list is deleted even on failure, and closes the WebSocket connection (`getDuplexApi().close()`) in `finally` to avoid connection leaks.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../../docs/image/group.png" width="400"/>
