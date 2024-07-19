## 录音文件识别
录音文件识别（Audio File Recognition）也称为文件转写，能够对常见的音频或者视频文件进行语音识别，并通过同步或者异步的方式将结果返回给用户。
相对于实时语音识别，录音文件识别提供了更多语音格式、以及信息更丰富的结果供用户选择。同时录音文件识可以批量提交任务，相对于实时语音识别更适合批量的任务处理。
录音文件识别适用于对识别时效性要求不高的场景，如电话录音质检、会议和销售语音分析等。


## 前提条件
本目录下提供了通过读取提交录音文件链接进行语音识别的示例。在运行代码之前请确保您已安装依赖并配置好必要的环境变量。

#### 使用 Maven

在你的 `pom.xml` 文件中添加以下依赖项：

```xml
<!-- https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java -->
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>dashscope-sdk-java</artifactId>
    <version>the-latest-version</version>
</dependency>
```
#### 使用 Gradle

在你的项目的 build.gradle 文件中添加以下依赖项：

```gradle
// https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'
```


### 配置阿里云百炼API-KEY
在使用百炼SDK进行语音识别之前，您需要先在阿里云控制台创建语音识别服务并获取API-KEY。
- 在[百炼控制台](https://bailian.console.aliyun.com/)界面右上角头像位置，鼠标悬浮后，展示API-KEY，点击后进入API-KEY管理页面。
- 点击【创建新的API-KEY】，会自动创建一条属于这个账号的API-KEY。列表上展示API-KEY密文，点击【查看】可以看到API-KEY的明文信息。请注意保存API-KEY的明文信息，后续使用API-KEY时需要用到。
- 更多百炼配置信息请参考：[PREREQUISITES.md](../../../../../PREREQUISITES.md)