# Paraformer-Realtime Speech Recognition FAQ

English | [简体中文](./paraformer.md)

- [Paraformer-Realtime Speech Recognition FAQ](#paraformer-realtime-speech-recognition-faq)
  - [Applicable Models](#applicable-models)
  - [Required Reading](#required-reading)
  - [How to configure ApiKey via temporary environment variables](#how-to-configure-apikey-via-temporary-environment-variables)
    - [Windows System](#windows-system)
- [Verify the setting](#verify-the-setting)
    - [Linux \& MacOS Systems](#linux--macos-systems)
- [Verify the setting](#verify-the-setting-1)
  - [How to enable logging](#how-to-enable-logging)
    - [Python SDK](#python-sdk)
      - [Windows System](#windows-system-1)
      - [Linux \& MacOS Systems](#linux--macos-systems-1)
    - [Java SDK](#java-sdk)
  - [How to obtain RequestId / TaskId](#how-to-obtain-requestid--taskid)
  - [Common Effect Issues](#common-effect-issues)
    - [No speech recognition errors, no recognition results.](#no-speech-recognition-errors-no-recognition-results)
    - [Missing or extra characters in recognition results](#missing-or-extra-characters-in-recognition-results)
      - [Streaming call ends with missing characters](#streaming-call-ends-with-missing-characters)
      - [Java SDK shows missing or extra characters in speech recognition](#java-sdk-shows-missing-or-extra-characters-in-speech-recognition)
    - [How to choose sentence segmentation method](#how-to-choose-sentence-segmentation-method)
    - [NullPointerException when using Gummy speech recognition + translation](#nullpointerexception-when-using-gummy-speech-recognition--translation)
  - [Common Exceptions and Solutions](#common-exceptions-and-solutions)
    - [CERTIFICATE\_VERIFY\_FAILED](#certificate_verify_failed)
- [Command 1](#command-1)
- [Command 2](#command-2)
    - [SDK internal state error](#sdk-internal-state-error)
    - [text is null](#text-is-null)
    - [Speech recognition has started.](#speech-recognition-has-started)
    - [Speech recognition has been called.](#speech-recognition-has-been-called)
    - [Speech recognition has stopped.](#speech-recognition-has-stopped)
    - [State invalid: expect recognition state is started but xxx](#state-invalid-expect-recognition-state-is-started-but-xxx)
  - [Common task-failed Errors](#common-task-failed-errors)
    - [Response timeout!](#response-timeout)
    - [Failed to decode audio](#failed-to-decode-audio)
    - [NO\_VALID\_AUDIO\_ERROR](#no_valid_audio_error)
    - [UNSUPPORTED\_FORMAT](#unsupported_format)
    - [Requests rate limit exceeded, please try again later.](#requests-rate-limit-exceeded-please-try-again-later)


## Applicable Models

| Model Name |
| ----- |
| paraformer-realtime-v2|
| paraformer-realtime-8k-v2|
| paraformer-realtime-v1|
| paraformer-realtime-8k-v1|

## Required Reading

Please read the following before starting:

1. Check the documentation for similar issues before contacting us.
2. If `task-failed` contains an error code, first refer to the official error code documentation: [Error Code Documentation](https://help.aliyun.com/zh/model-studio/developer-reference/status-codes).
3. When contacting us, please provide:
   - `RequestId` and `TaskId`
   - Sent text content
   - If possible, provide SDK-side log information

## How to configure ApiKey via temporary environment variables

### Windows System


```
$env:DASHSCOPE_API_KEY="YOUR_API_KEY"
# Verify the setting
echo $env:DASHSCOPE_API_KEY
```

### Linux & MacOS Systems

```
export DASHSCOPE_API_KEY=YOUR_API_KEY
# Verify the setting
echo $DASHSCOPE_API_KEY
```

## How to enable logging

You can enable logging via the following steps:

### Python SDK

Set environment variables in the command line:

#### Windows System

```
$env:DASHSCOPE_LOGGING_LEVEL="debug"
```

#### Linux & MacOS Systems

```
export DASHSCOPE_LOGGING_LEVEL=debug
```

### Java SDK

1. Configure SLF4J dependencies in pom:

```
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
2. Add `logback.xml` in resources directory:

```
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

## How to obtain RequestId / TaskId

1. Parse JSON in callback function to get request_id/task_id
2. After completing Recognition object initialization, use last_request_id/getLastRequestId methods.

## Common Effect Issues

### No speech recognition errors, no recognition results.
**Solution:** 
Check if audio format configuration (format) matches the audio. For example, uploading mp3 but configuring format as pcm.

### Missing or extra characters in recognition results

#### Streaming call ends with missing characters

**Solution:** 
Check if you call stop after sending audio, or send silence during real-time calls.

When audio is received by the service, it's first segmented by VAD and sent to ASR for recognition. If your audio ends without silence and you don't send a stop signal, VAD will continue waiting for audio, and ASR won't receive the cached audio in VAD, leading to missing characters at the end of audio.

Ensure to call stop after speech recognition. If you want to keep the task running after sending audio, promptly send silence audio to maintain the connection.

#### Java SDK shows missing or extra characters in speech recognition
**Solution:** 
Check if your code has similar errors when sending audio:
```
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
1. The parameter type of sendAudioFrame function is ByteBuffer. In the above example, it can be created as a reference to a byte[] array, allowing direct access to byte array data without copying.
2. The SDK uses asynchronous mechanisms to send network packets. After calling sendAudioFrame, the audio in ByteBuffer won't be sent immediately but queued. Updating the byte[] array content at this point will modify the audio data stored in ByteBuffer, causing voice loss, resulting in missing or extra characters in recognition results.
3. Refer to the commented line in the sample code to bind a new byte[] array to each ByteBuffer.

### How to choose sentence segmentation method
**Solution:** 
Paraformer-realtime series models support using VAD or semantics for sentence segmentation, defaulting to VAD.

When VAD segmentation is enabled, is_sentence_end is set to true if the following condition is met:
1. Silence longer than the threshold appears after speech.

When semantic segmentation is enabled, is_sentence_end is set to true only if one of the following conditions is met:
1. A complete sentence is recognized semantically.
2. Silence longer than two seconds appears after speech.

VAD segmentation offers faster response speed, while semantic segmentation provides better results. You can switch between segmentation methods using semantic_punctuation_enabled based on your needs.

### NullPointerException when using Gummy speech recognition + translation
**Solution:** 
In Gummy large model service, speech translation and speech recognition are parallel tasks. Real-time results may not have both speech recognition and translation results simultaneously.

Ensure the result is not null before parsing recognition or translation results in callbacks.

## Common Exceptions and Solutions

### CERTIFICATE_VERIFY_FAILED
Python SDK error:
```
websocket closed due to [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)
```
**Solution:** 
Certificate verification failed during websocket connection. Typically Python environment configuration error.
```
# Command 1
security find-certificate -a -p > ~/all_mac_certs.pem; export SSL_CERT_FILE=~/all_mac_certs.pem; export REQUESTS_CA_BUNDLE=~/all_mac_certs.pem
# Command 2
ln -s /etc/ssl/* /Library/Frameworks/Python.framework/Versions/3.9/etc/openssl
```
Execute the above commands manually to locate certificates. For the second command, select the corresponding Python version directory in your local environment.

Restart terminal after executing the above scripts, clear cache, and retry.

### SDK internal state error
Python error: `speech synthesizer has not been started.`
Java error: `State invalid: expect stream input tts state is started but idle`

**Solution:** 
1. If encountered during streamingComplete/streamingCancel call, check if streamingCall was previously called.
2. Check if streamingCall is called after streamingComplete. Synthesizer objects are not reusable.
3. Check if task-failed appears in callbacks. Enable logs to view received messages if using call interface. Investigate based on error messages if task-failed occurs.
4. Check if on_close is called (network interruption caused websocket disconnection).

### text is null

Sent text cannot be empty.

### Speech recognition has started.

**Solution:** 
Check if start function is called repeatedly. In Python SDK, Recognition objects are not reusable.

### Speech recognition has been called.
**Solution:** 
Check if call function is called repeatedly. In Python SDK, Recognition objects are not reusable.

### Speech recognition has stopped.
**Solution:** 
Check if other interfaces are called after stop function. In Python SDK, Recognition objects are not reusable. Stop function execution means task completion, this object cannot be reused.

### State invalid: expect recognition state is started but xxx
**Solution:** 
1. When encountering State invalid error in Java SDK, check if task_failed message is received in callbacks.
2. Check if multiple `call(RecognitionParam param, ResultCallback<RecognitionResult> callback)` interfaces are called consecutively.
3. Check if other API interfaces are called without re-calling call to start next task after stop.

## Common task-failed Errors

### Response timeout!

**Solution:** 
Websocket connection is terminated after one minute without receiving valid audio. Connection isn't maintained indefinitely. Call stop appropriately to end connection.

### Failed to decode audio

**Solution:** 
Audio format doesn't match configuration.

### NO_VALID_AUDIO_ERROR

**Solution:** 
1. No audio was sent.
2. Audio format doesn't match configuration. For example, uploading pcm audio but configuring as wav. Or uploading unsupported audio formats.

### UNSUPPORTED_FORMAT
**Solution:** 
Unsupported audio format uploaded.

### Requests rate limit exceeded, please try again later.
**Solution:** 
Call exceeds concurrency limit. Refer to [Rate Limit](https://help.aliyun.com/zh/model-studio/developer-reference/rate-limit) for different model limits.
