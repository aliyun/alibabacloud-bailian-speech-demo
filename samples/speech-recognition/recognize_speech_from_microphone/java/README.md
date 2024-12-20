[comment]: # (title and brief introduction of the sample)
## 麦克风实时语音识别
## Java

[comment]: # (prerequisites)
### :point_right: 前提条件

1. #### 配置阿里云百炼API-KEY

    在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### 使用 Maven

    在你的 `pom.xml` 文件中添加以下依赖项：
    
    ```xml
    <!-- https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java -->
    <dependency>
        <groupId>com.alibaba</groupId>
        <artifactId>dashscope-sdk-java</artifactId>
        <version>the-latest-version</version>
    </dependency>
    ```
3. #### 使用 Gradle

    在你的项目的 build.gradle 文件中添加以下依赖项：
    
    ```gradle
    // https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
    implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'
    ```


[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例

推荐通过IDE导入maven依赖并运行RecordAndRecognizeToText.java示例。从麦克风输入进行实时语音识别示例运行后会开启录音，调用streamCall()流式返回识别结果。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>

    