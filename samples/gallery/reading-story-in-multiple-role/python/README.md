[comment]: # (title and brief introduction of the sample)
## 分角色朗读故事

简体中文 | [English](./README_EN.md)

分角色朗读故事是通过调用不同音色的语音合成朗读一个完整的故事。适用于多种场景，如有声读物、在线教育等需要区分说话人的场景。
<!--
[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景         | 典型用法   | 使用说明                |
|--------------|--------|---------------------|
 -->


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

[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例


```commandline
python3 run.py
```
运行脚本后将会使用不同音色按照“鸭子妈妈”，“鸭子宝宝”和“旁白”三种不同的角色朗读小鸭子的故事。故事内容存放在story.json中。


[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
