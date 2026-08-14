[comment]: # (title and brief introduction of the sample)
## 流式语音识别的对话上下文

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

    > :warning: **上下文（`raw_input`）要求 dashscope >= 1.25.23**。低于该版本时 `raw_input` 会被 SDK 静默忽略，上下文不会发送到服务端，识别仍能正常返回但上下文无效。可用 `pip3 show dashscope` 确认版本。

[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例
您可以使用以下命令运行本示例：

```commandline
python3 run.py
```

示例会依次运行 4 个场景，每个场景先打印实际发送的上下文消息条数，再流式打印识别结果：

| 场景 | 说明 |
| --- | --- |
| 1. 无上下文 | 基线对照 |
| 2. 对话历史 | 传入 2 轮完整的 user / assistant 对话 |
| 3. 领域词表 | 用一条 `user` 消息承载 6 个领域术语 |
| 4. 超限裁剪 | 故意传入 7 条 user 消息与一段超长文本，演示自动裁剪 |

上下文通过 `raw_input` 参数传入：

```python
input_context = {
    'context': [
        {'role': 'user',      'content': [{'type': 'input_text', 'text': '你好啊'}]},
        {'role': 'assistant', 'content': [{'type': 'text',       'text': '你好啊，我是通义千问。'}]},
    ]
}
recognition.start(raw_input=input_context)   # 也可传给 recognition.call()
```

您可以修改 `run.py` 中的 `dialog_history` 与 `domain_terms` 来测试自己的上下文，`build_context()` 会自动按服务端约束裁剪消息条数与文本长度。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../../docs/image/group.png" width="400"/>
