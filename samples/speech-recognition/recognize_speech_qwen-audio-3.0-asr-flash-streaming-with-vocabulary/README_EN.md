[comment]: # (title and brief introduction of the sample)
## Precompiled Vocabulary for Qwen-Audio-3.0-ASR Streaming Recognition

English | [简体中文](./README.md)

This example specifically demonstrates the **precompiled vocabulary** capability of **`qwen-audio-3.0-asr-flash-streaming`**. Hotwords improve the recognition accuracy of proper nouns, personal names, brand names, and industry jargon.

> For the **conversation context** capability, see the other example: [Conversation Context](../recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-context)

### :point_right: Instant vs. Precompiled Vocabulary

| Approach | How it is passed | Best for |
| --- | --- | --- |
| **Instant vocabulary** | Pass the word list directly via the `vocabulary` parameter on every request | Word list changes per request, few entries |
| **Precompiled vocabulary** (this example) | Create the list once to get a `vocabulary_id`, then pass only the ID | Stable, reusable list with many entries; avoids re-transmitting it every time |

### :point_right: Full Lifecycle

A precompiled vocabulary is a **stateful resource** that must be managed explicitly:

```
create → query status (OK) → recognize by id → delete
```

The example uses `try / finally` to guarantee the vocabulary **is always deleted**, so it never keeps consuming your quota:

```python
service = VocabularyService()
vocabulary_id = None
try:
    vocabulary_id = service.create_vocabulary(
        prefix='demo', target_model=MODEL, vocabulary=my_vocabulary)
    if service.query_vocabulary(vocabulary_id).get('status') != 'OK':
        return
    recognition.call(file=audio_path, phrase_id=vocabulary_id)
finally:
    if vocabulary_id:
        service.delete_vocabulary(vocabulary_id)   # always delete
```

### :point_right: Format and Weight

Each entry has a `text` (the hotword) and a `weight`:

```python
my_vocabulary = [
    {'text': '语音实验室', 'weight': 4},   # regular hotword
    {'text': '通义千问',   'weight': 50},  # super hotword
]
```

`weight` accepts **[1, 5]** (regular hotword) **or 50** (super hotword):

| Weight | Effect | When to use |
| --- | --- | --- |
| 1~2 | Slight preference | The hotword sounds similar to common words and over-correction must be avoided |
| **3~4** | **Clear preference (recommended)** | **Best starting value for most scenarios** |
| 5 | Forced preference | The word appears frequently and is unlikely to be confused; too high a weight may force similar-sounding words into the hotword |

Start from `weight=4` and tune step by step based on the results.

> ### :fire: Super Hotword (weight = 50)
>
> Setting the weight to **50** turns the entry into a **super hotword**, which **boosts recall dramatically**. Use it for must-get-right terms such as brand names, drug names and person names.
>
> :warning: **Three constraints:**
> 1. **At most 50 super hotwords** (only weight=50 entries count; regular hotwords do not consume this quota)
> 2. **Only the Qwen-Audio-3.0-ASR-Flash-Streaming / Filetrans / Flash series support it** — other models do not
> 3. The only valid values are **[1, 5] or 50**; there is no 6~49 range. Note: in our tests the service **does not report an error** for out-of-range values (10 and 51 were accepted), but the resulting behaviour is undefined — **do not rely on it**; 10 is not "stronger" than 5
>
> Both precompiled and instant hotwords support super hotwords.

Other fields and limits:

- `prefix` is the vocabulary name prefix, useful for distinguishing lists across business lines in the console
- `lang` (optional) restricts the language a hotword applies to; once `language_hints` is set at recognition time, only hotwords of that language take effect
- A hotword must be a **real word**: with non-ASCII characters the total character count must be **≤ 15**; for pure ASCII the number of space-separated segments must be **≤ 7**

### :point_right: Notes

- After creation, the vocabulary status must be **`OK`** before it can be used for recognition
- The vocabulary is bound to a model: the `target_model` at creation must match the model used for recognition
- Quota is limited — **delete when done**; the example already guards this with `finally`
- :warning: **Both the Python and the Java version require the `DASHSCOPE_WORKSPACE_ID` environment variable.** The qwen-audio series models are served under the workspace-specific endpoint `https://{WORKSPACE_ID}.cn-beijing.maas.aliyuncs.com`; without it the example prints a hint and exits.

[comment]: # (supported programming languages of the sample)
### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: Reference

| Model | Mode | API Type | Key Features |
| --- | --- | --- | --- |
| **qwen-audio-3.0-asr-flash-streaming** | Real-time | WebSocket | Hotwords, dialog context, multilingual/dialects, **no duration limit** |

🔗 **API Docs**: [Realtime ASR Python SDK](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk) ｜ [Java SDK](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-java-sdk)

### :point_right: Expected Results

The console prints the vocabulary creation, status query, recognition result, and deletion in sequence:

```text
vocabulary created with id: vocab-xxxxxxxx
vocabulary status is OK, starting recognition...
recognition result:  hello world，这里是阿里巴巴语音实验室。
[Metric] requestId: xxx, first package delay ms: 644
vocabulary deleted.
```

`语音实验室` is recognized more reliably because it matches a hotword.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../docs/image/group.png" width="400"/>
