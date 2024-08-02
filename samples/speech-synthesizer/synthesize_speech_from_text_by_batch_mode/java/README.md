[comment]: # (title and brief introduction of the sample)
## 批量语音合成并保存
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
    <!-- https://mvnrepository.com/artifact/org.apache.commons/commons-pool2 -->
    <dependency>
        <groupId>org.apache.commons</groupId>
        <artifactId>commons-pool2</artifactId>
        <version>2.11.1</version>
    </dependency>
    ```
3. #### 使用 Gradle

    在你的项目的 build.gradle 文件中添加以下依赖项：
    
    ```gradle
    // https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
    implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'
    implementation group: 'org.apache.commons', name: 'commons-pool2', version: '2.11.1'
    ```


[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例

推荐通过IDE导入maven依赖，并导入`BatchSynthesizeTextToSpeechAndSaveInFiles.java`示例代码。

运行 `BatchSynthesizeTextToSpeechAndSaveInFiles.java` 示例。使用 longxiaochun 音色并发合成 “欢迎体验阿里云百炼大模型语音合成服务！” 并保存在 `<requestId>.mp3` 文件中。

在java并发示例中，使用了连接池、对象池、线程池三种资源池。当对象和连接复用时可以有效降低建立连接的时间开销。

您可以通过修改`task_list`中增加/删除任务合成指定数量的文本。通过`peakThreadNum`参数修改最大进程数。建议不超过机器的cpu核心数。通过`runTimes`参数设定任务执行次数。

:information_source: **注意**：个人账号的appkey当前仅支持 3 并发，如需开通多并发请联系我们。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../../docs/image/groups.png" width="400"/>

    