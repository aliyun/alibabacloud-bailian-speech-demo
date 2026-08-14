[comment]: # (title and brief introduction of the sample)
## 使用 Qwen-Audio-3.0-ASR-Flash 进行高精度非流式语音识别

简体中文 | [English](./README_EN.md)

本示例展示了如何使用阿里云百炼平台的 **`qwen-audio-3.0-asr-flash`** 模型进行**非流式语音识别**。该模型支持高达 **2GB** 或 **5分钟** 的音频文件，具备强大的多语种及方言识别能力，并支持通过 **Prompt 上下文**和**热词**增强识别精度。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景     | 典型用法      | 核心优势            |
|----------|-----------|-----------------|
| **高精度短音频转写** | 会议录音/访谈/播客片段 | *支持5分钟/2GB以内音频，提供句级时间戳和高精度文本*  |
| **垂直领域识别优化** | 医疗/法律/金融专有名词识别 | *支持自定义热词（Hotwords）和 Prompt 上下文，显著提升专有词汇准确率*  |
| **多语种/方言处理** | 跨国会议/地方方言录音 | *支持中、英、日、韩等30+语言及中国各地方言（粤语、吴语、川渝话等）*  |

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情

| 推荐模型 | 模式 | API 类型 | 关键特性 |
| ----- | ----- | ----- | ----- |
| **qwen-audio-3.0-asr-flash** | 非流式 | HTTP | 支持热词、Prompt上下文、多语种/方言、最大5分钟/2GB |

🔗 **API 文档**: [Qwen-Audio-3.0 语音识别 API 参考](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#nrt02-funasr-flash-h2)

### :point_right: 模型能力概览

*   **支持语言**: 
    *   **中文及方言**: 普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；覆盖中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等口音及地区官话。
    *   **外语**: 英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语。
*   **精度增强**: 支持传入 `hotwords` (热词) 和 `prompt` (上下文提示) 以优化特定场景识别效果。
*   **限制**: 单个音频文件最大时长 **5分钟** 或最大大小 **2GB**。

### :point_right: 预期结果

#### 1. 基础识别结果
控制台将打印识别出的纯文本及请求耗时：

```text
✅ 识别成功!
📝 识别文本: 
你好，欢迎使用阿里云通义千问音频大模型。这是一个测试高精度同步识别的示例。

[Metric] RequestId: xxx-xxx, Latency: 1200ms
```


[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../docs/image/group.png" width="400"/>

