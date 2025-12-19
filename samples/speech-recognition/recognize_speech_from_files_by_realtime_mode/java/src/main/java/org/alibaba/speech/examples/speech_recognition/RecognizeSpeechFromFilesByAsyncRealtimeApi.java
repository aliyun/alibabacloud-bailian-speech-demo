/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package org.alibaba.speech.examples.speech_recognition;

import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionResult;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import java.io.FileInputStream;
import java.nio.ByteBuffer;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;
import org.apache.commons.pool2.BasePooledObjectFactory;
import org.apache.commons.pool2.PooledObject;
import org.apache.commons.pool2.impl.DefaultPooledObject;
import org.apache.commons.pool2.impl.GenericObjectPool;
import org.apache.commons.pool2.impl.GenericObjectPoolConfig;

/**
 * Before making high-concurrency calls to the ASR service, please configure the connection pool
 * size through following environment variables.
 *
 * <p>DASHSCOPE_MAXIMUM_ASYNC_REQUESTS=2000 DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST=2000
 * DASHSCOPE_CONNECTION_POOL_SIZE=2000
 *
 * <p>The default is 32, and it is recommended to set it to 2 times the maximum concurrent
 * connections of a single server.
 */
public class RecognizeSpeechFromFilesByAsyncRealtimeApi {
  public static void checkoutEnv(String envName, int defaultSize) {
    if (System.getenv(envName) != null) {
      System.out.println("[ENV CHECK]: " + envName + " " + System.getenv(envName));
    } else {
      System.out.println("[ENV CHECK]: " + envName + " Using Default which is " + defaultSize);
    }
  }

  public static void main(String[] args) throws NoApiKeyException, InterruptedException {
    // Check for connection pool env
    checkoutEnv("DASHSCOPE_CONNECTION_POOL_SIZE", 32);
    checkoutEnv("DASHSCOPE_MAXIMUM_ASYNC_REQUESTS", 32);
    checkoutEnv("DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST", 32);
    checkoutEnv(
        RecognitionObjectPool.RECOGNITION_OBJECTPOOL_SIZE_ENV,
        RecognitionObjectPool.DEFAULT_OBJECT_POOL_SIZE);

    int threadNums = 2;
    String currentDir = System.getProperty("user.dir");
    // Please replace the path with your audio source
    Path[] filePaths = {
      Paths.get("../../../sample-data/hello_world_male_16k_16bit_mono.wav"),
      //                Paths.get("../../../sample-data/hello_world_male_16k_16bit_mono.wav"),
      //                Paths.get("../../../sample-data/hello_world_male_16k_16bit_mono.wav"),
    };
    // Use ThreadPool to run recognition tasks
    ExecutorService executorService = Executors.newFixedThreadPool(threadNums);
    for (int i = 0; i < threadNums; i++) {
      executorService.submit(new RealtimeRecognizeTask(filePaths));
    }
    executorService.shutdown();
    // wait for all tasks to complete
    executorService.awaitTermination(1, TimeUnit.MINUTES);
    System.exit(0);
  }
}

class RecognitionObjectFactory extends BasePooledObjectFactory<Recognition> {
  public RecognitionObjectFactory() {
    super();
  }

  @Override
  public Recognition create() {
    return new Recognition();
  }

  @Override
  public PooledObject<Recognition> wrap(Recognition obj) {
    return new DefaultPooledObject<>(obj);
  }
}

class RecognitionObjectPool {
  public static GenericObjectPool<Recognition> recognitionGenericObjectPool;
  public static String RECOGNITION_OBJECTPOOL_SIZE_ENV = "RECOGNITION_OBJECTPOOL_SIZE";
  public static int DEFAULT_OBJECT_POOL_SIZE = 500;
  private static Lock lock = new java.util.concurrent.locks.ReentrantLock();

  public static int getObjectivePoolSize() {
    try {
      Integer n = Integer.parseInt(System.getenv(RECOGNITION_OBJECTPOOL_SIZE_ENV));
      return n;
    } catch (NumberFormatException e) {
      return DEFAULT_OBJECT_POOL_SIZE;
    }
  }

  public static GenericObjectPool<Recognition> getInstance() {
    lock.lock();
    if (recognitionGenericObjectPool == null) {
      // You can set the object pool size here. or in environment variable
      // RECOGNITION_OBJECTPOOL_SIZE It is recommended to set it to 1.5 to 2
      // times your server's maximum concurrent connections.
      int objectPoolSize = getObjectivePoolSize();
      System.out.println("RECOGNITION_OBJECTPOOL_SIZE: " + objectPoolSize);
      RecognitionObjectFactory recognitionObjectFactory = new RecognitionObjectFactory();
      GenericObjectPoolConfig<Recognition> config = new GenericObjectPoolConfig<>();
      config.setMaxTotal(objectPoolSize);
      config.setMaxIdle(objectPoolSize);
      config.setMinIdle(objectPoolSize);
      recognitionGenericObjectPool = new GenericObjectPool<>(recognitionObjectFactory, config);
    }
    lock.unlock();
    return recognitionGenericObjectPool;
  }
}

class RealtimeRecognizeTask implements Runnable {
  private static final Object lock = new Object();
  private Path[] filePaths;

  public RealtimeRecognizeTask(Path[] filePaths) {
    this.filePaths = filePaths;
  }

  public void runCallback() throws NoApiKeyException {
    for (Path filePath : filePaths) {
      // Create recognition params
      // you can customize the recognition parameters, like model, format,
      // sample_rate for more information, please refer to
      // https://help.aliyun.com/document_detail/2712536.html
      RecognitionParam param = null;
      param =
          RecognitionParam.builder()
              .model("fun-asr-realtime")
              .format("pcm") // 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you
              // can check the supported formats in the document
              .sampleRate(16000) // supported 8000、16000
              .apiKey(getDashScopeApiKey()) // set your apikey in config.Environments.yourApikey
              // api key.
              .build();
      //            System.out.println("ApiKey" + yourApikey);
      Recognition recognizer = null;

      try {
        recognizer = RecognitionObjectPool.getInstance().borrowObject();
        CountDownLatch latch = new CountDownLatch(1);

        String threadName = Thread.currentThread().getName();

        ResultCallback<RecognitionResult> callback =
            new ResultCallback<RecognitionResult>() {
              @Override
              public void onEvent(RecognitionResult message) {
                synchronized (lock) {
                  if (message.isSentenceEnd()) {
                    System.out.println(
                        "[process " + threadName + "] Fix:" + message.getSentence().getText());
                  } else {
                    System.out.println(
                        "[process " + threadName + "] Result: " + message.getSentence().getText());
                  }
                }
              }

              @Override
              public void onComplete() {
                System.out.println("[" + threadName + "] Recognition complete");
                latch.countDown();
              }

              @Override
              public void onError(Exception e) {
                System.out.println(
                    "[" + threadName + "] RecognitionCallback error: " + e.getMessage());
              }
            };
        // set param & callback
        recognizer.call(param, callback);
        // Please replace the path with your audio file path
        System.out.println("[" + threadName + "] Input file_path is: " + filePath);
        // Read file and send audio by chunks
        try (FileInputStream fis = new FileInputStream(filePath.toFile())) {
          // chunk size set to 100 ms for 16KHz sample rate
          byte[] buffer = new byte[3200];
          int bytesRead;
          // Loop to read chunks of the file
          while ((bytesRead = fis.read(buffer)) != -1) {
            ByteBuffer byteBuffer;
            if (bytesRead < buffer.length) {
              byteBuffer = ByteBuffer.wrap(buffer, 0, bytesRead);
            } else {
              byteBuffer = ByteBuffer.wrap(buffer);
            }
            // Send the ByteBuffer to the recognition instance
            recognizer.sendAudioFrame(byteBuffer);
            Thread.sleep(100);
            buffer = new byte[3200];
          }
          System.out.println(LocalDateTime.now());
        } catch (Exception e) {
          e.printStackTrace();
          recognizer.getDuplexApi().close(1000, "bye");
        }

        recognizer.stop();
        // wait for the recognition to complete
        try {
          latch.await();
        } catch (InterruptedException e) {
          throw new RuntimeException(e);
        }

        System.out.println(
            "["
                + threadName
                + "][Metric] requestId: "
                + recognizer.getLastRequestId()
                + ", first package delay ms: "
                + recognizer.getFirstPackageDelay()
                + ", last package delay ms: "
                + recognizer.getLastPackageDelay());
      } catch (Exception e) {
        e.printStackTrace();
        recognizer.getDuplexApi().close(1000, "bye");
      } finally {
        if (recognizer != null) {
          try {
            // Return the recognition object to the pool
            RecognitionObjectPool.getInstance().returnObject(recognizer);
          } catch (Exception e) {
            e.printStackTrace();
          }
        }
      }
    }
  }

  @Override
  public void run() {
    try {
      runCallback();
    } catch (NoApiKeyException e) {
      throw new RuntimeException(e);
    }
  }

  /**
   * Set your DashScope API key. More information: <a
   * href="https://help.aliyun.com/document_detail/2712195.html">...</a> In fact, if you have set
   * DASHSCOPE_API_KEY in your environment variable, you can ignore this, and the SDK will
   * automatically get the api_key from the environment variable
   */
  private static String getDashScopeApiKey() throws NoApiKeyException {
    String dashScopeApiKey = null;
    try {
      ApiKey apiKey = new ApiKey();
      dashScopeApiKey = apiKey.getApiKey(null); // Retrieve from environment variable.
    } catch (NoApiKeyException e) {
      System.out.println("No API key found in environment.");
    }
    if (dashScopeApiKey == null) {
      // If you cannot set api_key in your environment variable,
      // you can set it here by code
      dashScopeApiKey = "your-dashscope-api-key";
    }
    return dashScopeApiKey;
  }
}
