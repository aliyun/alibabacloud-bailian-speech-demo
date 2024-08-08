[comment]: # (title and brief introduction of the sample)
## 单个音视频文件语音识别
本示例展示了如何从一个音视频文件中读取数据，并调用实时语音识别接口实现实时语音识别。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景     | 典型用法      | 使用说明            |
|----------|-----------|-----------------|
| **入门场景** | 音视频文件语音识别 | *对音视频文件进行语音识别*  |

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情

| 推荐模型 | API详情 |
| ----- | ----- |
| paraformer-realtime-v2<br>paraformer-realtime-v1<br>paraformer-realtime-8k-v1 | [Paraformer实时语音识别API详情](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-real-time-speech-recognition-api) |

### :point_right: 预期结果

完整的识别结果会以json的格式保存在 result.json文件中。完整结果包含句级别和字级别的时间戳信息等。

另外识别的完整文本会在控制台打印：
```text
The brief result is:
横看成岭侧成峰，远近高低各不同。不识庐山真面目，只缘身在此山中。
```

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../docs/image/groups.png" width="400"/>
