# Alibaba Cloud Bailian - Tongyi Speech Large Models - Development Examples

English | [简体中文](./README.md)

This repository demonstrates how to call **Tongyi Speech Large Models** (including [CosyVoice](https://fun-audio-llm.github.io/), [Paraformer](https://github.com/modelscope/FunASR), [SenseVoice](https://fun-audio-llm.github.io/), [Gummy](https://fun-audio-llm.github.io/)) via **Alibaba Cloud Bailian**, enabling functions like **speech recognition** (speech-to-text), **speech synthesis** (text-to-speech), and advanced AI capabilities such as **voice chat**, **audio analysis**, and **real-time translation** when integrated with large language models (e.g., Qwen, Baichuan, Moonshot, 01.AI, MiniMax). Developers can test examples using Bailian's **free quota** and integrate these samples into their projects for further development. For technical support, join our DingTalk/WeChat groups.

<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" height="200"/>

## ⭐ Latest Updates ⭐
#### 2025/01/17
- ✨ Added [Microphone Real-Time Speech Translation](./samples/speech-recognition/translate_speech_from_microphone_for_realtime_stream) example.
- ✨ Added [Batch Audio/Video File Translation (Real-Time Mode)](./samples/speech-recognition/translate_speech_from_files_by_realtime_mode/) example.
- ✨ Added [Microphone Real-Time Sentence Recognition & Translation](./samples/speech-recognition/translate_speech_from_microphone_for_one_sentence/) example.
- ✨ Added [Voice Cloning for Speech Synthesis (Streaming Mode)](./samples/speech-synthesizer/synthesize_speech_from_text_with_cloned_voice/) example.
- ✨ Added [Gallery](./samples/gallery/) with advanced projects:
  - [Sentence-by-Sentence Subtitle Display](./samples/gallery/read-and-display-subtitles/)
  - [Multi-Role Story Narration](./samples/gallery/reading-story-in-multiple-role/)
  - [Real-Time On-Screen Subtitle](./samples/gallery/record-from-microphone-and-display-realtime-subtitle/)
  - [Chinese-to-English Real-Time Translation & Playback](./samples/gallery/translate-audio-from-microphone-and-play-in-realtime/)
  - [Web AI Assistant](./samples/gallery/input-text-out-audio-html-ai-assistant/)
  - [Web Audio Recording & Recognition](./samples/gallery/input-audio-out-text-html/)
  - ✨ Optimized Java example structure with independent Maven projects.

## :point_right: Getting Started
- Clone the repository via `git clone` or download the [ZIP file](https://github.com/aliyun/alibabacloud-bailian-speech-demo/archive/refs/heads/master.zip).
- Prerequisites: Create an **Alibaba Cloud account**, activate **Bailian Model Service**, generate an **API_KEY**, configure the environment, and install the **DashScope SDK**. Detailed steps are in [PREREQUISITES.md](./PREREQUISITES.md). Check individual `README.md` files in example directories for specific dependencies.

## :point_right: Use Cases & Examples

### :rocket: Beginner Scenarios
| Use Case | Description | Example |
|---------|-------------|---------|
| Microphone Speech Recognition | Real-time speech recognition from microphone | [Microphone Real-Time Recognition](./samples/speech-recognition/recognize_speech_from_microphone) |
| Microphone Real-Time Translation | Real-time speech translation from microphone | [Microphone Real-Time Translation](./samples/speech-recognition/translate_speech_from_microphone_for_realtime_stream) |
| Audio/Video File Recognition | Speech recognition for local files | [Single File Recognition](./samples/speech-recognition/recognize_speech_from_single_file) |
| Speech Synthesis | Convert text to speech and save as file | [Simple Synthesis](./samples/speech-synthesizer/synthesize_speech_from_text) |

### :telephone: Call Center & Dialogue Analysis
| Use Case | Description | Example |
|---------|-------------|---------|
| Real-Time Call Recognition | Real-time speech recognition for call systems | [Microphone Real-Time Recognition](./samples/speech-recognition/recognize_speech_from_microphone) |
| Real-Time Agent Response Synthesis | Synthesize agent responses | [Streaming Synthesis](./samples/speech-synthesizer/synthesize_speech_from_text_by_streaming_mode) |
| Custom Voice Synthesis | Voice cloning for personalized TTS | [Voice Cloning Example](./samples/speech-synthesizer/synthesize_speech_from_text_with_cloned_voice) |
| Batch Call Recording Recognition | Batch processing of call recordings | [Batch Mode Recognition](./samples/speech-recognition/recognize_speech_from_files_by_batch_mode) |

### :loudspeaker: Voice Broadcasting & Dubbing
| Use Case | Description | Example |
|---------|-------------|---------|
| Information Broadcasting | Convert text to speech for announcements | [Streaming Synthesis](./samples/speech-synthesizer/synthesize_speech_from_text_by_streaming_mode) |
| Real-Time LLM Output Broadcasting | Stream LLM outputs as speech | [LLM Streaming Synthesis](./samples/speech-synthesizer/synthesize_speech_from_llm_by_streaming_mode) |

### :raising_hand: Meeting Analysis
| Use Case | Description | Example |
|---------|-------------|---------|
| Real-Time Meeting Recognition | Real-time speech-to-text for meetings | [Microphone Real-Time Recognition](./samples/speech-recognition/recognize_speech_from_microphone) |
| Real-Time Meeting Translation | Real-time multilingual translation | [Real-Time Translation](./samples/speech-recognition/translate_speech_from_microphone_for_realtime_stream) |
| Batch Meeting Recognition | Batch processing of meeting recordings | [Batch Mode Recognition](./samples/speech-recognition/recognize_speech_from_files_by_batch_mode) |
| Batch Meeting Translation | Batch translation of meeting recordings | [Batch Mode Translation](./samples/speech-recognition/translate_speech_from_files_by_realtime_mode) |

### :film_strip: Audio/Video Analysis
| Use Case | Description | Example |
|---------|-------------|---------|
| Batch Audio/Video Recognition | Batch speech recognition | [Batch Recognition](./samples/speech-recognition/recognize_speech_from_files_by_batch_mode) |
| Rich Info Recognition | Extract text/emotion/events from audio/video | [Rich Info Recognition](./samples/speech-recognition/recognize_speech_and_rich_information_from_files_by_batch_mode) |
| Summary & Q&A | Summarize and answer questions from audio/video | [Transcribe & QA](./samples/speech-plus/transcribe-video-and-do-translation-summarization-and-qa) |

### :speech_balloon: Voice Chat
| Use Case | Description | Example |
|---------|-------------|---------|
| Sentence-Level Recognition & Translation | Real-time sentence recognition and translation | [Sentence-Level Example](./samples/speech-recognition/translate_speech_from_microphone_for_one_sentence/) |
| Voice Chat with LLM | Voice interaction with large language models | [Alibaba Cloud Documentation](https://help.aliyun.com/zh/isi/developer-reference/voice-dialogue) |

## :point_right: High-Concurrency Usage
For Java-based services, refer to the high-concurrency guides:
- [Paraformer](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-in-high-concurrency-scenarios) for real-time speech recognition.
- [Sambert](https://help.aliyun.com/zh/model-studio/developer-reference/sambert-in-high-concurrency-scenarios) for speech synthesis.
- [CosyVoice](https://help.aliyun.com/zh/model-studio/developer-reference/high-concurrency-scenarios) for large model synthesis.

## :video_game: [Gallery](./samples/gallery)
The Gallery showcases creative applications built with Bailian AI capabilities. Contribute your projects to inspire others!

## :point_right: FAQ
- Paraformer issues: [QA Document](docs/QA/paraformer_en.md)
- CosyVoice issues: [QA Document](docs/QA/cosyvoice_en.md)

## :point_right: License
This project is licensed under the [MIT License](https://opensource.org/license/MIT).

## :point_right: Changelog

#### 2025/06/17
- Added English readme docs
- TTS model update to cosyvoice-v2

#### 2025/02/14
- Added JavaScript examples for CosyVoice and Paraformer.

#### 2025/01/24
- Added local file recognition example with Opus format conversion.
- Updated HTML streaming audio player for mobile/Safari compatibility.

#### 2025/01/17
- Unified Java examples as Maven projects.
- Added voice cloning and Gummy translation examples.
- Introduced Gallery section.

#### 2024/08/14
- Added [Transcribe \& QA](./samples/speech-plus/transcribe-video-and-do-translation-summarization-and-qa) example.

#### 2024/07/24
- Added parallel speech recognition/synthesis examples.
- Added story narration with real-time subtitles (Python/Java).
- Added web-based AI Assistant example.

#### 2024/07/19
- Updated documentation structure with speech quality inspection examples.

#### 2024/07/05
- Added QA documentation.

#### 2024/06/25
- Initial release with Python/Java examples for microphone/file input and speech synthesis.
