[comment]: # (title and brief introduction of the sample)
## 流式语音识别的预创建热词表

简体中文 | [English](./README_EN.md)

## Java

[comment]: # (prerequisites)
### :point_right: 前提条件

1. #### 配置阿里云百炼API-KEY

    在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

1. #### 配置 Workspace ID

    :warning: qwen-audio 系列模型使用 workspace 专属接入点 `https://{WORKSPACE_ID}.cn-beijing.maas.aliyuncs.com`，因此**必须**设置环境变量：

    ```commandline
    export DASHSCOPE_WORKSPACE_ID=llm-xxxxxx
    ```

    workspace id 可在阿里云百炼控制台获取。未设置时示例会打印提示并退出。Python 版本同样需要此变量。

1. #### Java环境与依赖

    示例需要 JDK 1.8 及以上版本，以及 Maven 构建工具。

[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例

您可以通过运行run.sh (Linux, Mac系统)或run.bat (Windows系统)来运行本示例。

示例会完整走一遍热词表的生命周期：**创建词表 → 查询状态 → 用 ID 识别 → 删除词表**。

```java
VocabularyService service = new VocabularyService(apiKey);
Vocabulary vocabulary = service.createVocabulary(MODEL, "testpfx", vocabularyJson);

RecognitionParam param = RecognitionParam.builder()
    .model(MODEL)
    .format("wav")
    .sampleRate(16000)
    .vocabularyId(vocabulary.getVocabularyId())   // 只传 ID
    .build();

service.deleteVocabulary(vocabulary.getVocabularyId());   // 务必删除
```

您可以修改 `RecognizeSpeechVocabulary.java` 中的 `vocabularyJson` 来测试自己的热词。`weight` 取值 **[1, 5]**（推荐 4）**或 50**：

> :fire: **超级热词（weight = 50）**：**召回率大幅提升**，适合必须识别准的关键术语。:warning: **数量最多 50 个**，且**仅 Qwen-Audio-3.0-ASR-Flash-Streaming / Filetrans / Flash 系列模型支持**。本示例中 `通义千问` 已设为超级热词作为演示。

权重对照表与热词文本规范参见[本示例说明的“词表格式与权重”章节](../README.md)。

> :warning: 词表配额有限。示例已用 `try / finally` 保证异常时也会删除词表，并在 `finally` 中关闭 WebSocket 连接（`getDuplexApi().close()`）避免连接泄漏。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../../docs/image/group.png" width="400"/>
