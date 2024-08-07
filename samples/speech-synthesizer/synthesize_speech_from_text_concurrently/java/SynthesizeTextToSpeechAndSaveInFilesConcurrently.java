/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package com.alibaba.dashscope;

import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.protocol.ConnectionConfigurations;
import com.alibaba.dashscope.utils.ApiKey;
import com.alibaba.dashscope.utils.Constants;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.time.Duration;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicLong;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.pool2.BasePooledObjectFactory;
import org.apache.commons.pool2.PooledObject;
import org.apache.commons.pool2.impl.DefaultPooledObject;
import org.apache.commons.pool2.impl.GenericObjectPool;
import org.apache.commons.pool2.impl.GenericObjectPoolConfig;

// Factory class for creating and managing SpeechSynthesizer objects
class SpeechSynthesizerObjectFactory
        extends BasePooledObjectFactory<SpeechSynthesizer> {
    private String dashScopeApiKey;
    public SpeechSynthesizerObjectFactory() throws NoApiKeyException {
        super();
        // Set your DashScope API key. More information: https://help.aliyun.com/document_detail/2712195.html
        // in fact,if you have set DASHSCOPE_API_KEY in your environment variable,
        // you can ignore this, and the sdk will automatically get the api_key from the environment variable
        try {
            ApiKey apiKey = new ApiKey();
            this.dashScopeApiKey = apiKey.getApiKey(null); // from environment variable.
        } catch (NoApiKeyException e) {
            System.out.println("No api key found in environment.");
        }
        if (this.dashScopeApiKey == null) {
            //if you can not set api_key in your environment variable,
            //you can set it here by code
            this.dashScopeApiKey = "your-dashscope-api-key";
        }
    }
    @Override
    public SpeechSynthesizer create() throws Exception {

        // Build parameters for speech synthesis
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        .model("cosyvoice-v1")
                        .voice("longxiaochun")
                        .apiKey(this.dashScopeApiKey)
                        .build();
        return new SpeechSynthesizer(param, null);
    }

    @Override
    public PooledObject<SpeechSynthesizer> wrap(SpeechSynthesizer obj) {
        return new DefaultPooledObject<>(obj);
    }
}

@Slf4j
public class SynthesizeTextToSpeechAndSaveInFilesConcurrently {
    public static void main(String[] args) throws InterruptedException, NoApiKeyException {
        // Record task start time
        LocalDateTime task_start_time = LocalDateTime.now();
        int peakThreadNum = 2;
        int runTimes = 2;
        DateTimeFormatter formatter =
                DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss:SSS");

        // Configure connection parameters
        Constants.connectionConfigurations =
                ConnectionConfigurations.builder()
                        .connectTimeout(Duration.ofSeconds(120))
                        .readTimeout(Duration.ofSeconds(300))
                        .writeTimeout(Duration.ofSeconds(60))
                        .connectionIdleTimeout(Duration.ofSeconds(300))
                        .connectionPoolSize(peakThreadNum)
                        .maximumAsyncRequests(peakThreadNum)
                        .maximumAsyncRequestsPerHost(peakThreadNum)
                        .proxyPort(443)
                        .proxyAuthenticator(null)
                        .build();

        // Create the factory and pool configuration
        SpeechSynthesizerObjectFactory speechSynthesizerObjectFactory =
                new SpeechSynthesizerObjectFactory();
        GenericObjectPoolConfig<SpeechSynthesizer> config =
                new GenericObjectPoolConfig<>();
        config.setMaxTotal(peakThreadNum);
        config.setMinIdle(peakThreadNum);
        config.setMinIdle(peakThreadNum);
        GenericObjectPool<SpeechSynthesizer> synthesizerPool =
                new GenericObjectPool<>(speechSynthesizerObjectFactory, config);

        // Create the pool of SpeechSynthesis objects
        ExecutorService executorService =
                Executors.newFixedThreadPool(peakThreadNum);

        // Track avaerage time cost
        AtomicLong averageTimeCost = new AtomicLong(0);
        AtomicLong totalWaitTime = new AtomicLong(0);

        for (int i = 0; i < runTimes; i++) {
            // Record the task submission time
            LocalDateTime submissionTime = LocalDateTime.now();
            executorService.submit(new QueuedTask(i, submissionTime, synthesizerPool,
                    averageTimeCost, totalWaitTime, formatter, false));
        }

        // Shut down the ExecutorService and wait for all tasks to complete
        executorService.shutdown();
        executorService.awaitTermination(1, TimeUnit.MINUTES);

        // Record the end time of the task
        LocalDateTime task_end_time = LocalDateTime.now();
        synthesizerPool.close();

        System.out.printf("Total number of tasks %d, thread pool size %d\n\n",
                runTimes, peakThreadNum);
        System.out.printf("Average time cost %d milliseconds\n",
                averageTimeCost.get() / runTimes);
        System.out.printf(
                "Average wait time %d milliseconds\n", totalWaitTime.get() / runTimes);
        System.out.printf("Total execution time %d milliseconds\n",
                (int) Duration.between(task_start_time, task_end_time).toMillis());
        System.exit(0);
    }
}

class QueuedTask implements Runnable {
    private final int taskId;
    private final LocalDateTime submissionTime;
    private final GenericObjectPool<SpeechSynthesizer> synthesizerPool;
    private final AtomicLong averageTimeCost;
    private final AtomicLong totalWaitTime;
    private final DateTimeFormatter formatter;
    private boolean saveAudio2File = false;

    public QueuedTask(int taskId, LocalDateTime submissionTime,
                      GenericObjectPool<SpeechSynthesizer> synthesizerPool,
                      AtomicLong averageTimeCost, AtomicLong totalWaitTime,
                      DateTimeFormatter formatter, boolean saveAudio2File) {
        this.taskId = taskId;
        this.submissionTime = submissionTime;
        this.synthesizerPool = synthesizerPool;
        this.averageTimeCost = averageTimeCost;
        this.totalWaitTime = totalWaitTime;
        this.formatter = formatter;
        this.saveAudio2File = saveAudio2File;
    }

    @Override
    public void run() {

        SpeechSynthesizer synthesizer = null;
        try {
            LocalDateTime createTime = LocalDateTime.now();
            String formattedCreat = createTime.format(formatter);

            // Borrow a SpeechSynthesizer object from object pool
            synthesizer = synthesizerPool.borrowObject();

            LocalDateTime startTime = LocalDateTime.now();
            // Record the start time of the task
            String formattedSubmit = submissionTime.format(formatter);
            long waitTime = Duration.between(submissionTime, createTime).toMillis();
            totalWaitTime.addAndGet(waitTime);
            String formattedStart = startTime.format(formatter);
            // Start the synthesizer
            ByteBuffer audio = synthesizer.call("欢迎体验阿里云百炼大模型语音合成服务！");

            LocalDateTime endTime = LocalDateTime.now();
            String formattedEnd = endTime.format(formatter);
            String requestId = synthesizer.getLastRequestId();

            long createTimeCost = Duration.between(createTime, startTime).toMillis();

            long synthesisTimeCost = Duration.between(startTime, endTime).toMillis();
            averageTimeCost.addAndGet(waitTime + createTimeCost + synthesisTimeCost);
            long allSynthesisTimeCost =
                    Duration.between(submissionTime, endTime).toMillis();

            System.out.println("[TTS] [thread " + Thread.currentThread().getId()
                    + "] " + taskId + " [request_id " + requestId + "] submission time: "
                    + formattedSubmit + ", object creation time: " + formattedCreat
                    + ", synthesis start time: " + formattedStart
                    + ", synthesis complete time: " + formattedEnd);
            System.out.println("[TTS] [thread " + Thread.currentThread().getId()
                    + "] " + taskId + " [request_id " + requestId + "] task waiting "
                    + waitTime + " ms, initialization cost " + createTimeCost
                    + " ms, synthesis cost " + synthesisTimeCost + " ms. Total cost "
                    + allSynthesisTimeCost + " ms");
            if (this.saveAudio2File) {
                String file = requestId + ".mp3";
                try (FileOutputStream fos = new FileOutputStream(file)) {
                    fos.write(audio.array());
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (synthesizer != null) {
                try {
                    // Return the SpeechSynthesizer object to the pool
                    synthesizerPool.returnObject(synthesizer);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }
}