[comment]: # (title and brief introduction of the sample)
## Conversation Context for Qwen-Audio-3.0-ASR Streaming Recognition

English | [简体中文](./README.md)

This example specifically demonstrates the **conversation context (`context`)** capability of **`qwen-audio-3.0-asr-flash-streaming`**. By passing previous dialog turns or domain terms, the model recognizes proper nouns, personal names, and industry jargon much more accurately in a given context.

> For the **vocabulary (hotword)** capability, see the other example: [Precompiled Vocabulary](../recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-vocabulary)

### :point_right: What is the Context

The context is a list of messages, with two roles serving different purposes:

| Role | `content.type` | Carries |
| --- | --- | --- |
| `user` | `input_text` | Recognition results of **previous user utterances**, or a **domain word list** |
| `assistant` | `text` | **Replies of the LLM** in previous turns |

Structure:

```json
{
  "context": [
    {"role": "user",      "content": [{"type": "input_text", "text": "你好啊"}]},
    {"role": "assistant", "content": [{"type": "text",       "text": "你好啊，我是通义千问。"}]}
  ]
}
```

How it is passed differs by language:

| Language | Parameter | Passed to | SDK Requirement |
| --- | --- | --- | --- |
| Python | `raw_input` | `recognition.start()` or `recognition.call()` | **>= 1.25.23** |
| Java | `input` | `RecognitionParam.builder().input(...)` | **>= 2.22.23** |

### :point_right: Two Typical Usages

**1. Dialog history** — for multi-turn voice interaction, carry the previous recognition results and model replies so the model understands the current context:

```python
context = {'context': [
    {'role': 'user',      'content': [{'type': 'input_text', 'text': '帮我看看今天的会议纪要'}]},
    {'role': 'assistant', 'content': [{'type': 'text',       'text': '好的，今天的会议主要讨论了语音识别模型的迭代计划。'}]},
]}
```

**2. Domain word list** — when there is no dialog history, a single `user` message can carry domain terms, acting like a lightweight vocabulary:

```python
context = {'context': [
    {'role': 'user', 'content': [{'type': 'input_text',
     'text': '相关术语：语音实验室、通义千问、百炼平台、声音复刻、热词表、说话人分离'}]},
]}
```

### :point_right: Constraints

The following limits are **enforced by the service**. The `build_context()` / `buildContext()` helpers in the example already implement the corresponding trimming logic:

- At most **5 `input_text` messages and 5 `text` messages**; the latest ones are kept
- The total context text length of one round must **not exceed 400 characters**; the excess is truncated from the tail
- Messages must be **ordered by dialog turn**; within one turn, the `user` (`input_text`) message must come **before** its `assistant` (`text`) message
- Only `qwen-audio-3.0-asr-flash-streaming`, `fun-asr-realtime`, and `fun-asr-realtime-2025-11-07` support `context`
- :warning: **Both the Python and the Java version require the `DASHSCOPE_WORKSPACE_ID` environment variable.** The qwen-audio series models are served under the workspace-specific endpoint `https://{WORKSPACE_ID}.cn-beijing.maas.aliyuncs.com`; without it the example prints a hint and exits.

[comment]: # (supported programming languages of the sample)
### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: Reference

| Model | Mode | API Type | Key Features |
| --- | --- | --- | --- |
| **qwen-audio-3.0-asr-flash-streaming** | Real-time | WebSocket | Dialog context, hotwords, multilingual/dialects, **no duration limit** |

🔗 **API Docs**: [Realtime ASR Python SDK](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk) ｜ [Java SDK](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-java-sdk)

### :point_right: Expected Results

The example runs 4 scenarios in sequence, printing the number of context messages actually sent and the recognition result for each:

| Scenario | Description |
| --- | --- |
| 1. Without context | Baseline for comparison |
| 2. Dialog history | Two complete user / assistant turns |
| 3. Domain word list | A single `user` message carrying 6 domain terms |
| 4. Trimming | 7 user messages and an oversized text on purpose, to show automatic trimming |

```text
=== Example 2: dialog history as context ===
[context] 4 message(s) sent to the service.
RecognitionCallback sentence end, text:  hello world，这里是阿里巴巴语音实验室。
[Metric] requestId: xxx, first package delay ms: 644

=== Example 4: context exceeding the limits is trimmed ===
[context] message truncated to fit the 400-character limit.
[context] 6 message(s) sent to the service.
```

In scenario 4, the 7 user messages are trimmed to the latest 5, plus 1 assistant message makes 6 in total; the oversized text is truncated to the 400-character limit.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../docs/image/group.png" width="400"/>
