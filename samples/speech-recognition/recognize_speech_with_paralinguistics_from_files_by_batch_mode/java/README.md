[comment]: # (title and brief introduction of the sample)
## 批量音视频文件富文本语音识别（批量模式）
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

推荐通过IDE导入maven依赖并运行示例。录音文件识别服务将会将提交的文件列表进行后台转写。转写成功后，每个文件的识别结果，将会存储在一个远程JSON文件中，您可以工作URL在浏览器中查看或者下载文件进行后续处理。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../../docs/image/groups.png" width="400"/>

    