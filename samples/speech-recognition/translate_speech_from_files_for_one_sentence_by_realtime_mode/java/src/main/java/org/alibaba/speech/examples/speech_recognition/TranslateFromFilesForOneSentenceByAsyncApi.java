/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package org.alibaba.speech.examples.speech_recognition;

import com.alibaba.dashscope.audio.asr.translation.TranslationRecognizerChat;
import com.alibaba.dashscope.audio.asr.translation.TranslationRecognizerParam;
import com.alibaba.dashscope.audio.asr.translation.results.TranslationRecognizerResult;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import java.io.FileInputStream;
import java.nio.ByteBuffer;
import java.nio.file.Path;
import java.nio.file.Paths;
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
public class TranslateFromFilesForOneSentenceByAsyncApi {
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
        TranslationRecognizerObjectPool.TRANSLATION_RECOGNIZER_OBJECTPOOL_SIZE_ENV,
        TranslationRecognizerObjectPool.DEFAULT_OBJECT_POOL_SIZE);

    int threadNums = 2;
    String currentDir = System.getProperty("user.dir");
    // Please replace the path with your audio source
    Path[] filePaths = {
      Paths.get("../../../sample-data/asr_example_chat.wav"),
      //                Paths.get("../../../sample-data/asr_example_chat.wav"),
      //                Paths.get("../../../sample-data/asr_example_chat.wav"),
    };
    // Use ThreadPool to run recognition and translation tasks
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

class TranslationRecognizerObjectFactory
    extends BasePooledObjectFactory<TranslationRecognizerChat> {
  public TranslationRecognizerObjectFactory() {
    super();
  }

  @Override
  public TranslationRecognizerChat create() {
    return new TranslationRecognizerChat();
  }

  @Override
  public PooledObject<TranslationRecognizerChat> wrap(TranslationRecognizerChat obj) {
    return new DefaultPooledObject<>(obj);
  }
}

class TranslationRecognizerObjectPool {
  public static GenericObjectPool<TranslationRecognizerChat> translatorGenericObjectPool;
  public static String TRANSLATION_RECOGNIZER_OBJECTPOOL_SIZE_ENV =
      "TRANSLATION_RECOGNIZER_OBJECTPOOL_SIZE";
  public static int DEFAULT_OBJECT_POOL_SIZE = 500;
  private static Lock lock = new java.util.concurrent.locks.ReentrantLock();

  public static int getObjectivePoolSize() {
    try {
      Integer n = Integer.parseInt(System.getenv(TRANSLATION_RECOGNIZER_OBJECTPOOL_SIZE_ENV));
      return n;
    } catch (NumberFormatException e) {
      return DEFAULT_OBJECT_POOL_SIZE;
    }
  }

  public static GenericObjectPool<TranslationRecognizerChat> getInstance() {
    lock.lock();
    if (translatorGenericObjectPool == null) {
      // You can set the object pool size here. or in environment variable
      // TRANSLATOR_OBJECTPOOL_SIZE It is recommended to set it to 1.5 to 2
      // times your server's maximum concurrent connections.
      int objectPoolSize = getObjectivePoolSize();
      System.out.println("TRANSLATOR_OBJECTPOOL_SIZE: " + objectPoolSize);
      TranslationRecognizerObjectFactory translatorObjectFactory =
          new TranslationRecognizerObjectFactory();
      GenericObjectPoolConfig<TranslationRecognizerChat> config = new GenericObjectPoolConfig<>();
      config.setMaxTotal(objectPoolSize);
      config.setMaxIdle(objectPoolSize);
      config.setMinIdle(objectPoolSize);
      translatorGenericObjectPool = new GenericObjectPool<>(translatorObjectFactory, config);
    }
    lock.unlock();
    return translatorGenericObjectPool;
  }
}

class RealtimeRecognizeTask implements Runnable {
  public static String target_language = "en";
  private static final Object lock = new Object();
  private Path[] filePaths;

  public RealtimeRecognizeTask(Path[] filePaths) {
    this.filePaths = filePaths;
  }

  public void runCallback() throws NoApiKeyException {
    for (Path filePath : filePaths) {
      // Create TranslationRecognizerParam
      // you can customize the TranslationRecognizer parameters, like model, format,
      // sample_rate for more information, please refer to
      // https://help.aliyun.com/document_detail/2712536.html
      TranslationRecognizerParam param = null;
      param =
          TranslationRecognizerParam.builder()
              .model("gummy-chat-v1")
              .format("pcm") // 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you
              // can check the supported formats in the document
              .sampleRate(16000) // supported 8000、16000
              .apiKey(getDashScopeApiKey()) // set your apikey in config.Environments.yourApikey
              .transcriptionEnabled(true)
              .translationEnabled(true)
              .translationLanguages(new String[] {target_language})
              .build();

      TranslationRecognizerChat translator = null;

      try {
        //                translator = TranslationRecognizerObjectPool.getInstance().borrowObject();
        translator = new TranslationRecognizerChat();
        CountDownLatch latch = new CountDownLatch(1);

        String threadName = Thread.currentThread().getName();

        ResultCallback<TranslationRecognizerResult> callback =
            new ResultCallback<TranslationRecognizerResult>() {
              @Override
              public void onEvent(TranslationRecognizerResult result) {
                synchronized (lock) {
                  if (result.getTranscriptionResult() != null) {
                    if (result.isSentenceEnd()) {
                      System.out.printf(
                          "\t[process "
                              + threadName
                              + "] Transcript Fix:"
                              + result.getTranscriptionResult().getText());
                      System.out.printf(
                          "\t[Stash]: " + result.getTranscriptionResult().getStash() + "\n");
                    } else {
                      System.out.println(
                          "\t[process "
                              + threadName
                              + "] Transcript:"
                              + result.getTranscriptionResult().getText());
                    }
                  }
                  if (result.getTranslationResult() != null) {
                    if (result.isSentenceEnd()) {
                      System.out.printf(
                          "\t[process "
                              + threadName
                              + "] Translate "
                              + target_language
                              + " Fix:"
                              + result
                                  .getTranslationResult()
                                  .getTranslation(target_language)
                                  .getText());
                      System.out.print(
                          "\t[Stash]: "
                              + result
                                  .getTranslationResult()
                                  .getTranslation(target_language)
                                  .getStash()
                              + "\n");
                    } else {
                      System.out.println(
                          "\t[process "
                              + threadName
                              + "] Translate "
                              + target_language
                              + ":"
                              + result
                                  .getTranslationResult()
                                  .getTranslation(target_language)
                                  .getText());
                    }
                  }
                }
              }

              @Override
              public void onComplete() {
                System.out.println("[" + threadName + "] Translation complete");
                latch.countDown();
              }

              @Override
              public void onError(Exception e) {
                System.out.println(
                    "[" + threadName + "] RecognitionCallback error: " + e.getMessage());
              }
            };
        // set param & callback
        translator.call(param, callback);
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
            // Send the ByteBuffer to the translation and recognition instance
            if (!translator.sendAudioFrame(byteBuffer)) {
              break;
            }
            Thread.sleep(100);
            buffer = new byte[3200];
          }
        } catch (Exception e) {
          e.printStackTrace();
          translator.getDuplexApi().close(1000, "bye");
        }

        translator.stop();
        // wait for the translation and recognition to complete
        try {
          latch.await();
        } catch (InterruptedException e) {
          throw new RuntimeException(e);
        }

        System.out.println(
            "["
                + threadName
                + "][Metric] requestId: "
                + translator.getLastRequestId()
                + ", first package delay ms: "
                + translator.getFirstPackageDelay()
                + ", last package delay ms: "
                + translator.getLastPackageDelay());
      } catch (Exception e) {
        e.printStackTrace();
        translator.getDuplexApi().close(1000, "bye");
      } finally {
        if (translator != null) {
          try {
            // Return the translation and recognition object to the pool
            //
            // TranslationRecognizerObjectPool.getInstance().returnObject(translator);
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
