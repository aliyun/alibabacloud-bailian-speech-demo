# CosyVoice语音合成常见问题汇总 (FAQ)

## 目录
- [CosyVoice语音合成常见问题汇总 (FAQ)](#cosyvoice语音合成常见问题汇总-faq)
  - [目录](#目录)
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
    - [保存的音频无法播放](#保存的音频无法播放)
    - [实时播放音频流只有第一包可以播放/都无法播放](#实时播放音频流只有第一包可以播放都无法播放)
    - [播放音频卡顿](#播放音频卡顿)
    - [合成的音频没有读完所有文本](#合成的音频没有读完所有文本)
    - [调用streamingCancel之后播放器没有立刻停止，而是会再播放一小段音频](#调用streamingcancel之后播放器没有立刻停止而是会再播放一小段音频)
  - [常见抛出异常及处理方法](#常见抛出异常及处理方法)
    - [CERTIFICATE\_VERIFY\_FAILED](#certificate_verify_failed)
    - [缺少必要参数](#缺少必要参数)
    - [SDK内部状态错误](#sdk内部状态错误)
    - [text is null](#text-is-null)
    - [speech synthesizer task has stopped](#speech-synthesizer-task-has-stopped)
    - [timeout 10000ms](#timeout-10000ms)
  - [常见task-failed错误](#常见task-failed错误)
    - [request timeout after 23 seconds](#request-timeout-after-23-seconds)
    - [Parameter invalid: text is null](#parameter-invalid-text-is-null)
    - [\[tts:\]Engine return error code: 418](#ttsengine-return-error-code-418)
    - [Requests rate limit exceeded, please try again later.](#requests-rate-limit-exceeded-please-try-again-later)

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
2. 在完成SpeechSynthesizer对象初始化后通过get_last_request_id/getLastRequestId方法获取。

## 常见效果问题

### 保存的音频无法播放
**解答：**
1. 请检查保存文件的后缀是否正确，默认格式为mp3。
2. 请检查是否是在on_data/onEvent回调中打开文件并保存。由于音频是按照音频流从回调中返回，因此此种方法只会保存一个音频chunk，并且在每次写入覆盖文件。正确的保存方法为在callback外部打开文件，在回调用追加写入。参考示例代码[Java示例](https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/samples/speech-synthesizer/save-to-file/java/SaveSynthesizedAudioToFileByStreamingInStreamingOut.java)和[Python示例](https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/samples/speech-synthesizer/save-to-file/python/save_synthesized_audio_to_file_by_streaming_in_streaming_out.py)

### 实时播放音频流只有第一包可以播放/都无法播放
**解答：**
1. 检查SDK设置的音频格式、采样率和播放器是否一致。
2. 如果保存的音频可以正常播放，则请检查是否将每个音频包都当做完整的音频文件播放。在流式播放中，是将一个完整的wav文件的音频按照8000字节一段分割为多个chunk返回。而在播放流式音频时，需要使用支持流式播放的音频播放器，比如pyaudio、ffmpeg、audio标签、AudioContext等，而不是将每一个chunk当作一个独立的音频播放，这样无法成功解码。

### 播放音频卡顿
**解答：**
1. 首先请参考[Java示例](https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/samples/speech-synthesizer/save-to-file/java/SaveSynthesizedAudioToFileByStreamingInStreamingOut.java)和[Python示例](https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/samples/speech-synthesizer/save-to-file/python/save_synthesized_audio_to_file_by_streaming_in_streaming_out.py)保存收到的音频，排查是播放器卡顿还是下发音频卡顿。如果保存音频卡顿，则请请将RequestId/TaskId提供给我们排查。
2. 请检查是否发送文本过慢，已发送文本已经读完。
3. 请检查回调函数中（特别是on_data/onEvent）是否有过多业务代码阻塞。由于回调在websocket线程中，因此回阻塞websocket接收网络包，导致接收音频卡住。可以自己写一个audio buffer，在回调用将音频写入buffer，在其他线程中读取并处理。
4. 请检查网络是否不稳定。
5. 如果非上述原因造成，请将RequestId/TaskId提供给我们排查。

### 合成的音频没有读完所有文本
**解答：**
请检查是否调用了streamingComplete方法，否则服务端存在未合成的文本缓存。

### 调用streamingCancel之后播放器没有立刻停止，而是会再播放一小段音频
**解答：**
请检查本地播放器是否存在缓存音频需要清空。


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

### 缺少必要参数
Java报错：
1. `Parameter invalid: StreamInputTtsParam is null`
2. `Parameter invalid: ResultCallback is null`

Python报错：
1. `Model is required!`
2. `format is required!`
3. `callback is required!`

**解答：**
缺少对应必填字段，请参照API详情文档填写。

### SDK内部状态错误
Python报错：`speech synthesizer has not been started.`
Java报错：`State invalid: expect stream input tts state is started but idle`

**解答：**
1. 如果是在调用streamingComplete/streamingCancel时出现，请检查是否之前调用过streamingCall开始任务。
2. 请检查是否在调用streamingComplete之后再次调用streamingCall。在Python SDK中，同一个synthesizer对象不可复用。在Java SDK中，复用SDK对象前请使用updateParamAndCallback函数。
3. 请检查回调函数中是否有task-failed出现，如果是使用call接口可以开启日志查看收到的消息。如果收到task-failed则根据错误提示进一步排查。
4. 检查on_close是否被调用，出现网络中断导致webscoket连接中断。

### text is null

发送文本不可为空。

### speech synthesizer task has stopped

**解答：**
请检查是否在调用streamingComplete之后再次调用streamingCall。同一个synthesizer对象不可复用。

### timeout 10000ms
Python报错：`speech synthesizer wait for complete timeout 10000ms`

**解答：**
请将requestId/taskId发送给我们排查。


## 常见task-failed错误

### request timeout after 23 seconds

**解答：**
超过23秒没有发送文本并且没有音频下发，则服务会中断websocket连接。服务不会无限保持连接，请在适当时候调用streamingComplete结束连接。

### Parameter invalid: text is null

**解答：**
发送文本不可为空。

### [tts:]Engine return error code: 418
1、请检查当前音色不支持。请确认是否音色在[音色列表](https://help.aliyun.com/zh/model-studio/developer-reference/model-list-1?spm=a2c4g.11186623.0.0.6bf214f5dJIxyY)中。
2、其他情况请将requestId/taskId发送给我们排查。

### Requests rate limit exceeded, please try again later.
**解答：**
调用超过并发限制。不同模型的并发限制请参考[限流](https://help.aliyun.com/zh/model-studio/developer-reference/rate-limit)。