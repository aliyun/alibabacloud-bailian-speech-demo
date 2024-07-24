## 一句话语音合成 
一句话语音合成是指一次性将一句文本合成语音的调用。
一句话语音合成适合需要实时合成语音，并且一次性合成文本的场景，如导航、语音助手、电话客服等场景。


## 前提条件
本目录提供的是一句话语音合成的示例。示例展示了调用CosyVoice 大模型语音合成音频并进行播放。

在运行代码之前请确保您已安装依赖并配置好必要的环境变量。

[同步调用示例](./SyncSynthesizeTextToSpeech.java)  | [异步调用示例](./AsyncSynthesizeTextToSpeechAndPlay.py)

### 安装 Java 依赖

阿里云百炼SDK运行环境需要Java8及以上版本，SDK版本请参考[Maven](https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java)。

运行本场景DEMO依赖的环境可以通过XML/Gradle安装。

#### 使用 Maven

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
#### 使用 Gradle

在你的项目的 build.gradle 文件中添加以下依赖项：

```gradle
// https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'
implementation group: 'javazoom', name: 'jlayer', version: '1.0.1'
```

### 配置阿里云百炼API-KEY
在使用百炼SDK进行语音识别之前，您需要先在阿里云控制台创建语音识别服务并获取API-KEY。
- 在[百炼控制台](https://bailian.console.aliyun.com/)界面右上角头像位置，鼠标悬浮后，展示API-KEY，点击后进入API-KEY管理页面。
- 点击【创建新的API-KEY】，会自动创建一条属于这个账号的API-KEY。列表上展示API-KEY密文，点击【查看】可以看到API-KEY的明文信息。请注意保存API-KEY的明文信息，后续使用API-KEY时需要用到。
- 更多百炼配置信息请参考：[PREREQUISITES.md](../../../../../PREREQUISITES.md)
