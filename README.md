# 阿里云百炼 - 通义语音大模型 - 开发示例代码

简体中文| [English](./README_EN.md) 

本仓库以示例代码的形式向开发者展示如何通过<strong>阿里云百炼</strong>调用<strong>语音大模型</strong>（包括[Qwen-Audio-3.0-TTS](https://help.aliyun.com/zh/model-studio/cosyvoice-websocket-api/)、[Qwen-Audio-3.0-ASR](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-websocket-api)、[CosyVoice](https://fun-audio-llm.github.io/)、[Fun-ASR](https://github.com/modelscope/FunASR)等），从而实现<strong>语音识别</strong>（语音转文字）、<strong>语音生成</strong>（文字转语音）等基础功能。以及如何结合阿里云百炼支持的大语言模型（包括千问OMNI、Qwen、百川、月之暗面、零一万物、MiniMax等），从而实现<strong>视频聊天对话</strong>、<strong>语音聊天对话</strong>、<strong>语音分析理解</strong>、<strong>语音翻译</strong>等高阶AI功能。


开发者可以通过阿里云百炼提供的模型调用 :moneybag: **免费额度** :moneybag: 试用本仓库中的各个示例，还可以直接将这些示例集成进自己的项目中进一步开发。在开发过程中如有任何疑问，都可以通过我们的钉钉群进行沟通交流。

<img src="./docs/image/group.png" height="200"/>

## ⭐最新动态⭐

### 2026/08/14
- 增加 Qwen-Audio-3.0-TTS 语音合成与声音复刻示例，支持通过指令控制音色风格、方言与情感。
- 增加 Qwen-Audio-3.0-ASR 系列语音识别示例，覆盖非流式识别、流式识别（支持热词与对话上下文）与录音文件转写。

### 2026/07/14
- 增加 Qwen-Audio-3.0-Realtime 端到端实时语音对话模型示例（含陪伴对话、函数调用、推理路由三种场景）。


更多历史发布信息请见[变更记录](#point_right-变更记录)。

## :point_right: 示例获取和准备工作
- 您可以通过`git clone`克隆示例工程，或者通过[`Download Zip`](https://github.com/aliyun/alibabacloud-bailian-speech-demo/archive/refs/heads/master.zip)下载完整工程，并在本地解压到文件。

- 在执行示例代码之前，您需要开通**阿里云账号**及**阿里云百炼模型服务**、创建阿里云百炼**API\_KEY**并进行必要的**环境配置**，以及安装阿里云百炼**DashScope SDK**，有关步骤的向导请参见[运行示例代码的前提条件](./PREREQUISITES.md)。某些示例还需要导入必要的依赖，您可以在示例代码所在目录下的README.md文件中查看具体的依赖条件。

## :point_right: 应用场景与开发示例

* ### :rocket: 推荐场景

| 典型用法 | 使用说明 | 开发示例 |
| --- | --- | --- |
| Qwen-Audio-3.0-ASR 流式语音识别 | *无时长限制的实时流式识别，支持热词与对话上下文* | [流式语音识别](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-streaming) |
| Qwen-Audio-3.0-ASR 非流式语音识别 | *对音频 URL 一次性识别，支持对话上下文，最大 5 分钟/2GB* | [非流式语音识别](./samples/speech-recognition/recognize_speech_qwen-audio_3.0_asr_flash) |
| Qwen-Audio-3.0-ASR 录音文件转写 | *异步转写最长 12 小时录音，支持说话人分离* | [录音文件转写](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-filetrans) |
| Qwen-Audio-3.0-TTS 语音合成 | *指令控制音色风格、方言和情感，实时流式播放* | [指令控制语音合成](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_model) |
| Qwen-Audio-3.0-TTS 声音复刻 | *一段音频复刻音色，用复刻音色合成任意文本* | [声音复刻并合成](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_by_cloned_voice) |
| Qwen-Audio-3.0-Realtime 实时语音对话 | *基于 WebSocket 的端到端实时语音对话，含陪伴对话、函数调用、推理路由* | [qwen-audio-3.0-realtime](./samples/conversation/fun-audiochat-realtime) |

> **更多智能体场景**：[qwen-audio-agent](https://github.com/QwenAudio/qwen-audio-agent) 提供了基于 Qwen-Audio-3.0-Realtime 构建的多种 Agent 示例，包括多轮记忆、工具编排和多模态输入，可作为生产级参考。

* ### :sparkles: 进阶用法

| 典型用法 | 使用说明 | 开发示例 |
| --- | --- | --- |
| 流式识别 + 对话上下文 | *传入对话历史或领域词表提升识别准确率，含条数与长度限制的裁剪* | [对话上下文](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-context) |
| 流式识别 + 预创建热词表 | *创建热词表拿到 ID 后复用，覆盖创建、查询、识别、删除完整生命周期* | [预创建热词表](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-vocabulary) |
| TTS 指令控制详解 | *风格指令、方言指令、情感标签、组合用法的完整示例与标签对照表* | [指令控制详解](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_by_instruction) |
| TTS 文本正则化（TN） | *数量词、单位、百分号、范围符、热线号码、多音字等难读文本的合成效果与检查点* | [文本正则化演示](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_text_normalization) |
| TTS All-in-One 多语言 | *单一音色 longanhuan_mtlv7 支持 16 种语言，切换语种时音色保持一致* | [多语言语音合成](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_multilingual) |


* ### :musical_note: 音乐生成场景
| 典型用法 | 使用说明 | 开发示例 |
| --- | --- | --- |
| 根据提示词生成音乐 | *输入音乐风格描述，自动生成歌词并演唱* | [根据提示词生成音乐](./samples/music-generation/generate_music_from_prompt) |
| 根据歌词生成音乐 | *提供自定义歌词，AI谱曲并演唱* | [根据歌词生成音乐](./samples/music-generation/generate_music_from_lyrics) |


* ### :telephone: 电话客服中心机器人及对话分析理解场景
| 典型用法 | 使用说明 | 开发示例                                                                                        |
| --- | --- |---------------------------------------------------------------------------------------------|
| 实时通话语音识别 | *实时对电话系统通话进行语音识别* | [麦克风实时语音识别](./samples/speech-recognition/recognize_speech_from_microphone)                    |
| 实时回复语音合成 | *对客服机器人回复进行语音合成* | [语音合成并播放（流式模式）](./samples/speech-synthesizer/synthesize_speech_from_text_by_streaming_mode)
| 定制音色语音合成 | *使用定制音色进行语音合成* | [复刻你的音色进行语音合成并播放（流式模式）](./samples/speech-synthesizer/synthesize_speech_from_text_with_cloned_voice)                       |
| Qwen-Audio-3.0-TTS 定制音色语音合成 | *使用 Qwen-Audio-3.0-TTS 模型复刻音色并进行语音合成* | [复刻你的音色进行语音合成并播放（流式模式）](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_by_cloned_voice)                       |
| 通话录音批量语音识别 | *对客服中心通话录音文件进行批量语音识别* | [批量音视频文件语音识别（批量模式）](./samples/speech-recognition/recognize_speech_from_files_by_batch_mode) |
| Qwen-Audio-3.0-ASR 实时通话语音识别 | *使用热词和对话上下文提升产品名、业务术语的实时识别准确率* | [Qwen-Audio-3.0-ASR 流式语音识别](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-streaming) |
| Qwen-Audio-3.0-ASR 通话录音质检 | *对通话录音异步转写，并通过说话人分离区分坐席与客户* | [Qwen-Audio-3.0-ASR 录音文件转写](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-filetrans) |


* ### :loudspeaker: 语音播报及配音场景
| 典型用法 | 使用说明 | 开发示例                                                                                |
| --- | --- |-------------------------------------------------------------------------------------|
| 信息播报 | *对各类文字进行语音合成* | [语音合成并播放（流式模式）](./samples/speech-synthesizer/synthesize_speech_from_text_by_streaming_mode)                |
| 大语言模型实时输出播报 <img src="./docs/image/logo.svg" height="15"/> | *对大语言模型产生的实时输出进行语音合成并播报* | [语音合成实时LLM输出并播放（流式模式）](./samples/speech-synthesizer/synthesize_speech_from_llm_by_streaming_mode)      |
| 方言与情感配音 | *通过指令指定方言与说话风格，或用行内标签控制情感* | [指令控制语音合成并播放（流式模式）](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_model)      |
| 专属音色播报 | *复刻主播或品牌音色，用于持续稳定的内容播报* | [声音复刻并合成语音（流式模式）](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_by_cloned_voice)      |
| 多语言内容播报 | *使用 All-in-One 音色一键切换 16 种语言，适合国际化内容* | [多语言语音合成](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_multilingual)      |
| 数字与专业文本播报 | *文本正则化自动处理数量词、单位、符号，让专业内容读得自然* | [文本正则化演示](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_text_normalization)      |

* ### :raising_hand: 会议语音分析理解场景
| 典型用法 | 使用说明 | 开发示例                                                                                        |
| --- | --- |---------------------------------------------------------------------------------------------|
| 实时会议语音识别 | *实时对会议语音进行语音识别* | [麦克风实时语音识别](./samples/speech-recognition/recognize_speech_from_microphone)                    |
| 实时会议语音翻译 | *实时对会议语音进行语音翻译* | [麦克风实时语音翻译](./samples/speech-recognition/translate_speech_from_microphone_for_realtime_stream/)                    |
| 会议录音批量语音识别 | *对会议录音文件进行批量语音识别* | [批量音视频文件语音识别（批量模式）](./samples/speech-recognition/recognize_speech_from_files_by_batch_mode) |
| 会议录音批量语音翻译 | *对会议录音文件进行批量语音翻译* | [批量音视频文件语音翻译（批量模式）](./samples/speech-recognition/translate_speech_from_files_by_realtime_mode) |
| Qwen-Audio-3.0-ASR 实时会议字幕 | *基于 WebSocket 长连接对无时长限制的会议音频流实时转写* | [Qwen-Audio-3.0-ASR 流式语音识别](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-streaming) |
| Qwen-Audio-3.0-ASR 全天会议录音转写 | *异步转写最长 12 小时的会议录音，并通过说话人分离区分发言人* | [Qwen-Audio-3.0-ASR 录音文件转写](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-filetrans) |


* ### :film_strip: 音视频语音分析理解场景
| 典型用法                                                         | 使用说明 | 开发示例                                                                                                            |
|--------------------------------------------------------------| --- |-----------------------------------------------------------------------------------------------------------------|
| 音视频批量语音识别                                                    | *对音视频文件进行批量语音识别* | [批量音视频文件语音识别（批量模式）](./samples/speech-recognition/recognize_speech_from_files_by_batch_mode)                     |
| 音视频批量富信息语音识别                                                 | *对音视频文件中的文本/情绪/事件进行识别* | [批量音视频文件富信息语音识别（批量模式）](./samples/speech-recognition/recognize_speech_and_rich_information_from_files_by_batch_mode) |
| 音视频摘要与问答 <img src="./docs/image/logo.svg" height="15"/> | *对音视频文件进行语音识别，并使用大模型进行摘要总结和问答* | [视频转写并进行翻译摘要和问答](./samples/speech-plus/transcribe-video-and-do-translation-summarization-and-qa)|
| 直播与课堂实时字幕 | *对直播、公开课等长时音频流持续输出低延迟字幕* | [Qwen-Audio-3.0-ASR 流式语音识别](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-streaming)|

* ### :speech_balloon: 语音对话聊天场景
| 典型用法 | 使用说明 | 开发示例                                       |
| --- | --- |--------------------------------------------|
| 一句话实时语音识别和翻译             | *实时从麦克风录音，断句并进行语音识别和翻译* | [麦克风实时一句话语音识别和翻译](./samples/speech-recognition/translate_speech_from_microphone_for_one_sentence/)                     |
| 语音对话聊天 <img src="./docs/image/logo.svg" height="15"/>  | *通过语音与大语言模型进行对话聊天* | [阿里云文档](https://help.aliyun.com/zh/isi/developer-reference/voice-dialogue) |
| 视频对话聊天 <img src="./docs/image/logo.svg" height="15"/>  | *通过多模态大模型进行视频聊天* | [阿里云文档](./samples/conversation/omni) |
| 端到端实时语音对话 <img src="./docs/image/logo.svg" height="15"/>  | *基于 WebSocket 的实时语音对话 SDK 与示例，含陪伴对话、函数调用、推理路由三种智能体场景* | [qwen-audio-3.0-realtime](./samples/conversation/fun-audiochat-realtime) |


## :point_right: 高并发调用

如果您使用Java搭建语音服务，请参考`高并发示例文档`获得最佳的性能。
- [实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide?#rt03-hc-sec)
- [实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#ug-hc-sec)



## :video_game: [Gallery](./samples/gallery)

[Gallery](./samples/gallery) 是为开发者们精心策划的灵感资源库，已包含使用百炼 AI 能力开发的一些有趣应用程序。

我们诚邀更多开发者加入，共同探索和建设这个广阔的技术天地。您的贡献不仅可以丰富我们的资源库，还将为更多开发者提供灵感和帮助，激发更多创新的可能性。无论是分享您的项目和代码，还是提出改进建议，我们都非常期待您的参与。让我们共同努力，打造一个更强大、更具创意的开发者社区！


## :point_right: 常见问题

ASR 调用常见问题请参考[QA文档](docs/QA/paraformer.md)
TTS 调用常见问题请参考[QA文档](docs/QA/cosyvoice.md)

## :point_right: 许可协议

本项目遵循[The MIT License](https://opensource.org/license/MIT)开源协议

## :point_right: 变更记录

### 2026/08/14
- 增加 Qwen-Audio-3.0-TTS 语音合成与声音复刻示例，支持通过指令控制音色风格、方言与情感。
- 增加 Qwen-Audio-3.0-ASR 系列语音识别示例，覆盖非流式识别、流式识别（支持热词与对话上下文）与录音文件转写。

### 2026/07/14
- 增加 Qwen-Audio-3.0-Realtime 端到端实时语音对话模型示例（含陪伴对话、函数调用、推理路由三种场景）。

### 2026/06/16
- 增加百聆音乐生成大模型（Fun-Music）示例，支持通过提示词和歌词生成音乐。
- 优化 Omni 演示程序,使用 session_end 优雅结束。
- 增加 Omni function calling 示例。

### 2025/12/19
- 更新ASR默认模型为fun-asr
- 更新TTS默认模型为cosyvoice-v3-flash

#### 2025/07/21
- 增加omni示例。
- 增加qwen-tts-realtime示例。

#### 2025/06/17
- 增加英文readme文档。
- TTS 相关模型升级为cosyvoice-v2。

#### 2025/02/14
- 增加cosyvoice和paraformer的javascript接入示例。

#### 2025/01/24
- 增加调用call api识别本地单个文件示例，将识别本地视频文件并转opus格式放入gallery。
- 更换html流式音频播放器，wavtools在移动端和Safari有杂音。

#### 2025/01/17
- 调整demo结构，java示例统一为maven项目。
- 增加声音复刻示例。
- 增加调用gummy语音翻译模型示例。
- 增加 Gallery 示例代码目录，及示例项目。

#### 2024/08/14
- 增加 [视频转写并进行翻译摘要和问答](./samples/speech-plus/transcribe-video-and-do-translation-summarization-and-qa) 示例。

#### 2024/08/07
- 优化目录结构和场景示例命名，增加更详细的调用说明。

#### 2024/07/24
- 增加并行调用语音识别和语音合成的python示例。
- 增加朗读故事并实时展示字幕的 python/java 示例。
- 增加使用网页播放流式音频的AI Assistant示例。
- 各示例根节点目录增加更详细的运行说明。

#### 2024/07/19
- 更新文档结构。增加语音质检示例。

#### 2024/07/17
- 更新说明文档。

#### 2024/07/05
- 补充QA文档。

#### 2024/06/25
- 发布初始版本，分别支持从麦克风/文件输入识别，以及语音合成到扬声器和文件的 python/java 示例。
