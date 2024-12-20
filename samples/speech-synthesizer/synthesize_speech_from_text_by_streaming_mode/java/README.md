[comment]: # (title and brief introduction of the sample)
## 语音合成并播放（流式模式）
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
    <!-- 引入jlayer用于解码mp3音频格式 -->
    <dependency>
        <groupId>javazoom</groupId>
        <artifactId>jlayer</artifactId>
        <version>1.0.1</version>
    </dependency>  
    ```
3. #### 使用 Gradle

    在你的项目的 build.gradle 文件中添加以下依赖项：
    
    ```gradle
    // https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
    implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'
    implementation group: 'javazoom', name: 'jlayer', version: '1.0.1'
    ```


[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例

推荐通过IDE导入maven依赖，并导入`SynthesizeSpeechFromeTextByStreamingMode.java`示例代码和`samples/speech_utils/java/RealtimeMp3Player.java`播放器。

运行 `SynthesizeSpeechFromeTextByStreamingMode.java` 示例。使用 loongstella 音色合成示例文本 “想不到时间过得这么快！昨天和你视频聊天，看到你那自豪又满意的笑容，我的心里呀，就如同喝了一瓶蜜一样甜呢！真心为你开心呢！” ，合成音频将按照流式方式下发，通过扬声器播放并保存到文件`result.mp3`中。

您可以通过修改`textToSynthesize`合成指定的文本。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>

    