[comment]: # (title and brief introduction of the sample)
## 语音合成并播放（流式模式）
本示例展示了如何合成指定文本的语音，流式获取返回音频并实时播放。本示例同时展示了如何在流式回调中保存音频到文件。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景 | 典型用法 | 使用说明 |
| ----- | ----- | ----- |
| **电话呼叫中心场景** | 客服回复转语音 | *使用文字转语音对客服机器人回复进行实时语音播报* |
| **数字人场景** | 新闻播报 | *新闻等场景，通过语音合成进行文本信息的播报* |

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情
| 推荐模型 | API详情 |
| --- | --- |
| **cosyvoice-v1** | [CosyVoice大模型语音合成API详情](https://help.aliyun.com/zh/model-studio/developer-reference/api-details-25) <br> [音色列表](https://help.aliyun.com/zh/model-studio/developer-reference/model-list-1)|

### :point_right: 预期结果

示例运行时，将会使用 loongstella 音色合成示例文本 “想不到时间过得这么快！昨天和你视频聊天，看到你那自豪又满意的笑容，我的心里呀，就如同喝了一瓶蜜一样甜呢！真心为你开心呢！” ，合成音频将按照流式方式下发，通过扬声器播放并保存到文件`result.mp3`中。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
