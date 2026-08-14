[comment]: # (title and brief introduction of the sample)
## Qwen-Audio-3.0-TTS Text Normalization (TN) Showcase

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
Run this sample with:

```commandline
python3 run.py
```

The sample synthesizes three **deliberately difficult** Chinese passages in order. Each one is played back through the speaker in real time and saved as `result_tn_1.mp3` ~ `result_tn_3.mp3`.

Before each synthesis the terminal prints that passage's **checkpoint list**, pairing the written form with the reading you should hear:

```
[2] 医药检测：百分号 + 波浪范围符 + 单位
  原文: 在一次检测中，1毫升20%甘露醇药液中可查出粒径4～30微米的微粒598个。
  检查点（应当听到的读法）:
    - 20%        -> 百分之二十 —— 而不是"二十百分号"
    - 4～30微米    -> 四到三十微米 —— 全角波浪号读作"到"，不能读出符号名
```

Listen along and compare against the checkpoints. Polyphone tones and digit-grouping choices cannot be asserted programmatically — see the [parent README](../README_EN.md) for why.

You can add your own hard-to-read text by editing `TN_CASES` in `run.py`; `checkpoints` only drives the terminal output and does not affect synthesis.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="../../../../docs/image/group.png" width="400"/>
