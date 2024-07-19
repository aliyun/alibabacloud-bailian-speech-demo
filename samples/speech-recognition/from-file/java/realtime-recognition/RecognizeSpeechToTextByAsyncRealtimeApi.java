package org.aliyun.bailian;

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

public class RecognizeSpeechToTextByAsyncRealtimeApi {
  public static void main(String[] args)
      throws NoApiKeyException, InterruptedException {
    // Create recognition params
    // you can customize the recognition parameters, like model, format,
    // sample_rate for more information, please refer to
    // https://help.aliyun.com/document_detail/2712536.html
    RecognitionParam param =
        RecognitionParam.builder()
            .model("paraformer-realtime-v1")
            .format("pcm") // 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you
                           // can check the supported formats in the document
            .sampleRate(16000) // supported 8000、16000
            .apiKey(
                getDashScopeApiKey()) // use getDashScopeApiKey to get api key.
            .build();
    Recognition recognizer = new Recognition();
    CountDownLatch latch = new CountDownLatch(1);
    ResultCallback<RecognitionResult> callback =
        new ResultCallback<RecognitionResult>() {
          @Override
          public void onEvent(RecognitionResult message) {
            if (message.isSentenceEnd()) {
              System.out.println("Fix:" + message.getSentence().getText());
            } else {
              System.out.println("Result: " + message.getSentence().getText());
            }
          }

          @Override
          public void onComplete() {
            System.out.println("Recognition complete");
            latch.countDown();
          }

          @Override
          public void onError(Exception e) {
            System.out.println("RecognitionCallback error: " + e.getMessage());
          }
        };
    // set param & callback
    recognizer.call(param, callback);
    // Please replace the path with your audio file path
    String currentDir = System.getProperty("user.dir");
    Path filePath =
        Paths.get(currentDir, "hello_world_male_16k_16bit_mono.wav");
    System.out.println("Input file_path is: " + filePath);
    // Read file and send audio by chunks
    try (FileInputStream fis = new FileInputStream(filePath.toFile())) {
      // chunk size set to 10 seconds for 16KHz sample rate
      byte[] buffer = new byte[32000 * 10];
      int bytesRead;
      // Loop to read chunks of the file
      while ((bytesRead = fis.read(buffer)) != -1) {
        ByteBuffer byteBuffer;
        // Handle the last chunk which might be smaller than the buffer size
        System.out.println("bytesRead: " + bytesRead);
        if (bytesRead < buffer.length) {
          byteBuffer = ByteBuffer.wrap(buffer, 0, bytesRead);
        } else {
          byteBuffer = ByteBuffer.wrap(buffer);
        }
        // Send the ByteBuffer to the recognition instance
        recognizer.sendAudioFrame(byteBuffer);
      }
      System.out.println(LocalDateTime.now());
    } catch (Exception e) {
      e.printStackTrace();
    }

    recognizer.stop();
    // wait for the recognition to complete
    latch.await();
    System.exit(0);
  }

  /**
   * Set your DashScope API key. More information: <a
   * href="https://help.aliyun.com/document_detail/2712195.html">...</a> In
   * fact, if you have set DASHSCOPE_API_KEY in your environment variable, you
   * can ignore this, and the SDK will automatically get the api_key from the
   * environment variable
   * */
  private static String getDashScopeApiKey() throws NoApiKeyException {
    String dashScopeApiKey = null;
    try {
      ApiKey apiKey = new ApiKey();
      dashScopeApiKey =
          apiKey.getApiKey(null); // Retrieve from environment variable.
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
