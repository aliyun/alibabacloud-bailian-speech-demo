# Alibaba Cloud Bailian - Tongyi Speech Large Models - Development Examples

English | [简体中文](./README.md)

This repository demonstrates how to call **Speech Large Models** (including [Qwen-Audio-3.0-TTS](https://help.aliyun.com/zh/model-studio/cosyvoice-websocket-api/), [Qwen-Audio-3.0-ASR](https://help.aliyun.com/zh/model-studio/fun-asr-realtime-websocket-api), [CosyVoice](https://fun-audio-llm.github.io/), [Fun-ASR](https://github.com/modelscope/FunASR), etc.) via **Alibaba Cloud Bailian**, enabling functions like **speech recognition** (speech-to-text), **speech synthesis** (text-to-speech), and advanced AI capabilities such as **voice chat**, **audio analysis**, and **real-time translation** when integrated with large language models (e.g., Qwen-OMNI, Qwen, Baichuan, Moonshot, 01.AI, MiniMax). Developers can test examples using Bailian's **free quota** and integrate these samples into their projects for further development. For technical support, join our DingTalk group.

<img src="./docs/image/group.png" height="200"/>

## ⭐ Latest Updates ⭐

#### 2026/08/14
- Added Qwen-Audio-3.0-TTS speech synthesis and voice cloning examples, with voice style, dialect and emotion controllable by instruction.
- Added the Qwen-Audio-3.0-ASR speech recognition examples, covering non-streaming recognition, streaming recognition (with hotwords and dialog context) and recorded-file transcription.

#### 2026/07/14
- Added Qwen-Audio-3.0-Realtime end-to-end real-time voice conversation example (companion chat, tool calling, and reasoning routing scenarios).

## :point_right: Getting Started
- Clone the repository via `git clone` or download the [ZIP file](https://github.com/aliyun/alibabacloud-bailian-speech-demo/archive/refs/heads/master.zip).
- Prerequisites: Create an **Alibaba Cloud account**, activate **Bailian Model Service**, generate an **API_KEY**, configure the environment, and install the **DashScope SDK**. Detailed steps are in [PREREQUISITES.md](./PREREQUISITES.md). Check individual `README.md` files in example directories for specific dependencies.

## :point_right: Use Cases & Examples

### :rocket: Recommended Scenarios
| Use Case | Description | Example |
|---------|-------------|---------|
| Qwen-Audio-3.0-ASR Streaming Recognition | Unlimited-duration real-time streaming recognition with hotwords and dialog context | [Streaming Recognition](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-streaming) |
| Qwen-Audio-3.0-ASR Non-Streaming Recognition | One-shot recognition of an audio URL, with dialog context, up to 5 min / 2 GB | [Non-Streaming Recognition](./samples/speech-recognition/recognize_speech_qwen-audio_3.0_asr_flash) |
| Qwen-Audio-3.0-ASR File Transcription | Asynchronous transcription of recordings up to 12 hours, with speaker diarization | [File Transcription](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-filetrans) |
| Qwen-Audio-3.0-TTS Synthesis | Control style, dialect and emotion by instruction, with real-time streaming playback | [Instruction-Controlled Synthesis](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_model) |
| Qwen-Audio-3.0-TTS Voice Cloning | Clone a voice from one audio sample and synthesize any text with it | [Voice Cloning Synthesis](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_by_cloned_voice) |
| Qwen-Audio-3.0-Realtime Voice Chat | End-to-end real-time voice conversation over WebSocket (companion chat, tool calling, reasoning routing) | [qwen-audio-3.0-realtime](./samples/conversation/fun-audiochat-realtime) |

> **More Agent scenarios**: [qwen-audio-agent](https://github.com/QwenAudio/qwen-audio-agent) provides production-grade Agent examples built on Qwen-Audio-3.0-Realtime, including multi-turn memory, tool orchestration, and multimodal input.

### :sparkles: Advanced Usage
| Use Case | Description | Example |
|---------|-------------|---------|
| Streaming + Dialog Context | Pass dialog history or domain terms to improve accuracy, with limit-aware trimming | [Dialog Context](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-context) |
| Streaming + Precompiled Vocabulary | Create a vocabulary once and reuse by ID; covers the full create/query/recognize/delete lifecycle | [Precompiled Vocabulary](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-vocabulary) |
| TTS Instruction Guide | Style, dialect, emotion tags and combined usage with a full tag reference table | [Instruction Guide](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_by_instruction) |
| TTS Text Normalization (TN) | Synthesis of hard-to-read text: quantities, units, percent signs, ranges, hotline numbers and polyphones | [Text Normalization Showcase](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_text_normalization) |
| TTS All-in-One Multilingual | One single voice longanhuan_mtlv7 speaks 16 languages while keeping the same timbre | [Multilingual Synthesis](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_multilingual) |

### :musical_note: Music Generation
| Use Case | Description | Example |
|---------|-------------|---------|
| Generate Music from Prompt | Input music style description, auto-generate lyrics and sing | [Generate from Prompt](./samples/music-generation/generate_music_from_prompt) |
| Generate Music from Lyrics | Provide custom lyrics, AI composes and sings | [Generate from Lyrics](./samples/music-generation/generate_music_from_lyrics) |

### :telephone: Call Center & Dialogue Analysis
| Use Case | Description | Example |
|---------|-------------|---------|
| Real-Time Call Recognition | Real-time speech recognition for call systems | [Microphone Real-Time Recognition](./samples/speech-recognition/recognize_speech_from_microphone) |
| Real-Time Agent Response Synthesis | Synthesize agent responses | [Streaming Synthesis](./samples/speech-synthesizer/synthesize_speech_from_text_by_streaming_mode) |
| Custom Voice Synthesis | Voice cloning for personalized TTS | [Voice Cloning Example](./samples/speech-synthesizer/synthesize_speech_from_text_with_cloned_voice) |
| Custom Voice Synthesis by Qwen-Audio-3.0-TTS | Voice cloning with the Qwen-Audio-3.0-TTS model | [Voice Cloning Example](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_by_cloned_voice) |
| Batch Call Recording Recognition | Batch processing of call recordings | [Batch Mode Recognition](./samples/speech-recognition/recognize_speech_from_files_by_batch_mode) |
| Qwen-Audio-3.0-ASR Real-Time Call Recognition | Improve accuracy on product names and business terms with hotwords and dialog context | [Qwen-Audio-3.0-ASR Streaming Recognition](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-streaming) |
| Qwen-Audio-3.0-ASR Call Recording Review | Asynchronously transcribe calls and separate agent from customer via speaker diarization | [Qwen-Audio-3.0-ASR File Transcription](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-filetrans) |

### :loudspeaker: Voice Broadcasting & Dubbing
| Use Case | Description | Example |
|---------|-------------|---------|
| Information Broadcasting | Convert text to speech for announcements | [Streaming Synthesis](./samples/speech-synthesizer/synthesize_speech_from_text_by_streaming_mode) |
| Real-Time LLM Output Broadcasting | Stream LLM outputs as speech | [LLM Streaming Synthesis](./samples/speech-synthesizer/synthesize_speech_from_llm_by_streaming_mode) |
| Dialect & Emotional Dubbing | Set dialect and speaking style by instruction, or control emotion with inline tags | [Instruction-Controlled Synthesis](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_model) |
| Signature Voice Broadcasting | Clone a host or brand voice for consistent content broadcasting | [Voice Cloning Synthesis](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_by_cloned_voice) |
| Multilingual Broadcasting | Switch among 16 languages with one All-in-One voice for internationalized content | [Multilingual Synthesis](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_multilingual) |
| Numeric & Professional Text | Text Normalization auto-handles quantities, units and symbols for natural reading | [Text Normalization Showcase](./samples/speech-synthesizer/synthesize_speech_from_text_with_qwen_audio_tts_text_normalization) |

### :raising_hand: Meeting Analysis
| Use Case | Description | Example |
|---------|-------------|---------|
| Real-Time Meeting Recognition | Real-time speech-to-text for meetings | [Microphone Real-Time Recognition](./samples/speech-recognition/recognize_speech_from_microphone) |
| Real-Time Meeting Translation | Real-time multilingual translation | [Real-Time Translation](./samples/speech-recognition/translate_speech_from_microphone_for_realtime_stream) |
| Batch Meeting Recognition | Batch processing of meeting recordings | [Batch Mode Recognition](./samples/speech-recognition/recognize_speech_from_files_by_batch_mode) |
| Batch Meeting Translation | Batch translation of meeting recordings | [Batch Mode Translation](./samples/speech-recognition/translate_speech_from_files_by_realtime_mode) |
| Qwen-Audio-3.0-ASR Real-Time Meeting Captions | Transcribe unlimited-duration meeting audio streams over a WebSocket connection | [Qwen-Audio-3.0-ASR Streaming Recognition](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-streaming) |
| Qwen-Audio-3.0-ASR All-Day Meeting Transcription | Asynchronously transcribe recordings up to 12 hours and tell speakers apart via diarization | [Qwen-Audio-3.0-ASR File Transcription](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-filetrans) |

### :film_strip: Audio/Video Analysis
| Use Case | Description | Example |
|---------|-------------|---------|
| Batch Audio/Video Recognition | Batch speech recognition | [Batch Recognition](./samples/speech-recognition/recognize_speech_from_files_by_batch_mode) |
| Rich Info Recognition | Extract text/emotion/events from audio/video | [Rich Info Recognition](./samples/speech-recognition/recognize_speech_and_rich_information_from_files_by_batch_mode) |
| Summary & Q&A | Summarize and answer questions from audio/video | [Transcribe & QA](./samples/speech-plus/transcribe-video-and-do-translation-summarization-and-qa) |
| Live & Classroom Captions | Continuously caption long-running live streams and lectures with low latency | [Qwen-Audio-3.0-ASR Streaming Recognition](./samples/speech-recognition/recognize_speech_qwen-audio-3.0-asr-flash-streaming) |

### :speech_balloon: Voice Chat
| Use Case | Description | Example |
|---------|-------------|---------|
| Sentence-Level Recognition & Translation | Real-time sentence recognition and translation | [Sentence-Level Example](./samples/speech-recognition/translate_speech_from_microphone_for_one_sentence/) |
| Voice Chat with LLM | Voice interaction with large language models | [Alibaba Cloud Documentation](https://help.aliyun.com/zh/isi/developer-reference/voice-dialogue) |
| Video Chat with LLM | Video chat via multimodal large models | [Omni Example](./samples/conversation/omni) |
| End-to-End Real-Time Voice Chat | WebSocket-based real-time voice conversation SDK and examples (companion chat, tool calling, reasoning routing) | [qwen-audio-3.0-realtime](./samples/conversation/fun-audiochat-realtime) |

## :point_right: High-Concurrency Usage
For Java-based services, refer to the high-concurrency guides:
- [real-time speech recognition](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide?#rt03-hc-sec)
- [real-time speech synthesis](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#ug-hc-sec)

## :video_game: [Gallery](./samples/gallery)
The Gallery showcases creative applications built with Bailian AI capabilities. Contribute your projects to inspire others!

## :point_right: FAQ
- Paraformer issues: [QA Document](docs/QA/paraformer_en.md)
- CosyVoice issues: [QA Document](docs/QA/cosyvoice_en.md)

## :point_right: License
This project is licensed under the [MIT License](https://opensource.org/license/MIT).

## :point_right: Changelog

#### 2026/08/14
- Added Qwen-Audio-3.0-TTS speech synthesis and voice cloning examples, with voice style, dialect and emotion controllable by instruction.
- Added the Qwen-Audio-3.0-ASR speech recognition examples, covering non-streaming recognition, streaming recognition (with hotwords and dialog context) and recorded-file transcription.

#### 2026/07/14
- Added Qwen-Audio-3.0-Realtime end-to-end real-time voice conversation example (companion chat, tool calling, and reasoning routing scenarios).

#### 2026/06/16
- Added Fun-Music (Bailing Music Generation) examples, supporting music generation from prompts and lyrics.
- Improved graceful session finish in the Omni demo.
- Added Omni function calling example.

#### 2025/12/19
- update default asr model to fun-asr
- update default tts model to cosyvoice-v3-flash

#### 2025/07/21
- Added qwen-omni demo.
- Added qwen-tts-realtime demo.

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
