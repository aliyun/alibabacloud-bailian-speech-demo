[comment]: # (title and brief introduction of the sample)
## 流式语音识别的对话上下文

简体中文 | [English](./README_EN.md)

## Java

[comment]: # (prerequisites)
### :point_right: 前提条件

1. #### 配置阿里云百炼API-KEY

    在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

1. #### 配置 Workspace ID

    qwen-audio 系列模型使用 workspace 专属接入点 `https://{WORKSPACE_ID}.cn-beijing.maas.aliyuncs.com`，因此**必须**设置环境变量：

    ```commandline
    export DASHSCOPE_WORKSPACE_ID=llm-xxxxxx
    ```

    workspace id 可在阿里云百炼控制台获取。未设置时示例会打印提示并退出。

1. #### Java环境与依赖

    示例需要 JDK 1.8 及以上版本，以及 Maven 构建工具。

    > :warning: **上下文（`input`）要求 dashscope-sdk-java >= 2.22.23**，本示例的 `pom.xml` 已声明满足要求的版本。

[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例

您可以通过运行run.sh (Linux, Mac系统)或run.bat (Windows系统)来运行本示例。

示例会依次运行 4 个场景，每个场景先打印实际发送的上下文消息条数，再打印识别结果：

| 场景 | 说明 |
| --- | --- |
| 1. 无上下文 | 基线对照 |
| 2. 对话历史 | 传入 2 轮完整的 user / assistant 对话 |
| 3. 领域词表 | 用一条 `user` 消息承载 6 个领域术语 |
| 4. 超限裁剪 | 故意传入 7 条 user 消息与一段超长文本，演示自动裁剪 |

上下文通过 `RecognitionParam` 的 `input` 参数传入：

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

您可以修改 `RecognizeSpeechContext.java` 中的 `dialogHistory` 与 `domainTerms` 来测试自己的上下文，`buildContext()` 会自动按服务端约束裁剪消息条数与文本长度。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../../docs/image/group.png" width="400"/>
