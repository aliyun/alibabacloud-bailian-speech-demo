[comment]: # (title and brief introduction of the sample)
## 麦克风实时一句话语音识别和翻译

简体中文 | [English](./README_EN.md)

本示例展示了如何从麦克风录制音频，并将获取的音频流发送至阿里云百炼模型服务进行实时一句话语音翻译。运行示例时，用户对麦克风所说的第一句话会被实时翻译成英文并显示在屏幕上。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景     | 典型用法 | 使用说明 |
|----------| ----- | ----- |
| **入门场景** | 麦克风语音翻译 | *实时从麦克风录音并进行语音翻译* |
| **实时双语字幕** | 自动生成音视频不同语言字幕 | *实时对视频流进行语音识别和翻译，生成双语字幕* |
| **会议语音分析理解场景** | 实时会议语音识别	 | *实时对会议语音进行语音识别并翻译* |

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情

| 推荐模型 | API详情 |
| ----- | ----- |
| **gummy-realtime-v1** | [Paraformer实时语音识别API详情（TODO：更新）](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-real-time-speech-recognition-api) |

### :point_right: 预期结果

运行示例，在控制台会提示您开始说话，服务端会根据VAD（Voice Activity Detection，静音检测）判停，当您停止说话后会自动停止录制。识别结果文本会在控制台打印，录制的音频会被保存到`request_id_record.pcm`文件中。
```text
	[log] Initializing ...
	[log] TranslationRecognizerCallback open.
	[log] Recording...
	[log] Translation started, request_id: a66eac0a04a24dddadeca3acc4a64c01
translation will stop after recording one sentence...
- - - - - - - - - - -
[2024-12-19 14:00:06.757] transcript : 测试一
[2024-12-19 14:00:06.757] translate to en: Test
- - - - - - - - - - -
[2024-12-19 14:00:06.956] transcript : 测试一
[2024-12-19 14:00:06.956] translate to en: Test
- - - - - - - - - - -
[2024-12-19 14:00:07.154] transcript : 测试一
[2024-12-19 14:00:07.154] translate to en: Test
- - - - - - - - - - -
[2024-12-19 14:00:07.353] transcript : 测试一句话识别。
[2024-12-19 14:00:07.353] translate to en: Test sentence recognition.
- - - - - - - - - - -
[2024-12-19 14:00:07.553] transcript : 测试一句话识别。
[2024-12-19 14:00:07.554] <=== [vad pre_end] silence start at 1560 ms, detected at 2000 ms ===>
[2024-12-19 14:00:07.554] translate to en: Test sentence recognition.
- - - - - - - - - - -
[2024-12-19 14:00:07.955] transcript : 测试一句话识别。
[2024-12-19 14:00:07.955] translate to en: Test sentence recognition.
- - - - - - - - - - -
[2024-12-19 14:00:08.157] transcript : 测试一句话识别。
[2024-12-19 14:00:08.157] translate to en: Test sentence recognition.
request id: a66eac0a04a24dddadeca3acc4a64c01 usage: {'duration': 4}
	[log] sentence end, stop sending
	[log] Translation completed.
	[log] TranslationRecognizerCallback close.
    [log] Recorded audio saved to a66eac0a04a24dddadeca3acc4a64c01_record.pcm
```

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
