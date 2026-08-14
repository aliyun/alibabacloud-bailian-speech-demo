[comment]: # (title and brief introduction of the sample)
## 使用 Qwen-Audio-3.0-ASR 流式识别的预创建热词表（Vocabulary）

简体中文 | [English](./README_EN.md)

本示例专门演示 **`qwen-audio-3.0-asr-flash-streaming`** 的**预创建热词表（Vocabulary）**能力。热词用于提升专有名词、人名、品牌名、行业术语的识别准确率。

> **对话上下文能力**请参考另一个示例：[对话上下文](../recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-context)

### :point_right: 两种热词用法的区别

| 用法 | 传参方式 | 适用场景 |
| --- | --- | --- |
| **即时热词** | 每次识别时通过 `vocabulary` 参数直接传入词表 | 词表随请求变化、词条较少 |
| **预创建热词表**（本示例） | 先创建词表拿到 `vocabulary_id`，识别时只传 ID | 词表稳定复用、词条较多，避免每次重复传输 |

### :point_right: 完整生命周期

预创建热词表是一个**有状态资源**，需要显式管理：

```
创建词表 → 查询状态(OK) → 用 ID 识别 → 删除词表
```

示例代码用 `try / finally` 保证词表**一定会被删除**，避免长期占用配额：

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
        service.delete_vocabulary(vocabulary_id)   # 务必删除
```

### :point_right: 词表格式与权重

每个词条包含 `text`（热词文本）与 `weight`（权重）：

```python
my_vocabulary = [
    {'text': '语音实验室', 'weight': 4},   # 普通热词
    {'text': '通义千问',   'weight': 50},  # 超级热词
]
```

`weight` 取值范围为 **[1, 5]**（普通热词）**或 50**（超级热词）：

| 权重 | 效果 | 适用场景 |
| --- | --- | --- |
| 1~2 | 轻微偏好 | 热词与常用词发音相似，需避免过度纠偏 |
| **3~4** | **明显偏好（推荐）** | **大多数场景的最佳起始值** |
| 5 | 强制偏好 | 该词在音频中频繁出现且几乎不会与其他词混淆；过高可能导致发音相近的其他词被错误识别为热词 |

建议从 `weight=4` 起测，根据识别效果逐步调整。

> ### :fire: 超级热词（weight = 50）
>
> 将权重直接设为 **50** 即启用**超级热词**，**召回率大幅提升**，适合“无论如何都必须识别准”的关键术语（品牌名、药品名、人名等）。
>
> :warning: **三条约束**：
> 1. **数量最多 50 个**（仅指 weight=50 的超级热词，普通热词不占用此额度）
> 2. **仅 Qwen-Audio-3.0-ASR-Flash-Streaming / Filetrans / Flash 系列模型支持**，其他模型不支持
> 3. 合法取值只有 **[1, 5] 或 50**，不存在 6~49 这段。注意：实测发现服务端对越界值**不报错**（10、51 也能创建成功），但越界后的行为未定义，**请勿依赖**——写 10 并不会比 5 “更强”
>
> 预编译热词与即时热词均支持超级热词。

其他字段与规范：

- `prefix` 是词表名称前缀，便于在控制台区分不同业务的词表
- `lang`（可选）限定热词作用的语种；识别时一旦设置了 `language_hints`，仅匹配该语种的热词生效
- 热词文本需为**实际词语**：含非 ASCII 字符时总字符数 **≤ 15**；纯 ASCII 时按空格切分后的片段数 **≤ 7**

### :point_right: 注意事项

- 词表创建后需**查询状态为 `OK`** 才能用于识别
- 词表与模型绑定：创建时的 `target_model` 必须与识别时使用的模型一致
- 配额有限，**用完及时删除**；示例已用 `finally` 兜底
- :warning: **Python 与 Java 版本都需要 `DASHSCOPE_WORKSPACE_ID` 环境变量**：qwen-audio 系列模型使用 workspace 专属接入点 `https://{WORKSPACE_ID}.cn-beijing.maas.aliyuncs.com`，未设置时示例会打印提示并退出。

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情

| 推荐模型 | 模式 | API 类型 | 关键特性 |
| --- | --- | --- | --- |
| **qwen-audio-3.0-asr-flash-streaming** | 实时 (Real-time) | WebSocket | 支持热词、对话上下文、多语种/方言、**无时长限制** |

🔗 **API 文档**：[实时语音识别 Python SDK](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-python-sdk) ｜ [Java SDK](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-java-sdk)

### :point_right: 预期结果

控制台会依次打印词表创建、状态查询、识别结果与词表删除：

```text
vocabulary created with id: vocab-xxxxxxxx
vocabulary status is OK, starting recognition...
recognition result:  hello world，这里是阿里巴巴语音实验室。
[Metric] requestId: xxx, first package delay ms: 644
vocabulary deleted.
```

其中 `语音实验室` 因命中热词而识别更稳定。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../docs/image/group.png" width="400"/>
