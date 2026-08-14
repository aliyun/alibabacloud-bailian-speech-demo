[comment]: # (title and brief introduction of the sample)
## 使用 Qwen-Audio-3.0-ASR 流式识别的对话上下文（Context）

简体中文 | [English](./README_EN.md)

本示例专门演示 **`qwen-audio-3.0-asr-flash-streaming`** 的**对话上下文（`context`）**能力。通过传入前几轮的对话内容或领域术语，模型能在特定语境下显著提升专有名词、人名、行业术语的识别准确率。

> **热词能力**请参考另一个示例：[预创建热词表](../recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-vocabulary)

### :point_right: 上下文是什么

上下文是一个消息列表，两种角色各有分工：

| 角色 | `content.type` | 承载内容 |
| --- | --- | --- |
| `user` | `input_text` | 前几轮**用户语音的识别结果**，或**领域相关的词表** |
| `assistant` | `text` | 前几轮**大语言模型的回复内容** |

结构如下：

```json
{
  "context": [
    {"role": "user",      "content": [{"type": "input_text", "text": "你好啊"}]},
    {"role": "assistant", "content": [{"type": "text",       "text": "你好啊，我是通义千问。"}]}
  ]
}
```

传参方式因语言而异：

| 语言 | 参数名 | 传入位置 | SDK 版本要求 |
| --- | --- | --- | --- |
| Python | `raw_input` | `recognition.start()` 或 `recognition.call()` | **>= 1.25.23** |
| Java | `input` | `RecognitionParam.builder().input(...)` | **>= 2.22.23** |

### :point_right: 两种典型用法

**1. 对话历史** —— 多轮语音交互场景，把前几轮的识别结果与模型回复带上，让模型理解当前语境：

```python
context = {'context': [
    {'role': 'user',      'content': [{'type': 'input_text', 'text': '帮我看看今天的会议纪要'}]},
    {'role': 'assistant', 'content': [{'type': 'text',       'text': '好的，今天的会议主要讨论了语音识别模型的迭代计划。'}]},
]}
```

**2. 领域词表** —— 没有对话历史时，用一条 `user` 消息承载领域术语，效果类似轻量级热词：

```python
context = {'context': [
    {'role': 'user', 'content': [{'type': 'input_text',
     'text': '相关术语：语音实验室、通义千问、百炼平台、声音复刻、热词表、说话人分离'}]},
]}
```

### :point_right: 约束

以下限制由**服务端强制**，示例代码中的 `build_context()` / `buildContext()` 已实现对应的裁剪逻辑：

- `input_text` 与 `text` 类型消息**各最多 5 条**，超出时保留最近 5 条
- 每轮上下文文本总长度**不超过 400 字符**，超出部分从末尾截断
- 消息必须**按对话轮次排列**，每轮中 `user`（`input_text`）必须在对应的 `assistant`（`text`）**之前**
- 仅 `qwen-audio-3.0-asr-flash-streaming`、`fun-asr-realtime` 及 `fun-asr-realtime-2025-11-07` 支持 `context`
- :warning: **Python 与 Java 版本都需要 `DASHSCOPE_WORKSPACE_ID` 环境变量**：qwen-audio 系列模型使用 workspace 专属接入点 `https://{WORKSPACE_ID}.cn-beijing.maas.aliyuncs.com`，未设置时示例会打印提示并退出。

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情

| 推荐模型 | 模式 | API 类型 | 关键特性 |
| --- | --- | --- | --- |
| **qwen-audio-3.0-asr-flash-streaming** | 实时 (Real-time) | WebSocket | 支持对话上下文、热词、多语种/方言、**无时长限制** |

🔗 **API 文档**：[实时语音识别 Python SDK](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk) ｜ [Java SDK](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-java-sdk)

### :point_right: 预期结果

示例依次运行 4 个场景，控制台会打印每个场景实际发送的上下文消息条数与识别结果：

| 场景 | 说明 |
| --- | --- |
| 1. 无上下文 | 基线对照 |
| 2. 对话历史 | 传入 2 轮完整的 user / assistant 对话 |
| 3. 领域词表 | 用一条 `user` 消息承载 6 个领域术语 |
| 4. 超限裁剪 | 故意传入 7 条 user 消息与一段超长文本，演示自动裁剪 |

```text
=== Example 2: dialog history as context ===
[context] 4 message(s) sent to the service.
RecognitionCallback sentence end, text:  hello world，这里是阿里巴巴语音实验室。
[Metric] requestId: xxx, first package delay ms: 644

=== Example 4: context exceeding the limits is trimmed ===
[context] message truncated to fit the 400-character limit.
[context] 6 message(s) sent to the service.
```

场景 4 中，7 条 user 消息被裁剪为最近 5 条，加上 1 条 assistant 消息共 6 条；超长文本被截断到 400 字符上限。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../docs/image/group.png" width="400"/>
