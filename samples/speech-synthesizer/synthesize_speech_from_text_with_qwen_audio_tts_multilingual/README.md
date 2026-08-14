[comment]: # (title and brief introduction of the sample)
## Qwen-Audio-3.0-TTS All-in-One 多语言语音合成

简体中文 | [English](./README_EN.md)

`longanhuan_mtlv7` 是一个 **All-in-One 多语言音色**：**同一个音色 ID 支持 16 种语言**，切换语种时无需更换音色，说话人的音色特征保持一致。这使它适合「一个品牌声音服务全球用户」的场景——多语种客服播报、多语言产品介绍、出海应用的统一语音形象等。

### :point_right: 支持的 16 种语言

| 语种 | 代码 | 语种 | 代码 |
| --- | --- | --- | --- |
| 中文 | `zh` | 阿拉伯语 | `ar` |
| 英语 | `en` | 泰语 | `th` |
| 日语 | `ja` | 越南语 | `vi` |
| 韩语 | `ko` | 印尼语 | `id` |
| 法语 | `fr` | 马来语 | `ms` |
| 德语 | `de` | 菲律宾语 | `tl` |
| 俄语 | `ru` | 意大利语 | `it` |
| 西班牙语 | `es` | 葡萄牙语 | `pt` |

### :point_right: 关键用法：language_hints 与 instruction

语种由两个参数共同决定：

```python
synthesizer = SpeechSynthesizer(
    model='qwen-audio-3.0-tts-flash',
    voice='longanhuan_mtlv7',
    language_hints=['ja'],      # 告诉模型输入文本是什么语种
    instruction='请讲日语。',     # 显式要求模型用该语种说话
    callback=callback,
)
```

> :warning: **中文和英文只需要 `language_hints`**，其余 14 种语言**还必须传入对应的 `instruction`**，否则模型可能用中文或英文的发音方式去念这段文本。

各语种对应的指令：

| 代码 | instruction | 代码 | instruction |
| --- | --- | --- | --- |
| `zh` | *（不需要）* | `ar` | `请讲阿拉伯语。` |
| `en` | *（不需要）* | `th` | `请讲泰语。` |
| `ja` | `请讲日语。` | `vi` | `请讲越南语。` |
| `ko` | `请讲韩语。` | `id` | `请讲印尼语。` |
| `fr` | `请讲法语。` | `ms` | `请讲马来语。` |
| `de` | `请讲德语。` | `tl` | `请讲菲律宾语。` |
| `ru` | `请讲俄语。` | `it` | `请讲意大利语。` |
| `es` | `请讲西班牙语。` | `pt` | `请讲葡萄牙语。` |

### :point_right: 实测验证

本示例的 16 种语言均已实跑验证：合成音频送回语音识别做回环，确认输出的确是目标语种，而非用其他语种的发音方式硬念。

| 验证方式 | 覆盖语种 | 结果 |
| --- | --- | --- |
| `paraformer-realtime-v2` 回环转写 | `zh` `en` `ja` `ko` `fr` `de` `ru` | 原文均被正确还原 |
| `qwen3-asr-flash` 回环 + 语种识别（LID） | `es` `pt` `it` `ar` `th` `vi` `id` `ms` `tl` | LID 与目标语种一致 |

> :bulb: 唯一的例外是马来语（`ms`）被 LID 判定为 `id`。马来语与印尼语高度近似，识别侧的语种判定容易混淆；但回环转写文本使用的是马来语词汇（`perkhidmatan sintesis pertuturan`），语种本身是正确的。

### :point_right: 音频格式说明

示例默认使用 MP3 输出，便于实时播放和保存。若需要 WAV，可传入 `format=AudioFormat.WAV_24000HZ_MONO_16BIT`。

> :warning: 流式返回的 WAV 头部长度字段是**占位值**（实测为 `2147483583`）。若把流式数据直接落盘成 `.wav`，文件头声明的时长会是错误的巨大值，部分严格的播放器或音频库会解析异常。如需规范的 WAV 文件，应在写入完成后回填 `RIFF` 与 `data` 块的长度字段。

---

[comment]: # (supported programming languages of the sample)
### :point_right: 编程语言
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: 参考详情
| 推荐模型 | 音色 | API 文档 |
| --- | --- | --- |
| **Qwen-Audio-3.0-TTS** (`qwen-audio-3.0-tts-flash` / `qwen-audio-3.0-tts-plus`) | `longanhuan_mtlv7` | [实时语音合成](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide) |

### :point_right: 预期结果

直接运行 `python run.py` 会用**同一个音色**依次合成 16 种语言的同一句问候语，实时播放并分别保存为 `result_<语种代码>.mp3`，便于横向对比同一音色在各语种下的表现。

也可以只合成单个语种，或换成自己的文本：

```commandline
python3 run.py -l ja                          # 只合成日语（用内置示例文本）
python3 run.py -l fr -t "Bonjour à tous."     # 合成自定义法语文本
python3 run.py -l ko -o ./out/korean.mp3      # 指定输出路径
```

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../docs/image/group.png" width="400"/>
