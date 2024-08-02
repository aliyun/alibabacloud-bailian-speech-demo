[comment]: # (title and brief introduction of the sample)
## 语音合成并保存到文件
## Python

[comment]: # (prerequisites)
### :point_right: 前提条件

1. #### 配置阿里云百炼API-KEY

    在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

1. #### 安装Python依赖

    阿里云百炼SDK运行环境需要Python 3.8及以上版本。您可以使用以下命令来安装本示例的依赖：
    ```commandline
    pip3 install -r requirements.txt
    ```
    请参考[文档](https://github.com/kkroening/ffmpeg-python)安装ffmpeg

[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例
您可以使用以下命令运行本示例：

```commandline
python3 run.py
```

示例运行时，将会使用longxiaochun音色合成示例文本 “欢迎体验阿里云百炼大模型语音合成服务！” 保存在 `result.mp3` 文件中，并通过扬声器播放。
您可以通过修改`text_to_synthesize`合成指定的文本。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../../docs/image/groups.png" width="400"/>
