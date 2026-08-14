[comment]: # (title and brief introduction of the sample)
## Qwen-Audio-3.0-TTS 文本正则化（TN）能力演示

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
您可以使用以下命令运行本示例：

```commandline
python3 run.py
```

示例会依次合成 3 段**刻意难读**的中文文本，每段都通过扬声器实时播放，并保存为 `result_tn_1.mp3` ~ `result_tn_3.mp3`。

每段合成前，终端会先打印该段的**检查点清单**，列出书面形式与期望听到的读法，例如：

```
[2] 医药检测：百分号 + 波浪范围符 + 单位
  原文: 在一次检测中，1毫升20%甘露醇药液中可查出粒径4～30微米的微粒598个。
  检查点（应当听到的读法）:
    - 20%        -> 百分之二十 —— 而不是"二十百分号"
    - 4～30微米    -> 四到三十微米 —— 全角波浪号读作"到"，不能读出符号名
```

请边听边对照检查点判断 TN 效果。TN 涉及的多音字声调、数字分组读法无法通过程序自动断言，详见[上层说明](../README.md)。

您可以通过修改 `run.py` 中的 `TN_CASES` 加入自己业务里的难读文本，`checkpoints` 只用于终端提示，不影响合成结果。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../../docs/image/group.png" width="400"/>
