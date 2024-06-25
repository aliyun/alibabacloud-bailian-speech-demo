[![SVG Banners](https://svg-banners.vercel.app/api?type=luminance&text1=Bailian%20Speech&width=800&height=400)](https://github.com/Akshay090/svg-banners)


# Sample Repository for the AlibabaCloud Bailian Speech SDK

## 关于
---

本仓库提供了阿里云百炼语音大模型服务在一些常用场景的集成示例代码。示例展示了如何通过阿里云百炼的语音大模型服务开发工具包（SDK），实现语音识别（语音转文字）、语音合成（文字转语音）、语音交互等各类AI功能。
您可以将本文档中的这些示例集成进自己的项目中进行二次开发。如有任何疑问还可以通过我们的钉钉 / 微信群进行沟通交流。

### 联系我们

<img src="docs/image/groups.png" width="400"/>


## 最新动态
----
- 2024/06/25：发布初始版本，分别支持从麦克风/文件输入识别，以及语音合成到扬声器和文件的python/java示例。


## 示例获取和准备
----

- 您可以通过 `git clone` 克隆示例工程，或者通过 `Download Zip` 下载完整工程，并在本地解压到文件。

- 在执行示例代码之前，您需要申请阿里云账号并开通**API\_KEY,** 并进行必要的**环境配置**。 请参考文档[PREREQUISITES.md](./PREREQUISITES.md).
- 有些示例的场景还需要导入必要的依赖，如mp3播放的示例需要导入mp3编解码和播放的依赖库。您可以在示例代码所在目录下的README.md文件中查看依赖条件。

## 接入指南
----
### 快速开始

 * 1.语音识别
   * [1.1 语音交互中的识别](#recognition-in-speech-interaction)
   * [1.2 实现语音搜索](#recognition-in-voice-search)
   * [1.3 语音消息转文字](#recognition-in-voice-message)
   * [1.4 会议字幕生成](#meeting-caption-generation)
   * [1.5 电话录音质检](#voice-quality-inspection)
   * [1.6 会议总结和归档](#meeting-recoding-recognition-and-archiving)
 * 2.语音合成
   * [2.1 AI助手中的语音合成](#vocice-synthesis-in-ai-assistant)
   * [2.2 导航中的语音播报](#voice-synthesis-in-navigation)
   * [2.3 合成音频为有声读物等](#vocie-synthesis-for-spoken-books)
   * [2.4 批量合成音频](#batch-vocie-synthesis)
 * 3.融合场景
   * [3.1 LLM输出结果合成语音播放](#llm-output-result-synthesis-voice-play)
   * [3.2 分角色绘本语音合成](#multiple-roles-voice-synthesis)

### 从使用场景出发
#### 1 语音合成
#####  1.1 语音交互<a name="recognition-in-speech-interaction"></a>
我们通常使用一句话识别的模式来实现语音交互中语音识别。一句话识别一般指一次性将长度不超过60s的音频进行识别的调用。
通常这种调用方式会用在交互类的场景，如智能音箱类产品的语音识别、聊天APP中的语音聊天转为文字。当然，您也可以在很多创新场景使用这种方式实现语音转文字，如语音翻译、AI助理等。

- **从麦克风输入**
这种调用示例，旨在模拟实时输入音频流进行语音识别，通常语音交互或者搜索类场景中，我们需要尽快的给用户反馈，包括给用户展示识别中间结果。所以我们需要在识别调用上使用异步回调的模式，以尽快的给用户展示识别结果。

| Demo名称                                                       | 说明                   | 调用API                                                        |
|--------------------------------------------------------------|----------------------|--------------------------------------------------------------|
| [RecognitionFromMicrophone.java](samples/speech-recognition/from-microphone/java/RecognitionFromMicrophone.java) | 从麦克风实时获取音频数据并进行实时识别。 | [实时语音识别](https://help.aliyun.com/document_detail/2712536.html)<br> |
| [recognition_from_microphone.py](samples/speech-recognition/from-microphone/python) | 从麦克风实时获取音频数据并进行实时识别。 | [实时语音识别](https://help.aliyun.com/document_detail/2712536.html) |

##### 1.2 语音搜索<a name="recognition-in-voice-search"></a>
您也可以在搜索业务中使用一句话识别的模式来实现语音识别，将识别文本作为搜索输入。
    - 您可以直接选择从麦克风输入流式音频的方式识别，这样的好处是有中间结果同时能够最快的返回最终结果。
    - 您也可以完成录音，将录音数据一次性发送给识别服务，这样也会尽快的给您返回识别结果。

- **从麦克风输入**
这种调用示例，旨在模拟实时输入音频流进行语音识别，通常语音交互或者搜索类场景中，我们需要尽快的给用户反馈，包括给用户展示识别中间结果。所以我们需要在识别调用上使用异步回调的模式，以尽快的给用户展示识别结果。

| Demo名称                                                       | 说明                   | 调用API                                                        |
|--------------------------------------------------------------|----------------------|--------------------------------------------------------------|
| [RecognitionFromMicrophone.java](samples/speech-recognition/from-microphone/java/RecognitionFromMicrophone.java) | 从麦克风实时获取音频数据并进行实时识别。 | [实时语音识别](https://help.aliyun.com/document_detail/2712536.html)<br> |
| [recognition_from_microphone.py](samples/speech-recognition/from-microphone/python) | 从麦克风实时获取音频数据并进行实时识别。 | [实时语音识别](https://help.aliyun.com/document_detail/2712536.html) |

- **同步获取识别结果**
这种调用方式通过从文件读取音频数据，模拟了您一次性录音的过程，并调用同步的接口获取识别结果。

| Demo名称                                                       | 说明                   | 调用API                                                        |
|--------------------------------------------------------------|----------------------|--------------------------------------------------------------|
| [recognition_from_file_with_realtime_api_by_sync_call.py](samples/speech-recognition/from-file/python/recognition_from_file_with_realtime_api_by_sync_call.py)     | 从文件中读取音频数据，调用实时语音识别API，同步获取识别结果。                  | [实时语音识别](https://help.aliyun.com/document_detail/2712536.html)     |
| [RecognitionFromFileWithRealtimeApiBySyncCall.java](samples%2Fspeech-recognition%2Ffrom-file%2Fjava%2FRecognitionFromFileWithRealtimeApiBySyncCall.java)           | 从文件中读取音频数据，调用实时语音识别API，同步获取识别结果。                  | [实时语音识别](https://help.aliyun.com/document_detail/2712536.html)     |


##### 1.3 聊天软件中的语音消息转文字<a name="recognition-in-voice-message"></a>
这种调用方式，旨在模拟已有一段短音频，需要进行识别的场景。如在一个社交app中，用户对接收到的语音消息转为文字；或者实现一个网页版本的交互或者语音翻译的功能，通过网页录音后，一次性进行识别。

| Demo名称                                                       | 说明                   | 调用API                                                        |
|--------------------------------------------------------------|----------------------|--------------------------------------------------------------|
| [recognition_from_file_with_realtime_api_by_async_start.py](samples/speech-recognition/from-file/python/recognition_from_file_with_realtime_api_by_async_start.py) | 从文件中读取音频数据，调用实时语音识别API，异步获取识别结果。                  | [实时语音识别](https://help.aliyun.com/document_detail/2712536.html)     |
| [recognition_from_file_with_realtime_api_by_sync_call.py](samples/speech-recognition/from-file/python/recognition_from_file_with_realtime_api_by_sync_call.py)     | 从文件中读取音频数据，调用实时语音识别API，同步获取识别结果。                  | [实时语音识别](https://help.aliyun.com/document_detail/2712536.html)     |
| [RecognitionFromFileWithRealtimeApiByAsyncCall.java](samples%2Fspeech-recognition%2Ffrom-file%2Fjava%2FRecognitionFromFileWithRealtimeApiByAsyncCall.java)         | 从文件中读取音频数据，调用实时语音识别API，异步获取识别结果。                  | [实时语音识别](https://help.aliyun.com/document_detail/2712536.html)     |
| [RecognitionFromFileWithRealtimeApiBySyncCall.java](samples%2Fspeech-recognition%2Ffrom-file%2Fjava%2FRecognitionFromFileWithRealtimeApiBySyncCall.java)           | 从文件中读取音频数据，调用实时语音识别API，同步获取识别结果。                  | [实时语音识别](https://help.aliyun.com/document_detail/2712536.html)     |

###### 1.4 在会议中展示实时字幕<a name="meeting-caption-generation"></a>
会议字幕生成是会议类场景一个刚需的功能。我们通常使用实时长语音识别来实现这种功能。实时长语音识别一般指长时间持续的、实时输入音频/实时输出识别结果的调用。通常这种调用方式会用在语音会议、直播之类的场景，需要在一次请求中维护一个持续的识别过程。

- **从麦克风输入**
这种调用示例，旨在模拟实时输入音频流进行长语音识别。这里展示的是建议一个长连接来实现长语音识别的过程，但是在实际的场景中，您可能需要维持多个识别通道，以实现不同角色/会议室的音频输入和识别。

| Demo名称                                                       | 说明                   | 调用API                                                        |
|--------------------------------------------------------------|----------------------|--------------------------------------------------------------|
| [RecognitionFromMicrophone.java](samples/speech-recognition/from-microphone/java/RecognitionFromMicrophone.java) | 从麦克风实时获取音频数据并进行实时识别。 | [实时语音识别](https://help.aliyun.com/document_detail/2712536.html)<br> |
| [recognition_from_microphone.py](samples/speech-recognition/from-microphone/python) | 从麦克风实时获取音频数据并进行实时识别。 | [实时语音识别](https://help.aliyun.com/document_detail/2712536.html) |


##### 1.5 电话录音质检<a name="voice-quality-inspection"></a>
在客服等场景，您可能需要针对采集的电话录音的对话内容做识别，以实现语音质检。通过挖掘已有电话数据来促进客服质量的提升。在这种场景，通常用户会沉淀一定时间的客服电话，批量进行识别，以提取出客服的对话内容。在这个典型场景，使用录音文件识别服务是最好的选择。
另外一个类似的场景是会议总结归档，您可以在会后对会议视频做快速的转写，并调用通义大模型等大模型能力做会议总结。

- **录音文件识别**
录音文件识别需要您先将文件上传到一个可分享下载链接的云存储服务中心，这里推荐阿里云OSS服务，您可以方便的对文件下载时效性做控制。相较于实时转写接口，文件转写会加速识别，并提供更丰富的识别结果信息，如全文级文字、句子级文字、词和时间戳等。您可以提交多通道的音频文件，转写服务会给您返回不同通道的识别结果。

| Demo名称                                                                                                                                                             | 说明                                                | 调用API                                                              |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------|--------------------------------------------------------------------|
| [transcription_from_file_url_with_restful_api.py](samples/speech-recognition/from-file/python//transcription_from_file_url_with_restful_api.py)                    | 批量提交音频文件链接，通过异步回调获取识别结果。                          | [录音文件识别](https://help.aliyun.com/document_detail/2712535.html)     |
| [TranscriptionFromFileLinks.java](samples%2Fspeech-recognition%2Ffrom-file%2Fjava%2FTranscriptionFromFileLinks.java)                                               | 批量提交音频文件链接，通过异步回调获取识别结果。                          | [录音文件识别](https://help.aliyun.com/document_detail/2712535.html)     |


##### 1.6 会议总结和归档<a name="meeting-recoding-recognition-and-archiving"></a>
网络办公、远程办公日益成为主流的场景，对线上会议总结归档，是提升企业生产效率的重要手段。您可以在会后对会议视频做快速的转写，并调用通义大模型等大模型能力做会议总结，快速沉淀会议内容进行归档。

- **录音文件识别**
录音文件识别需要您先将文件上传到一个可分享下载链接的云存储服务中心，这里推荐阿里云OSS服务，您可以方便的对文件下载时效性做控制。相较于实时转写接口，文件转写会加速识别，并提供更丰富的识别结果信息，如全文级文字、句子级文字、词和时间戳等。您可以提交多通道的音频文件，转写服务会给您返回不同通道的识别结果。

| Demo名称                                                                                                                                                             | 说明                                                | 调用API                                                              |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------|--------------------------------------------------------------------|
| [transcription_from_file_url_with_restful_api.py](samples/speech-recognition/from-file/python//transcription_from_file_url_with_restful_api.py)                    | 批量提交音频文件链接，通过异步回调获取识别结果。                          | [录音文件识别](https://help.aliyun.com/document_detail/2712535.html)     |
| [TranscriptionFromFileLinks.java](samples%2Fspeech-recognition%2Ffrom-file%2Fjava%2FTranscriptionFromFileLinks.java)                                               | 批量提交音频文件链接，通过异步回调获取识别结果。                          | [录音文件识别](https://help.aliyun.com/document_detail/2712535.html)     |



#### 2. 语音合成
下面展示的示例基于百炼语音合成大模型服务为基础构建。
##### 2.1 AI助手中的语音合成<a name="vocice-synthesis-in-ai-assistant"></a>
- 合成到扬声器播放

在语音交互，AI助手等场景中，典型的处理流式是 「语音识别」-> 「语义处理」 -> 「语音合成」，在语义处理上，您可以自行实现对话系统或者调用阿里云通义千问大模型生成文本回复，再将回复文本调用语音合成能力生成音频并播放。
本示例展示的是如何调用语音合成服务，将文本合成mp3音频，并通过扬声器播放的过程。示例代码合成设定的文本，您可以结合您的场景进行定制修改。

| Demo名称                                                                                                        | 说明                     | 调用API                                                        | 推荐使用场景   |
|---------------------------------------------------------------------------------------------------------------|------------------------|--------------------------------------------------------------|----------|
| [play_synthesized_audio_to_speaker_by_async_call.py](samples%2Fspeech-synthesizer%2Fplay-by-speaker%2Fpython) | 流式回调合成mp3音频并实时通过扬声器播放。 | [CosyVoice语音合成](https://help.aliyun.com/zh/dashscope/developer-reference/cosyvoice-quick-start) | 实时交互类应用等 |
| [play_synthesized_audio_to_speaker_by_sync_call.py](samples%2Fspeech-synthesizer%2Fplay-by-speaker%2Fpython)  | 一次合成mp3音频，通过扬声器播放。     | [CosyVoice语音合成](https://help.aliyun.com/zh/dashscope/developer-reference/cosyvoice-quick-start) | 非流式的语音对话，如网页版的客服 |
| [PlaySynthesizedMp3ToSpeakerAsyncCall.java](samples%2Fspeech-synthesizer%2Fplay-by-speaker%2Fjava)            | 流式回调合成mp3音频并实时通过扬声器播放。 | [CosyVoice语音合成](https://help.aliyun.com/zh/dashscope/developer-reference/cosyvoice-quick-start) | 实时交互类应用等 |
| [PlaySynthesizedMp3ToSpeakerSyncCall.java](samples%2Fspeech-synthesizer%2Fplay-by-speaker%2Fjava)             | 一次合成mp3音频，通过扬声器播放。     | [CosyVoice语音合成](https://help.aliyun.com/zh/dashscope/developer-reference/cosyvoice-quick-start) | 非流式的语音对话，如网页版的客服 |

##### 2.2 导航中的语音播报<a name="voice-synthesis-in-navigation"></a>
导航是目前很重要的语音合成使用场景。通常您需要在车端不断播放导航文本。本示例展示的是如何调用语音合成服务，将文本合成mp3音频，并通过扬声器播放的过程。在示例的基础上，您需要实现监听异步数据流，并下发到您的客户端进行播放。

| Demo名称                                                                                                        | 说明                     | 调用API                                                        | 推荐使用场景   |
|---------------------------------------------------------------------------------------------------------------|------------------------|--------------------------------------------------------------|----------|
| [play_synthesized_audio_to_speaker_by_async_call.py](samples%2Fspeech-synthesizer%2Fplay-by-speaker%2Fpython) | 流式回调合成mp3音频并实时通过扬声器播放。 | [CosyVoice语音合成](https://help.aliyun.com/zh/dashscope/developer-reference/cosyvoice-quick-start) | 导航应用服务端等 |
| [PlaySynthesizedMp3ToSpeakerAsyncCall.java](samples%2Fspeech-synthesizer%2Fplay-by-speaker%2Fjava)            | 流式回调合成mp3音频并实时通过扬声器播放。 | [CosyVoice语音合成](https://help.aliyun.com/zh/dashscope/developer-reference/cosyvoice-quick-start) | 导航应用服务端等 |


##### 2.3 合成音频为有声读物、新闻、播客等<a name="vocie-synthesis-for-spoken-books"></a>
- 流式输入流式输出

如果是直接使用流式方式实时的去生成合成文本，我们提供了**流式输入，流式输出**的调用方式。这种方式适合大量文本场景下，一次调用过程中，不断次序输入文本，流式输出合成数据，直到合成整篇文档。

| Demo名称                                                                                                                                                                                               | 调用API                                                        |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| [PlaySynthesizedMp3ToSpeakerByStreamingInStreamingOut.java](samples%2Fspeech-synthesizer%2Fplay-by-speaker%2Fjava%2FPlaySynthesizedMp3ToSpeakerByStreamingInStreamingOut.java)                       |[CosyVoice语音合成](https://help.aliyun.com/zh/dashscope/developer-reference/cosyvoice-quick-start) |
| [playe_synthesized_audio_to_speaker_by_streaming_in_streaming_out.py](samples%2Fspeech-synthesizer%2Fplay-by-speaker%2Fpython%2Fplaye_synthesized_audio_to_speaker_by_streaming_in_streaming_out.py) |[CosyVoice语音合成](https://help.aliyun.com/zh/dashscope/developer-reference/cosyvoice-quick-start) |


- 合成到文件

您也可以在这个场景提前合成完整数据。本示例展示将语音合成的mp3数据保存到文件的操作。通过这种方式您可以方便的集成合成音频到您自己的业务。在一些场景，可以将音频合成后进行二次处理再进行播放。您需要使用这种方式来实现音频合成。或者您可以直接在业务代码中使用返回的音频数据流。

| Demo名称                                                                                                                                                  | 说明               | 调用API                                                        |
|---------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|--------------------------------------------------------------|
| [save_synthesized_audio_to_file_by_sync_call.py](samples%2Fspeech-synthesizer%2Fsave-to-file%2Fpython%2Fsave_synthesized_audio_to_file_by_sync_call.py) | 合成语音数据并保存到本地文件。  |[CosyVoice语音合成](https://help.aliyun.com/zh/dashscope/developer-reference/cosyvoice-quick-start) |
| [SaveSynthesizedAudioToFile.java](samples%2Fspeech-synthesizer%2Fsave-to-file%2Fjava%2FSaveSynthesizedAudioToFile.java)                                 |合成语音数据并保存到本地文件。 |[CosyVoice语音合成](https://help.aliyun.com/zh/dashscope/developer-reference/cosyvoice-quick-start) |


##### 2.4 批量合成<a name="batch-vocie-synthesis"></a>
示例展示了通过对象池批量合成文本到音频文件的操作。通常在小说、电子读物等大量文本需要合成的场景使用。

| Demo名称                                                                                                                                                  | 说明             | 调用API                                                        | 推荐使用场景                  |
|---------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|--------------------------------------------------------------|-------------------------|
|[BatchSynthesizedToFiles.java](samples%2Fspeech-synthesizer%2Fsave-to-file%2Fjava%2FBatchSynthesizedToFiles.java) | 批量合成语音合成数据到文件。 |[CosyVoice语音合成](https://help.aliyun.com/zh/dashscope/developer-reference/cosyvoice-quick-start) | 大并发调用场景，小说等文本类app后端服务等。 |

#### 3. 融合场景

##### 3.1 LLM输出结果合成语音播放<a name="llm-output-result-synthesis-voice-play"></a>
示例展示了调用通义千问大模型获取问答结果。并通过语音合成服务合成语音并播放。由于通常大模型服务的文本结果是流式返回的，所以为了用户体验更自然更快捷，我们的示例集成了流式输入、流式输出的语音合成能力。

| Demo名称                                                                                                                                                                           | 说明             | 调用API                                                        | 推荐使用场景               |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|--------------------------------------------------------------|----------------------|
| [PlayLLMTextToSpeakerByStreamingInStreamingOut.java](samples%2Fspeech-synthesizer%2Fplay-by-speaker%2Fjava%2FPlayLLMTextToSpeakerByStreamingInStreamingOut.java)                 | 流式播报大模型返回的流式文本 |[CosyVoice语音合成](https://help.aliyun.com/zh/dashscope/developer-reference/cosyvoice-quick-start) | 集成大模型的APP、智能座舱、智能家居。 |
| [play_llm_text_to_speaker_by_streaming_in_streaming_out.py](samples%2Fspeech-synthesizer%2Fplay-by-speaker%2Fpython%2Fplay_llm_text_to_speaker_by_streaming_in_streaming_out.py) | 流式播报大模型返回的流式文本 |[CosyVoice语音合成](https://help.aliyun.com/zh/dashscope/developer-reference/cosyvoice-quick-start) | 集成大模型的APP、智能座舱、智能家居。 |


##### 3.2 分角色绘本语音合成<a name="multiple-roles-voice-synthesis"></a>
示例展示了在一个多角色的绘本故事中，如何调用语音合成多角色不同音色的对话音频。

| Demo名称                                                                                                                                                                           | 说明      | 调用API                                                        | 推荐使用场景               |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|--------------------------------------------------------------|----------------------|
| [play_synthesized_story.py](samples%2Fspeech-synthesizer%2Fplay-by-speaker%2Fpython%2Fplay_synthesized_story.py)   | 分角色语音合成 |[CosyVoice语音合成](https://help.aliyun.com/zh/dashscope/developer-reference/cosyvoice-quick-start) | 绘本故事等 |




## 许可协议

本项目遵循[The MIT License](./LICENSE)开源协议