package org.alibaba.speech.examples.speech_synthesizer;

import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import java.time.LocalDateTime;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.pool2.BasePooledObjectFactory;
import org.apache.commons.pool2.PooledObject;
import org.apache.commons.pool2.impl.DefaultPooledObject;
import org.apache.commons.pool2.impl.GenericObjectPool;
import org.apache.commons.pool2.impl.GenericObjectPoolConfig;

/**
 * 您需要在项目中引入org.apache.commons.pool2和DashScope相关的包。
 *
 * <p>DashScope SDK 2.16.6及后续版本针对高并发场景进行了优化， DashScope SDK 2.16.6之前的版本不推荐在高并发场景下使用。
 *
 * <p>在对TTS服务进行高并发调用之前， 请通过以下环境变量配置连接池的相关参数。
 *
 * <p>DASHSCOPE_MAXIMUM_ASYNC_REQUESTS DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST
 * DASHSCOPE_CONNECTION_POOL_SIZE
 */
class SpeechSynthesizerObjectFactory extends BasePooledObjectFactory<SpeechSynthesizer> {
  public SpeechSynthesizerObjectFactory() {
    super();
  }

  @Override
  public SpeechSynthesizer create() throws Exception {
    return new SpeechSynthesizer();
  }

  @Override
  public PooledObject<SpeechSynthesizer> wrap(SpeechSynthesizer obj) {
    return new DefaultPooledObject<>(obj);
  }
}

class CosyvoiceObjectPool {
  public static GenericObjectPool<SpeechSynthesizer> synthesizerPool;
  public static String COSYVOICE_OBJECTPOOL_SIZE_ENV = "COSYVOICE_OBJECTPOOL_SIZE";
  public static int DEFAULT_OBJECT_POOL_SIZE = 500;
  private static Lock lock = new java.util.concurrent.locks.ReentrantLock();

  public static int getObjectivePoolSize() {
    try {
      Integer n = Integer.parseInt(System.getenv(COSYVOICE_OBJECTPOOL_SIZE_ENV));
      System.out.println("Using Object Pool Size In Env: " + DEFAULT_OBJECT_POOL_SIZE);
      return n;
    } catch (NumberFormatException e) {
      System.out.println("Using Default Object Pool Size: " + DEFAULT_OBJECT_POOL_SIZE);
      return DEFAULT_OBJECT_POOL_SIZE;
    }
  }

  public static GenericObjectPool<SpeechSynthesizer> getInstance() {
    lock.lock();
    if (synthesizerPool == null) {
      // 您可以在这里设置对象池的大小。或在环境变量COSYVOICE_OBJECTPOOL_SIZE中设置。
      // 建议设置为服务器最大并发连接数的1.5到2倍。
      int objectPoolSize = getObjectivePoolSize();
      SpeechSynthesizerObjectFactory speechSynthesizerObjectFactory =
          new SpeechSynthesizerObjectFactory();
      GenericObjectPoolConfig<SpeechSynthesizer> config = new GenericObjectPoolConfig<>();
      config.setMaxTotal(objectPoolSize);
      config.setMaxIdle(objectPoolSize);
      config.setMinIdle(objectPoolSize);
      synthesizerPool = new GenericObjectPool<>(speechSynthesizerObjectFactory, config);
    }
    lock.unlock();
    return synthesizerPool;
  }
}

class SynthesizeTaskWithCallback implements Runnable {
  String[] textArray;
  String requestId;
  long timeCost;

  public SynthesizeTaskWithCallback(String[] textArray) {
    this.textArray = textArray;
  }

  @Override
  public void run() {
    SpeechSynthesizer synthesizer = null;
    long startTime = System.currentTimeMillis();

    try {
      class ReactCallback extends ResultCallback<SpeechSynthesisResult> {
        ReactCallback() {}

        @Override
        public void onEvent(SpeechSynthesisResult message) {
          if (message.getAudioFrame() != null) {
            try {
              byte[] bytesArray = message.getAudioFrame().array();
              System.out.println("收到音频，音频文件流length为：" + bytesArray.length);
            } catch (Exception e) {
              throw new RuntimeException(e);
            }
          }
        }

        @Override
        public void onComplete() {}

        @Override
        public void onError(Exception e) {
          System.out.println(e.getMessage());
          e.printStackTrace();
        }
      }

      SpeechSynthesisParam param =
          SpeechSynthesisParam.builder()
              .model("cosyvoice-v1")
              .voice("longxiaochun")
              .format(SpeechSynthesisAudioFormat.MP3_22050HZ_MONO_256KBPS) // 流式合成使用PCM或者MP3
              .apiKey(getDashScopeApiKey()) // Set your API key
              .build();

      try {
        synthesizer = CosyvoiceObjectPool.getInstance().borrowObject();
        synthesizer.updateParamAndCallback(param, new ReactCallback());
        for (String text : textArray) {
          synthesizer.streamingCall(text);
        }
        Thread.sleep(20);
        synthesizer.streamingComplete(60000);
        requestId = synthesizer.getLastRequestId();
      } catch (Exception e) {
        System.out.println("Exception e: " + e.toString());
        synthesizer.getDuplexApi().close(1000, "bye");
      }
    } catch (Exception e) {
      throw new RuntimeException(e);
    } finally {
      if (synthesizer != null) {
        try {
          // Return the SpeechSynthesizer object to the pool
          CosyvoiceObjectPool.getInstance().returnObject(synthesizer);
        } catch (Exception e) {
          e.printStackTrace();
        }
      }
    }
    long endTime = System.currentTimeMillis();
    timeCost = endTime - startTime;
    System.out.println(
        "[线程 "
            + Thread.currentThread()
            + "] [Metric] requestId: "
            + synthesizer.getLastRequestId()
            + ", first package delay ms: "
            + synthesizer.getFirstPackageDelay()
            + ", totalCost ms: "
            + timeCost);
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

@Slf4j
public class SynthesizeTextToSpeechWithCallbackConcurrently {
  public static void checkoutEnv(String envName, int defaultSize) {
    if (System.getenv(envName) != null) {
      System.out.println("[ENV CHECK]: " + envName + " " + System.getenv(envName));
    } else {
      System.out.println("[ENV CHECK]: " + envName + " Using Default which is " + defaultSize);
    }
  }

  public static void main(String[] args) throws InterruptedException, NoApiKeyException {
    // Check for connection pool env
    checkoutEnv("DASHSCOPE_CONNECTION_POOL_SIZE", 32);
    checkoutEnv("DASHSCOPE_MAXIMUM_ASYNC_REQUESTS", 32);
    checkoutEnv("DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST", 32);
    checkoutEnv(
        CosyvoiceObjectPool.COSYVOICE_OBJECTPOOL_SIZE_ENV,
        CosyvoiceObjectPool.DEFAULT_OBJECT_POOL_SIZE);

    int runTimes = 2;
    // Create the pool of SpeechSynthesis objects
    ExecutorService executorService = Executors.newFixedThreadPool(runTimes);

    for (int i = 0; i < runTimes; i++) {
      // Record the task submission time
      LocalDateTime submissionTime = LocalDateTime.now();
      executorService.submit(
          new SynthesizeTaskWithCallback(new String[] {"床前明月光，", "疑似地上霜。", "举头望明月，", "低头思故乡。"}));
    }

    // Shut down the ExecutorService and wait for all tasks to complete
    executorService.shutdown();
    executorService.awaitTermination(1, TimeUnit.MINUTES);
    System.exit(0);
  }
}
