[comment]: # (title and brief introduction of the sample)
## 使用 Qwen-Audio-3.0-ASR-Flash-Filetrans 进行长音频异步转写与说话人分离

简体中文 | [English](./README_EN.md)

本示例展示了如何使用阿里云百炼平台的 **`qwen-audio-3.0-asr-flash-filetrans`** 模型对**长音频文件**进行**非实时（异步）**语音识别。该模型基于 **HTTP** 协议，支持高达 **12小时** 或 **2GB** 的超大音频文件，具备强大的多语种及方言识别能力，并独有**说话人分离（Speaker Diarization）**功能，同时支持通过 **Prompt 上下文**和**热词**增强识别精度。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景     | 典型用法      | 核心优势            |
|----------|-----------|-----------------|
| **超长音频离线转写** | 全天会议记录/讲座/庭审录音 | *支持12小时/2GB以内超大音频，异步处理不阻塞业务，提供高精度文本*  |
| **多人对话分析** | 访谈/圆桌会议/客服录音质检 | *内置**说话人分离**功能，自动区分不同发言者（如：Speaker A, Speaker B），便于后续整理*  |
| **垂直领域高精度转写** | 医疗/法律/金融档案数字化 | *支持自定义热词（Hotwords）和 Prompt 上下文，显著提升专有词汇准确率*  |

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情

| 推荐模型 | 模式 | API 类型 | 关键特性 |
| ----- | ----- | ----- | ----- |
| **qwen-audio-3.0-asr-flash-filetrans** | 非实时 (Asynchronous) | HTTP | 支持热词、Prompt上下文、**说话人分离**、多语种/方言、最大12小时/2GB |

🔗 **API 文档**: [Qwen-Audio 文件转写 API 参考](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)

### :point_right: 模型能力概览

*   **支持语言**: 
    *   **中文及方言**: 普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；覆盖中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等口音及地区官话。
    *   **外语**: 英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语。
*   **精度增强**: 支持传入 `hotwords` (热词) 和 `prompt` (上下文提示) 以优化特定场景识别效果。
*   **说话人分离**: 自动识别并标记不同说话人的片段（例如：`Speaker 1: ...`, `Speaker 2: ...`）。
*   **限制**: 单个音频文件最大时长 **12小时** 或最大大小 **2GB**。

### :point_right: 预期结果

#### 1. 基础识别结果（含说话人分离）
任务完成后，控制台将打印带有说话人标签的识别文本：

```text
✅ 异步任务完成!
📝 识别文本 (带说话人分离): 

[Speaker 1] 大家好，欢迎参加今天的季度总结会议。
[Speaker 2] 谢谢主持人，我先汇报一下销售部门的数据。
[Speaker 1] 好的，请继续。
[Speaker 2] 本季度我们的营收增长了...

[Metric] Task ID: xxx-xxx, Duration: 45m, Status: SUCCEEDED
```

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../docs/image/group.png" width="400"/>