[comment]: # (title and brief introduction of the sample)
## 复刻你的音色进行语音合成并播放（流式模式）

简体中文 | [English](./README_EN.md)

本示例展示了如何根据指引录制音频，复刻您自己的音色，并合成指定文本的语音。示例将流式获取返回音频并实时播放。本示例同时展示了如何在流式回调中保存音频到文件。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景 | 典型用法 | 使用说明 |
| ----- | ----- | ----- |
| **电话呼叫中心场景** | 客服回复转语音 | *使用自定义音色文字转语音对客服机器人回复进行实时语音播报* |
| **数字人场景** | 新闻播报 | *使用自定义音色新闻等场景，通过语音合成进行文本信息的播报* |

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情
| 推荐模型 | API详情 |
| --- | --- |
| **cosyvoice-v1** | [CosyVoice大模型语音合成API详情](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#95303fd00f0ge) |
| **cosyvoice-v2** | [CosyVoice大模型语音合成API详情](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [音色列表](https://help.aliyun.com/zh/model-studio/cosyvoice-java-sdk#da9ae03e5ek7b) |

### :point_right: 预期结果

本示例分为两部分：录制音频和复刻音色。

#### 录制音频

示例运行时，将会开启录音。请您按照提示录制一段音频用于克隆，并储存在`your_record_file.wav`中。请您使用阿里云oss或其他云存储方法获取可下载http链接。

#### 复刻音色

示例运行时，将会根据您提供的录音创建复刻音色，并使用复刻音色合成示例文本 “你好，现在我在用你自己克隆的语音朗读这一段文本～” ，合成音频将按照流式方式下发，通过扬声器播放并保存到文件`result.mp3`中。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
