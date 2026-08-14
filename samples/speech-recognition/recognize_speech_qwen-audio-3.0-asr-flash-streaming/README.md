[comment]: # (title and brief introduction of the sample)
## 使用 Qwen-Audio-3.0-ASR-Flash-Streaming 进行实时流式语音识别

简体中文 | [English](./README_EN.md)

本示例展示了如何使用阿里云百炼平台的 **`qwen-audio-3.0-asr-flash-streaming`** 模型进行**实时（Real-time）**流式语音识别。该模型基于 **WebSocket** 协议，支持**无限制时长**的音频流输入，具备强大的多语种及方言识别能力，并支持通过 **Prompt 上下文**和**热词**增强识别精度，适用于直播字幕、实时会议转录等低延迟场景。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景     | 典型用法      | 核心优势            |
|----------|-----------|-----------------|
| **实时直播/会议字幕** | 在线直播/远程会议/课堂实录 | *基于 WebSocket 长连接，毫秒级延迟返回识别结果，支持无限时长音频流*  |
| **垂直领域实时交互** | 智能客服/语音助手 | *支持自定义热词（Hotwords）和 Prompt 上下文，显著提升专有词汇实时识别准确率*  |
| **多语种/方言实时转写** | 跨国直播/方言交流 | *支持中、英、日、韩等30+语言及中国各地方言（粤语、吴语、川渝话等）的实时混合识别*  |

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

### :point_right: 相关示例

本示例仅展示**最基础的流式识别**：读取本地音频文件、逐帧发送、实时打印识别结果。两项进阶能力已拆分为独立示例：

| 能力 | 示例 |
| --- | --- |
| **对话上下文（Context）** | [传入对话历史或领域词表提升识别准确率，含条数与长度限制的裁剪处理](../recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-context) |
| **预创建热词表（Vocabulary）** | [创建词表拿到 ID 后复用，管理完整生命周期](../recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-vocabulary) |

> :warning: **运行本示例需要 `DASHSCOPE_WORKSPACE_ID` 环境变量**：qwen-audio 系列模型使用 workspace 专属接入点 `https://{WORKSPACE_ID}.cn-beijing.maas.aliyuncs.com`，未设置时示例会打印提示并退出。

[comment]: # (model and interface of the sample)
### :point_right: 参考详情

| 推荐模型 | 模式 | API 类型 | 关键特性 |
| ----- | ----- | ----- | ----- |
| **qwen-audio-3.0-asr-flash-streaming** | 实时 (Real-time) | WebSocket | 支持热词、Prompt上下文、多语种/方言、**无时长限制** |

🔗 **API 文档**: [Qwen-Audio 实时语音识别 API 参考](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)

### :point_right: 模型能力概览

*   **支持语言**: 
    *   **中文及方言**: 普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；覆盖中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等口音及地区官话。
    *   **外语**: 英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语。
*   **精度增强**: 支持传入 `hotwords` (热词) 和 `prompt` (上下文提示) 以优化特定场景识别效果。
*   **时长限制**: **无限制**（受限于网络稳定性及会话保持策略，建议合理管理长连接）。

### :point_right: 预期结果

#### 1. 实时流式识别结果
控制台将实时打印增量识别文本，最终合并为完整句子：

```text
🌊 开始实时流式识别...
[Stream] 你好
[Stream] ，欢迎
[Stream] 使用阿里云
[Stream] 通义千问
[Stream] ...
✅ 识别结束!
📝 最终完整文本: 
你好，欢迎使用阿里云通义千问音频大模型。这是一个测试实时流式识别的示例。

[Metric] RequestId: xxx-xxx, First Token Latency: 150ms
```


[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../docs/image/group.png" width="400"/>

