[comment]: # (title and brief introduction of the sample)
## Qwen-Audio-3.0-TTS All-in-One 多语言语音合成

简体中文 | [English](./README_EN.md)

## Java

[comment]: # (prerequisites)
### :point_right: 前提条件

1. #### 配置阿里云百炼API-KEY

    在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例

```commandline
mvn clean package
java -jar target/alibabacloud-bailian-speech-demo-java-1.0-SNAPSHOT.jar
```

示例会用**同一个音色** `longanhuan_mtlv7` 依次合成 16 种语言的同一句问候语，实时播放并分别保存为 `result_<语种代码>.mp3`。

功能与 [Python 版本](../python) 完全一致。完整的 16 种语言列表、`languageHints` + `instruction` 用法与回环验证结果见[上层说明](../README.md)。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../../docs/image/group.png" width="400"/>
