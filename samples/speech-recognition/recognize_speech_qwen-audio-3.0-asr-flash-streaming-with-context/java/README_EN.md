[comment]: # (title and brief introduction of the sample)
## Conversation Context for Streaming Speech Recognition

English | [简体中文](./README.md)

## Java

[comment]: # (prerequisites)
### :point_right: Prerequisites

1. #### Configure the Alibaba Cloud Model Studio API-KEY

    Before running this example, you need to activate an Alibaba Cloud account, obtain the Model Studio API_KEY, and complete the required environment configuration. For detailed steps, see: [PREREQUISITES_EN.md](../../../../PREREQUISITES_EN.md)

1. #### Configure the Workspace ID

    The qwen-audio series models are served under the workspace-specific endpoint `https://{WORKSPACE_ID}.cn-beijing.maas.aliyuncs.com`, so you **must** set:

    ```commandline
    export DASHSCOPE_WORKSPACE_ID=llm-xxxxxx
    ```

    The workspace id can be found on the Alibaba Cloud Model Studio console. Without it the example prints a hint and exits.

1. #### Java environment and dependencies

    This example requires JDK 1.8 or later and the Maven build tool.

    > :warning: **The context (`input`) requires dashscope-sdk-java >= 2.22.23.** The `pom.xml` of this example already declares a satisfying version.

[comment]: # (how to run the sample and expected results)
### :point_right: Run the Example

You can run this example by executing run.sh (Linux/Mac systems) or run.bat (Windows systems).

The example runs 4 scenarios in sequence. Each one first prints the number of context messages actually sent, then prints the recognition result:

| Scenario | Description |
| --- | --- |
| 1. Without context | Baseline for comparison |
| 2. Dialog history | Two complete user / assistant turns |
| 3. Domain word list | A single `user` message carrying 6 domain terms |
| 4. Trimming | 7 user messages and an oversized text on purpose, to show automatic trimming |

The context is passed through the `input` parameter of `RecognitionParam`:

```java
Map<String, Object> userContent = new HashMap<>();
userContent.put("type", "input_text");
userContent.put("text", "你好啊");

Map<String, Object> userMessage = new HashMap<>();
userMessage.put("role", "user");
userMessage.put("content", Arrays.asList(userContent));

Map<String, Object> input = new HashMap<>();
input.put("context", Arrays.asList(userMessage));

RecognitionParam param = RecognitionParam.builder()
    .model("qwen-audio-3.0-asr-flash-streaming")
    .format("wav")
    .sampleRate(16000)
    .input(input)
    .build();
```

You can edit `dialogHistory` and `domainTerms` in `RecognizeSpeechContext.java` to test your own context. `buildContext()` automatically trims the message count and text length according to the service constraints.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../../docs/image/group.png" width="400"/>
