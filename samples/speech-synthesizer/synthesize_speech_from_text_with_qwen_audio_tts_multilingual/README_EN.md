[comment]: # (title and brief introduction of the sample)
## Qwen-Audio-3.0-TTS All-in-One Multilingual Speech Synthesis

[简体中文](./README.md) | English

`longanhuan_mtlv7` is an **all-in-one multilingual voice**: **a single voice id speaks 16 languages**, so you never have to swap voices when switching languages, and the speaker timbre stays recognizably the same throughout. That makes it a good fit for "one brand voice serving a global audience" — multilingual customer-service announcements, multilingual product tours, or a unified voice identity for apps going global.

### :point_right: The 16 supported languages

| Language | Code | Language | Code |
| --- | --- | --- | --- |
| Chinese | `zh` | Arabic | `ar` |
| English | `en` | Thai | `th` |
| Japanese | `ja` | Vietnamese | `vi` |
| Korean | `ko` | Indonesian | `id` |
| French | `fr` | Malay | `ms` |
| German | `de` | Filipino | `tl` |
| Russian | `ru` | Italian | `it` |
| Spanish | `es` | Portuguese | `pt` |

### :point_right: Key usage: language_hints and instruction

The language is selected by two parameters working together:

```python
synthesizer = SpeechSynthesizer(
    model='qwen-audio-3.0-tts-flash',
    voice='longanhuan_mtlv7',
    language_hints=['ja'],      # tells the model which language the text is in
    instruction='请讲日语。',     # explicitly asks the model to speak Japanese
    callback=callback,
)
```

> :warning: **Chinese and English need `language_hints` only.** The other 14 languages **must also receive the matching `instruction`**, otherwise the model may read the text using Chinese or English pronunciation.

The instruction for each language:

| Code | instruction | Code | instruction |
| --- | --- | --- | --- |
| `zh` | *(not needed)* | `ar` | `请讲阿拉伯语。` |
| `en` | *(not needed)* | `th` | `请讲泰语。` |
| `ja` | `请讲日语。` | `vi` | `请讲越南语。` |
| `ko` | `请讲韩语。` | `id` | `请讲印尼语。` |
| `fr` | `请讲法语。` | `ms` | `请讲马来语。` |
| `de` | `请讲德语。` | `tl` | `请讲菲律宾语。` |
| `ru` | `请讲俄语。` | `it` | `请讲意大利语。` |
| `es` | `请讲西班牙语。` | `pt` | `请讲葡萄牙语。` |

### :point_right: Verification

All 16 languages in this sample were actually run and verified: the synthesized audio was fed back into speech recognition to confirm the output really is in the target language, rather than the text being read with another language's pronunciation.

| Verification method | Languages covered | Result |
| --- | --- | --- |
| `paraformer-realtime-v2` round-trip transcription | `zh` `en` `ja` `ko` `fr` `de` `ru` | source text recovered correctly |
| `qwen3-asr-flash` round-trip + language ID (LID) | `es` `pt` `it` `ar` `th` `vi` `id` `ms` `tl` | LID matches the target language |

> :bulb: The one exception is Malay (`ms`), which LID reported as `id`. Malay and Indonesian are extremely close and recognizers routinely conflate them; the round-trip transcript nevertheless uses Malay wording (`perkhidmatan sintesis pertuturan`), so the language itself is correct.

### :point_right: A note on audio formats

The sample outputs MP3 by default, which is convenient for real-time playback and saving. For WAV, pass `format=AudioFormat.WAV_24000HZ_MONO_16BIT`.

> :warning: The length fields in a streamed WAV header are **placeholders** (observed value: `2147483583`). Dumping the stream straight into a `.wav` file therefore produces a header that declares an absurd duration, which stricter players and audio libraries may fail to parse. To get a well-formed WAV file, patch the `RIFF` and `data` chunk sizes after writing finishes.

---

[comment]: # (supported programming languages of the sample)
### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: Reference
| Recommended Model | Voice | API Documentation |
| --- | --- | --- |
| **Qwen-Audio-3.0-TTS** (`qwen-audio-3.0-tts-flash` / `qwen-audio-3.0-tts-plus`) | `longanhuan_mtlv7` | [Realtime Speech Synthesis](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide) |

### :point_right: Expected Results

Running `python run.py` with no arguments synthesizes the same greeting in all 16 languages using **one single voice**, plays each one back in real time and saves them as `result_<language-code>.mp3`, making it easy to compare how that one voice sounds across languages.

You can also synthesize a single language, or supply your own text:

```commandline
python3 run.py -l ja                          # Japanese only, using the built-in sample text
python3 run.py -l fr -t "Bonjour à tous."     # a custom French sentence
python3 run.py -l ko -o ./out/korean.mp3      # choose the output path
```

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../docs/image/group.png" width="400"/>
