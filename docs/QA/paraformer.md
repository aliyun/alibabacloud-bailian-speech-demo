# Paraformer-Realtime语音识别常见问题汇总 (FAQ)

简体中文 | [English](./paraformer_en.md)

## 目录
- [Paraformer-Realtime语音识别常见问题汇总 (FAQ)](#paraformer-realtime语音识别常见问题汇总-faq)
  - [目录](#目录)
  - [适用模型](#适用模型)
  - [必读](#必读)
  - [如何通过临时环境变量配置ApiKey](#如何通过临时环境变量配置apikey)
    - [Windows 系统](#windows-系统)
    - [Linux \& MacOS 系统](#linux--macos-系统)
  - [如何开启日志](#如何开启日志)
    - [Python SDK](#python-sdk)
      - [Windows 系统](#windows-系统-1)
      - [Linux \& MacOS 系统](#linux--macos-系统-1)
    - [Java SDK](#java-sdk)
  - [如何获取 RequestId / TaskId](#如何获取-requestid--taskid)
  - [常见效果问题](#常见效果问题)
    - [语音识别无报错，无识别结果。](#语音识别无报错无识别结果)
    - [识别结果丢字、多字](#识别结果丢字多字)
      - [流式调用在音频结尾出现丢字问题](#流式调用在音频结尾出现丢字问题)
      - [Java SDK出现语音识别丢字、多字](#java-sdk出现语音识别丢字多字)
    - [断句方法如何选择](#断句方法如何选择)
    - [调用Gummy语音识别+翻译时遇到空指针](#调用gummy语音识别翻译时遇到空指针)
  - [常见抛出异常及处理方法](#常见抛出异常及处理方法)
    - [CERTIFICATE\_VERIFY\_FAILED](#certificate_verify_failed)
    - [SDK内部状态错误](#sdk内部状态错误)
    - [text is null](#text-is-null)
    - [Speech recognition has started.](#speech-recognition-has-started)
    - [Speech recognition has been called.](#speech-recognition-has-been-called)
    - [Speech recognition has stopped.](#speech-recognition-has-stopped)
    - [State invalid: expect recognition state is started but xxx](#state-invalid-expect-recognition-state-is-started-but-xxx)
  - [常见task-failed错误](#常见task-failed错误)
    - [Response timeout!](#response-timeout)
    - [Failed to decode audio](#failed-to-decode-audio)
    - [NO\_VALID\_AUDIO\_ERROR](#no_valid_audio_error)
    - [UNSUPPORTED\_FORMAT](#unsupported_format)
    - [Requests rate limit exceeded, please try again later.](#requests-rate-limit-exceeded-please-try-again-later)

## 适用模型

| 模型名称 |
| ----- |
| paraformer-realtime-v2|
| paraformer-realtime-8k-v2|
| paraformer-realtime-v1|
| paraformer-realtime-8k-v1|

## 必读

请在开始前务必阅读以下内容：

1. 在联系我们之前，请先在文档中检查是否有相似的问题可以参考。
2. 如果 `task-failed` 时存在错误代码，请先参考官方文档中的错误码说明：[错误码说明](https://help.aliyun.com/zh/model-studio/developer-reference/status-codes)。
3. 联系我们时您最好可以提供以下信息：
   - `RequestId` 和 `TaskId`
   - 发送的文本内容
   - 如有可能，请提供 SDK 侧打印的日志信息

## 如何通过临时环境变量配置ApiKey

### Windows 系统


```bash
$env:DASHSCOPE_API_KEY="YOUR_API_KEY"
# 验证设置生效
echo $env:DASHSCOPE_API_KEY
```

### Linux & MacOS 系统

```bash
export DASHSCOPE_API_KEY=YOUR_API_KEY
# 验证设置生效
echo $DASHSCOPE_API_KEY
```

## 如何开启日志

你可以通过以下步骤开启日志功能：

### Python SDK

在命令行设置环境变量：

#### Windows 系统

```bash
$env:DASHSCOPE_LOGGING_LEVEL="debug"
```

#### Linux & MacOS 系统

```bash
export DASHSCOPE_LOGGING_LEVEL=debug
```

### Java SDK

1. 通过pom配置@Slf4j日志依赖：

```xml
   <!-- Lombok for @Slf4j -->
<dependency>
  <groupId>org.projectlombok</groupId>
  <artifactId>lombok</artifactId>
  <version>1.18.24</version>
  <scope>provided</scope>
</dependency>

<!-- SLF4J API -->
<dependency>
  <groupId>org.slf4j</groupId>
  <artifactId>slf4j-api</artifactId>
  <version>1.7.32</version>
</dependency>

<!-- Logback Implementation -->
<dependency>
  <groupId>ch.qos.logback</groupId>
  <artifactId>logback-classic</artifactId>
  <version>1.2.6</version>
</dependency>
```
2. 在resources目录下添加`logback.xml`：

```xml
<configuration>
<appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
    <encoder>
        <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
    </encoder>
</appender>

<root level="info">
    <appender-ref ref="STDOUT" />
</root>
</configuration>
```

## 如何获取 RequestId / TaskId

1. 解析回调函数中的json获得request_id/task_id
2. 在完成Recognition对象初始化后通过last_request_id/getLastRequestId方法获取。

## 常见效果问题

### 语音识别无报错，无识别结果。
**解答：**
请检查音频格式配置项format是否和音频匹配，例如上传mp3等格式音频但format配置为pcm。

### 识别结果丢字、多字

#### 流式调用在音频结尾出现丢字问题

**解答：**
请检查您是否在发送音频后调用stop方法，或实时调用中发送静音。

当服务收到音频后，首先会通过VAD分句并发送给ASR识别。如果您的语音结尾没有静音，并且没有发送stop信号，VAD会继续等待音频，此时ASR不会收到缓存在VAD中的音频，因此会导致音频结尾丢字。

请确保在调用语音识别后调用stop。如果您希望在发送完音频后不断开任务，请及时补充发送静音音频保持连接。

#### Java SDK出现语音识别丢字、多字
**解答：**
请检查您的代码中发送音频部分是否有类似的错误用法：
```java
byte[] buffer = new byte[3200 * 10];
int bytesRead;
while ((bytesRead = fis.read(buffer)) != -1) {
    ByteBuffer byteBuffer;
    byteBuffer = ByteBuffer.wrap(buffer);
    recognizer.sendAudioFrame(byteBuffer);
    // buffer = new byte[3200 * 10];
    Thread.sleep(100);
}
```
1. sendAudioFrame函数的入参类型为ByteBuffer，在上面示例代码中，可以创建为byte[]数组的引用，此时可以在不复制数据的情况下直接访问byte数组的数据。
2. 在SDK内部采用了异步机制发送网络包，因此在您调用sendAudioFrame函数后，ByteBuffer中的音频不会被立刻发送，而是进入队列中排队。如果此时更新byte[]数组内容，会导致ByteBuffer中存储的音频数据被修改，进而造成语音丢失。这就会导致识别结果有丢字、多字现象。
3. 请参考示例代码中注释行，为每一个ByteBuffer绑定新的byte[]数组。


### 断句方法如何选择
**解答：**
paraformer-realtime系列模型支持使用VAD或语义进行分句，默认使用VAD断句。
当开启VAD断句时，只要满足如下条件就会给出is_sentence_end为true:
1. 语音后出现超过阈值长度的静音。

当开启语义断句时，只有当如下条件满足其一才会给出is_sentence_end为true：
1. 识别出语义完整的一整个句子。
2. 语音后出现超过两秒的静音。

VAD断句具有更快的响应速度，语义断句具有更好的效果。您可以通过semantic_punctuation_enabled根据需要，切换断句方法。

### 调用Gummy语音识别+翻译时遇到空指针
**解答：**
在Gummy大模型服务中，语音翻译和语音识别为并行执行的任务，因此在每一次下发的实时结果中不保证同时具有语音识别结果和语音翻译结果。

因此请在回调中解析识别结果或翻译结果前确保结果不为空。


## 常见抛出异常及处理方法

### CERTIFICATE_VERIFY_FAILED
Python SDK报错：
```
websocket closed due to [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)
```
**解答：**
连接websocket时，本地的openssl验证证书失败，找不到证书。通常是python环境配置错误。
```bash
#命令1
security find-certificate -a -p > ~/all_mac_certs.pem; export SSL_CERT_FILE=~/all_mac_certs.pem; export REQUESTS_CA_BUNDLE=~/all_mac_certs.pem
#命令2
ln -s /etc/ssl/* /Library/Frameworks/Python.framework/Versions/3.9/etc/openssl
```
执行上面这两条命令手动定位证书。第2条命令注意选择您本地环境python版本的对应目录。

请在执行完上述脚本后重新开启终端，清除缓存后重试。

### SDK内部状态错误
Python报错：`speech synthesizer has not been started.`
Java报错：`State invalid: expect stream input tts state is started but idle`

**解答：**
1. 如果是在调用streamingComplete/streamingCancel时出现，请检查是否之前调用过streamingCall开始任务。
2. 请检查是否在调用streamingComplete之后再次调用streamingCall。同一个synthesizer对象不可复用。
3. 请检查回调函数中是否有task-failed出现，如果是使用call接口可以开启日志查看收到的消息。如果收到task-failed则根据错误提示进一步排查。
4. 检查on_close是否被调用，出现网络中断导致webscoket连接中断。

### text is null

发送文本不可为空。

### Speech recognition has started.

**解答：**
请检查是否重复调用了start函数。在Python SDK中，Recognition对象不可复用。

### Speech recognition has been called.
**解答：**
请检查是否重复调用了call函数。在Python SDK中，Recognition对象不可复用。

### Speech recognition has stopped.
**解答：**
请检查是否在调用stop函数之后又调用了其他接口。在Python SDK中，Recognition对象不可复用。stop函数执行后意味着任务完成，此对象不可再使用。

### State invalid: expect recognition state is started but xxx
**解答：**
1. 在使用Java SDK时遇到State invalid报错，请检查是否在回调中收到了task_failed任务失败消息。
2. 是否连续调用多次`call(RecognitionParam param, ResultCallback<RecognitionResult> callback) `接口
3. 是否在stop之后没有重新调用call开启下一个任务就调用其他API接口。


## 常见task-failed错误

### Response timeout!

**解答：**
超过一分钟没有收到有效音频，服务会中断websocket连接。服务不会无限保持连接，请在适当时候调用stop结束连接。

### Failed to decode audio

**解答：**
音频格式和配置不匹配。

### NO_VALID_AUDIO_ERROR

**解答：**
1、没有发送音频。
2、音频格式和配置不匹配。如上传pcm格式音频但配置为wav。或上传了不支持的音频格式。

### UNSUPPORTED_FORMAT
**解答：**
上传了不支持的音频格式。

### Requests rate limit exceeded, please try again later.
**解答：**
调用超过并发限制。不同模型的并发限制请参考[限流](https://help.aliyun.com/zh/model-studio/developer-reference/rate-limit)。
