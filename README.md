# 阿里云百炼 - 通义语音大模型 - 开发示例代码

本仓库以示例代码的形式向开发者展示如何通过<strong>阿里云百炼</strong>调用<strong>通义语音大模型</strong>（包括[CosyVoice](https://fun-audio-llm.github.io/)、[Paraformer](https://github.com/modelscope/FunASR)、[SenseVoice](https://fun-audio-llm.github.io/)等），从而实现<strong>语音识别</strong>（语音转文字）、<strong>语音生成</strong>（文字转语音）等基础功能。以及如何结合阿里云百炼支持的大语言模型（包括通义千问、百川、月之暗面、零一万物、MiniMax等），从而实现<strong>语音聊天对话</strong>、<strong>语音分析理解</strong>、<strong>语音翻译</strong>等高阶AI功能。

开发者可以通过阿里云百炼提供的模型调用 :moneybag: **免费额度** :moneybag: 试用本仓库中的各个示例，还可以直接将这些示例集成进自己的项目中进一步开发。在开发过程中如有任何疑问，都可以通过我们的钉钉 / 微信群进行沟通交流。

<img src="./docs/image/groups.png" height="200"/>

## ⭐最新动态⭐
#### 2024/08/07
- 优化目录结构和场景示例命名，增加更详细的调用说明。

更多历史发布信息请见[变更记录](#point_right-变更记录)。

## :point_right: 示例获取和准备工作
- 您可以通过`git clone`克隆示例工程，或者通过[`Download Zip`](https://github.com/aliyun/alibabacloud-bailian-speech-demo/archive/refs/heads/master.zip)下载完整工程，并在本地解压到文件。

- 在执行示例代码之前，您需要开通**阿里云账号**及**阿里云百炼模型服务**、创建阿里云百炼**API\_KEY**并进行必要的**环境配置**，以及安装阿里云百炼**DashScope SDK**，有关步骤的向导请参见[运行示例代码的前提条件](./PREREQUISITES.md)。某些示例还需要导入必要的依赖，您可以在示例代码所在目录下的README.md文件中查看具体的依赖条件。

## :point_right: 应用场景与开发示例

* ### :rocket: 入门场景

| 典型用法 | 使用说明 | 开发示例                                                                          |
| --- | --- |-------------------------------------------------------------------------------|
| 麦克风语音识别 | *实时从麦克风录音并进行语音识别* | [麦克风实时语音识别](./samples/speech-recognition/recognize_speech_from_microphone)    |
| 音视频文件语音识别 | *对音视频文件进行语音识别* | [单个音视频文件语音识别](./samples/speech-recognition/recognize_speech_from_single_file) |
| 语音合成 | *将文字合成为语音并保存到文件* | [语音合成并保存（简单模式）](./samples/speech-synthesizer/synthesize_speech_from_text)         |

* ### :telephone: 电话客服中心机器人及对话分析理解场景
| 典型用法 | 使用说明 | 开发示例                                                                                        |
| --- | --- |---------------------------------------------------------------------------------------------|
| 实时通话语音识别 | *实时对电话系统通话进行语音识别* | [麦克风实时语音识别](./samples/speech-recognition/recognize_speech_from_microphone)                    |
| 实时回复语音合成 | *对客服机器人回复进行语音合成* | [语音合成并保存（简单模式）](./samples/speech-synthesizer/synthesize_speech_from_text)                       |
| 通话录音批量语音识别 | *对客服中心通话录音文件进行批量语音识别* | [批量音视频文件语音识别（批量模式）](./samples/speech-recognition/recognize_speech_from_files_by_batch_mode) |


* ### :loudspeaker: 语音播报及配音场景
| 典型用法 | 使用说明 | 开发示例                                                                                |
| --- | --- |-------------------------------------------------------------------------------------|
| 信息播报 | *对各类文字进行语音合成* | [语音合成并保存（简单模式）](./samples/speech-synthesizer/synthesize_speech_from_text)               |
| 大语言模型实时输出播报 <img src="./docs/image/logo.svg" height="15"/> | *对大语言模型产生的实时输出进行语音合成并播报* | [语音合成实时LLM输出并播放（流式模式）](./samples/speech-synthesizer/synthesize_speech_from_llm_by_streaming_mode)      |

* ### :raising_hand: 会议语音分析理解场景
| 典型用法 | 使用说明 | 开发示例                                                                                        |
| --- | --- |---------------------------------------------------------------------------------------------|
| 实时会议语音识别 | *实时对会议语音进行语音识别* | [麦克风实时语音识别](./samples/speech-recognition/recognize_speech_from_microphone)                    |
| 会议录音批量语音识别 | *对会议录音文件进行批量语音识别* | [批量音视频文件语音识别（批量模式）](./samples/speech-recognition/recognize_speech_from_files_by_batch_mode) |


* ### :film_strip: 音视频语音分析理解场景
| 典型用法                                                   | 使用说明                      | 开发示例                                                                                        |
|--------------------------------------------------------|---------------------------|---------------------------------------------------------------------------------------------|
| 音视频批量语音识别                        | *对音视频文件进行批量语音识别*          | [批量音视频文件语音识别（批量模式）](./samples/speech-recognition/recognize_speech_from_files_by_batch_mode) |
| 音视频批量富文本语音识别            | *对音视频文件中的文本/情绪/事件进行识别*    | [批量音视频文件富文本语音识别（批量模式）](./samples/speech-recognition/recognize_speech_with_paralinguistics_from_files_by_batch_mode)  |
| 音视频摘要总结 <img src="./docs/image/logo.svg" height="15"/> | *对音视频文件进行语音识别，并使用大模型进行摘要* | Comming Soon                                                                                |

* ### :speech_balloon: 语音对话聊天场景
| 典型用法 | 使用说明 | 开发示例                                       |
| --- | --- |--------------------------------------------|
| 语音对话聊天 <img src="./docs/image/logo.svg" height="15"/>  | *通过语音与大语言模型进行对话聊天* | coming soon |

## :point_right: 常见问题

常见问题请参考[QA文档](docs/QA/qa.md)

## :point_right: 许可协议

本项目遵循[The MIT License](https://opensource.org/license/MIT)开源协议

## :point_right: 变更记录

#### 2024/08/07
- 优化目录结构和场景示例命名，增加更详细的调用说明。

### 2024/07/24
- 增加并行调用语音识别和语音合成的python示例。
- 增加朗读故事并实时展示字幕的 python/java 示例。
- 增加使用网页播放流式音频的AI Assistant示例。
- 各示例根节点目录增加更详细的运行说明。
- VoiceChat示例运行代码优化。

#### 2024/07/19
- 更新文档结构。增加VoiceChat示例、增加语音质检示例。

#### 2024/07/17
- 更新说明文档。

#### 2024/07/05
- 补充QA文档。

#### 2024/06/25
- 发布初始版本，分别支持从麦克风/文件输入识别，以及语音合成到扬声器和文件的 python/java 示例。
