[comment]: # (title and brief introduction of the sample)
## 流式语音识别的预创建热词表

简体中文 | [English](./README_EN.md)

## Python

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

1. #### 安装Python依赖

    阿里云百炼SDK运行环境需要Python 3.8及以上版本。您可以使用以下命令来安装本示例的依赖：
    ```commandline
    pip3 install -r requirements.txt
    ```

[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例
您可以使用以下命令运行本示例：

```commandline
python3 run.py
```

示例会完整走一遍热词表的生命周期：**创建词表 → 查询状态 → 用 ID 识别 → 删除词表**。

```python
service = VocabularyService()
vocabulary_id = service.create_vocabulary(
    prefix='demo', target_model=MODEL, vocabulary=my_vocabulary)

# 识别时只传 ID，不必重复传输整个词表
recognition.call(file=audio_path, phrase_id=vocabulary_id)

service.delete_vocabulary(vocabulary_id)   # 务必删除，避免占用配额
```

您可以修改 `run.py` 中的 `my_vocabulary` 来测试自己的热词。`weight` 取值 **[1, 5]**（推荐 4）**或 50**：

> :fire: **超级热词（weight = 50）**：**召回率大幅提升**，适合必须识别准的关键术语。:warning: **数量最多 50 个**，且**仅 Qwen-Audio-3.0-ASR-Flash-Streaming / Filetrans / Flash 系列模型支持**。本示例的词表中 `通义千问` 已设为超级热词作为演示。

权重对照表与热词文本规范参见[本示例说明的“词表格式与权重”章节](../README.md)。

> :warning: 词表配额有限。示例已用 `try / finally` 保证异常时也会删除词表；若您改写代码，请同样确保删除逻辑不被跳过。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../../docs/image/group.png" width="400"/>
