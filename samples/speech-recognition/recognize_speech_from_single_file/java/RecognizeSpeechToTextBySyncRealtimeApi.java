/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package org.aliyun.bailian;

import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

public class RecognizeSpeechToTextBySyncRealtimeApi {
  public static void main(String[] args) throws NoApiKeyException {
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
    // Please replace the path with your audio file path
    String currentDir = System.getProperty("user.dir");
    Path filePath =
        Paths.get(currentDir, "hello_world_male_16k_16bit_mono.wav");
    System.out.println("Input file_path is: " + filePath);
    // Start recognition with the audio file
    String result = recognizer.call(param, filePath.toFile());
    // Check the result
    System.out.println(result);
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
