[comment]: # (title and brief introduction of the sample)
## Qwen-Audio-3.0-TTS All-in-One 多语言语音合成

简体中文 | [English](./README_EN.md)

## Python

[comment]: # (prerequisites)
### :point_right: 前提条件

1. #### 配置阿里云百炼API-KEY

    在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

1. #### 安装ffmpeg

    示例需要用到ffmpeg进行音视频解码。推荐从官方网站下载安装，并将ffmpeg安装路径配置进环境变量：[ffmpeg官方网站下载](https://www.ffmpeg.org/download.html)。也可以参考文档[如何安装ffmpeg](../../../../docs/QA/ffmpeg.md)。

1. #### 安装Python依赖

    阿里云百炼SDK运行环境需要Python 3.8及以上版本。您可以使用以下命令来安装本示例的依赖：
    ```commandline
    pip3 install -r requirements.txt
    ```

[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例

不带参数运行时，示例会用**同一个音色** `longanhuan_mtlv7` 依次合成 **16 种语言**的同一句问候语，实时播放并分别保存为 `result_<语种代码>.mp3`：

```commandline
python3 run.py
```

终端输出形如：

```
[3/16] 日语 日本語 (ja)
  instruction: 请讲日语。
  text: こんにちは、アリババクラウドの音声合成サービスへようこそ。
  requestId: bb9b333ac4b0416ca538532d0e2b09cd, first_package_delay: 445ms
  saved to: result_ja.mp3
```

请重点留意：**切换语种时说话人的音色始终保持一致**，这正是 All-in-One 多语言音色的价值所在。

也可以只合成单个语种，或换成自己的文本：

```commandline
python3 run.py -l ja                          # 只合成日语（用内置示例文本）
python3 run.py -l fr -t "Bonjour à tous."     # 合成自定义法语文本
python3 run.py -l ko -o ./out/korean.mp3      # 指定输出路径
```

可用的语种代码：`zh` `en` `ja` `ko` `fr` `de` `ru` `it` `es` `pt` `ar` `th` `vi` `id` `ms` `tl`

> :bulb: `-t/--text` 必须与 `-l/--lid` 一起使用，因为模型需要知道这段文本是什么语种。单独传 `-t` 会直接报错退出。

### :point_right: 关键实现说明

语种由 `language_hints` 与 `instruction` 两个参数共同决定，各语种对应的指令维护在 `run.py` 的 `LANGUAGES` 表中：

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

**中文和英文的 `instruction` 为 `None`**（只靠 `language_hints` 即可），其余 14 种语言必须传入对应指令。完整对照表与实测验证结果见[上层说明](../README.md)。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../../docs/image/group.png" width="400"/>
