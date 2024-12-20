[comment]: # (title and brief introduction of the sample)
## 批量音视频文件语音识别（实时模式）
批量音视频文件语音识别（实时模式）是指并发的将多个音视频文件通过实时的方式将语音数据发送给语音识别服务，并实时地将语音转换为文字的过程。

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

推荐通过IDE导入maven依赖并运行示例。示例使用了线程池实现并发运行。在示例运行时，程序会并发的读取您输入的多个音视频文件，将其独立的转为实时识别结果并分别以callback的方式回调。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>

    