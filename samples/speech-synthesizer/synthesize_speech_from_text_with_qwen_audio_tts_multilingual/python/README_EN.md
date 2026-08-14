[comment]: # (title and brief introduction of the sample)
## Qwen-Audio-3.0-TTS All-in-One Multilingual Speech Synthesis

[简体中文](./README.md) | English

## Python

[comment]: # (prerequisites)
### :point_right: Prerequisites

1. #### Configure the Alibaba Cloud Model Studio API-KEY

    Before running this sample you need an Alibaba Cloud account, an Alibaba Cloud Model Studio API_KEY and the necessary environment configuration. For the detailed steps see: [PREREQUISITES_EN.md](../../../../PREREQUISITES_EN.md)

1. #### Install ffmpeg

    This sample requires ffmpeg for audio decoding. It is recommended to download and install it from the official website and add the ffmpeg installation path to your environment variables: [Download from ffmpeg's official website](https://www.ffmpeg.org/download.html). You can also refer to the document [How to install ffmpeg](../../../../docs/QA/ffmpeg_en.md).

1. #### Install Python dependencies

    The Alibaba Cloud Model Studio SDK requires Python 3.8 or above. Install this sample's dependencies with:
    ```commandline
    pip3 install -r requirements.txt
    ```

[comment]: # (how to run the sample and expected results)
### :point_right: Run the sample

With no arguments, the sample uses **one single voice** `longanhuan_mtlv7` to synthesize the same greeting in **16 languages**, playing each back in real time and saving them as `result_<language-code>.mp3`:

```commandline
python3 run.py
```

The terminal output looks like:

```
[3/16] 日语 日本語 (ja)
  instruction: 请讲日语。
  text: こんにちは、アリババクラウドの音声合成サービスへようこそ。
  requestId: bb9b333ac4b0416ca538532d0e2b09cd, first_package_delay: 445ms
  saved to: result_ja.mp3
```

The thing to listen for: **the speaker timbre stays consistent as the language changes** — that is exactly what an all-in-one multilingual voice buys you.

You can also synthesize a single language, or supply your own text:

```commandline
python3 run.py -l ja                          # Japanese only, using the built-in sample text
python3 run.py -l fr -t "Bonjour à tous."     # a custom French sentence
python3 run.py -l ko -o ./out/korean.mp3      # choose the output path
```

Available language codes: `zh` `en` `ja` `ko` `fr` `de` `ru` `it` `es` `pt` `ar` `th` `vi` `id` `ms` `tl`

> :bulb: `-t/--text` must be combined with `-l/--lid`, because the model needs to know which language the text is in. Passing `-t` alone exits with an error.

### :point_right: Implementation notes

The language is selected by `language_hints` together with `instruction`. The per-language instruction is maintained in the `LANGUAGES` table in `run.py`:

```python
kwargs = {
    'model': MODEL,
    'voice': VOICE,
    'language_hints': [lid],
    'callback': callback,
}
if instruction is not None:
    kwargs['instruction'] = instruction
```

**Chinese and English have `instruction` set to `None`** (`language_hints` alone is enough); the other 14 languages must send their matching instruction. For the full table and the verification results, see the [parent README](../README_EN.md).

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../../docs/image/group.png" width="400"/>
