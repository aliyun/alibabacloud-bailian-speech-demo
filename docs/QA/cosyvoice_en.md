# CosyVoice Text-to-Speech FAQ

English | [简体中文](./cosyvoice.md)

- [CosyVoice Text-to-Speech FAQ](#cosyvoice-text-to-speech-faq)
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
  - [How to obtain RequestId/TaskId](#how-to-obtain-requestidtaskid)
  - [Common Effect Issues](#common-effect-issues)
    - [Saved audio cannot play](#saved-audio-cannot-play)
    - [Real-time audio playback only plays first packet/none](#real-time-audio-playback-only-plays-first-packetnone)
    - [Audio playback stutters](#audio-playback-stutters)
    - [Synthesized audio doesn't read all text](#synthesized-audio-doesnt-read-all-text)
    - [After calling streamingCancel, player doesn't stop immediately but plays short audio](#after-calling-streamingcancel-player-doesnt-stop-immediately-but-plays-short-audio)
  - [Common Exceptions and Solutions](#common-exceptions-and-solutions)
    - [CERTIFICATE\_VERIFY\_FAILED](#certificate_verify_failed)
- [Command 1](#command-1)
- [Command 2](#command-2)
    - [Missing required parameters](#missing-required-parameters)
    - [SDK internal state error](#sdk-internal-state-error)
    - [text is null](#text-is-null)
    - [speech synthesizer task has stopped](#speech-synthesizer-task-has-stopped)
    - [timeout 10000ms](#timeout-10000ms)
  - [Common task-failed Errors](#common-task-failed-errors)
    - [request timeout after 23 seconds](#request-timeout-after-23-seconds)
    - [Parameter invalid: text is null](#parameter-invalid-text-is-null)
    - [\[tts:\]Engine return error code: 418](#ttsengine-return-error-code-418)
    - [Requests rate limit exceeded, please try again later.](#requests-rate-limit-exceeded-please-try-again-later)


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

## How to obtain RequestId/TaskId

1. Parse JSON in callback function to get request_id/task_id
2. After initializing SpeechSynthesizer object, use get_last_request_id/getLastRequestId methods.

## Common Effect Issues

### Saved audio cannot play
**Solution:**
1. Check if the file extension is correct (default format is mp3).
2. Verify if saving occurs within on_data/onEvent callbacks. Since audio streams are returned in chunks, opening files inside callbacks will only save a single chunk with each write operation overwriting the file. Correct method: open file outside callback and append in callback. Refer to example code [Java example](../../samples/speech-synthesizer/synthesize_speech_from_text_by_streaming_mode/java/src/main/java/org/alibaba/speech/examples/speech_synthesizer/SynthesizeSpeechFromTextByStreamingMode.java) and [Python example](../../samples/speech-synthesizer/synthesize_speech_from_text_by_streaming_mode/python/run.py)

### Real-time audio playback only plays first packet/none
**Solution:**
1. Check if SDK's audio format/sampling rate matches player.
2. If saved audio plays normally, verify if each audio packet is treated as complete audio. Streaming audio divides complete wav files into 8000-byte chunks. Use streaming-capable players like pyaudio, ffmpeg, audio tags, AudioContext, etc., instead of treating each chunk as independent audio.

### Audio playback stutters
**Solution:**
1. First check [Java example](../../samples/speech-synthesizer/synthesize_speech_from_text_by_streaming_mode/java/src/main/java/org/alibaba/speech/examples/speech_synthesizer/SynthesizeSpeechFromTextByStreamingMode.java) and [Python example](../../samples/speech-synthesizer/synthesize_speech_from_text_by_streaming_mode/python/run.py) to determine if issue is with player or audio delivery. If saved audio stutters, provide RequestId/TaskId for investigation.
2. Check if text input is too slow, causing early completion.
3. Verify if excessive business logic in callbacks (especially on_data/onEvent) blocks execution. Websocket thread may be blocked, causing audio reception delay. Create an audio buffer in callback and process in separate thread.
4. Check network stability.
5. If none of above apply, provide RequestId/TaskId for investigation.

### Synthesized audio doesn't read all text
**Solution:** 
Verify if streamingComplete was called. Server may have cached unsynthesized text.

### After calling streamingCancel, player doesn't stop immediately but plays short audio
**Solution:** 
Check if local player has audio cache needing clearance.

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
Execute above commands to manually locate certificates. Second command requires Python version-specific directory.

Restart terminal after executing above scripts, clear cache, and retry.

### Missing required parameters
Java error:
1. `Parameter invalid: StreamInputTtsParam is null`
2. `Parameter invalid: ResultCallback is null`

Python error:
1. `Model is required!`
2. `format is required!`
3. `callback is required!`

**Solution:** 
Missing mandatory fields. Refer to API documentation.

### SDK internal state error
Python error: `speech synthesizer has not been started.`
Java error: `State invalid: expect stream input tts state is started but idle`

**Solution:** 
1. If during streamingComplete/streamingCancel call, verify if streamingCall was previously called.
2. Check if streamingCall is called after streamingComplete. In Python SDK, synthesizer objects are not reusable. In Java SDK, use updateParamAndCallback before reusing SDK objects.
3. Check if task-failed appears in callbacks. Enable logs to view received messages if using call interface. Investigate based on error messages if task-failed occurs.
4. Check if on_close is called (network interruption caused websocket disconnection).

### text is null

Sent text cannot be empty.

### speech synthesizer task has stopped

**Solution:** 
Verify if streamingCall is called after streamingComplete. Synthesizer objects are not reusable.

### timeout 10000ms
Python error: `speech synthesizer wait for complete timeout 10000ms`

**Solution:** 
Provide requestId/taskId for investigation.

## Common task-failed Errors

### request timeout after 23 seconds

**Solution:** 
Websocket connection is terminated after 23 seconds of no text input and audio output. Connection isn't maintained indefinitely. Call streamingComplete to end connection appropriately.

### Parameter invalid: text is null

**Solution:** 
Sent text cannot be empty.

### [tts:]Engine return error code: 418
1. Check if voice model is unsupported. Confirm if voice is in [Voice List](https://help.aliyun.com/zh/model-studio/developer-reference/model-list-1?spm=a2c4g.11186623.0.0.6bf214f5dJIxyY).
2. For other cases, provide requestId/taskId for investigation.

### Requests rate limit exceeded, please try again later.
**Solution:** 
Call exceeds concurrency limit. Refer to [Rate Limit](https://help.aliyun.com/zh/model-studio/developer-reference/rate-limit) for different model limits.
