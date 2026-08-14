[comment]: # (title and brief introduction of the sample)
## Qwen-Audio-3.0-TTS 文本正则化（TN）能力演示

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

示例会依次合成 3 段刻意难读的中文文本，每段通过扬声器实时播放并保存为 `result_tn_1.mp3` ~ `result_tn_3.mp3`，同时在终端打印该段的检查点。

功能与 [Python 版本](../python) 完全一致，请参考[上层说明](../README.md)了解检查点详情。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../../docs/image/group.png" width="400"/>
