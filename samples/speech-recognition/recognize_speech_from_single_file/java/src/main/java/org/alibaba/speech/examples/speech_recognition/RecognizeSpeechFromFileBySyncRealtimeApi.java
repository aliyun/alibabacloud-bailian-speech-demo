/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package org.alibaba.speech.examples.speech_recognition;

import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

public class RecognizeSpeechFromFileBySyncRealtimeApi {
  public static void main(String[] args) throws NoApiKeyException {
    // Create recognition params
    // you can customize the recognition parameters, like model, format,
    // sample_rate for more information, please refer to
    // https://help.aliyun.com/document_detail/2712536.html
    RecognitionParam param =
        RecognitionParam.builder()
            .model("paraformer-realtime-v2")
            .format("pcm") // 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you
            // can check the supported formats in the document
            .sampleRate(16000) // supported 8000、16000
            .apiKey(getDashScopeApiKey()) // set your apikey in config.Environments.yourApikey
            .build();
    Recognition recognizer = new Recognition();
    // Please replace the path with your audio file path
    String currentDir = System.getProperty("user.dir");
    Path filePath =
        Paths.get(currentDir, "../../../sample-data/hello_world_male_16k_16bit_mono.wav");
    System.out.println("Input file_path is: " + filePath);
    // Start recognition with the audio file
    String result = recognizer.call(param, filePath.toFile());

    System.out.println("Full recognition result is saved into file: result.json ");
    System.out.println("\nThe brief result is:");
    FileOutputStream fos = null;
    try {
      fos = new FileOutputStream("result.json");
      fos.write(result.getBytes());
      fos.close();
    } catch (IOException e) {
      throw new RuntimeException(e);
    }

    // format json print
    Gson gson = new GsonBuilder().setPrettyPrinting().create();
    JsonObject jsonObject = gson.fromJson(result, JsonObject.class);

    if (jsonObject.has("sentences")) {
      for (JsonElement sent : jsonObject.get("sentences").getAsJsonArray()) {
        JsonObject sentObj = sent.getAsJsonObject();
        System.out.println(sentObj.get("text").getAsString());
      }
    }

    System.out.println(
        "[Metric] requestId: "
            + recognizer.getLastRequestId()
            + ", first package delay ms: "
            + recognizer.getFirstPackageDelay()
            + ", last package delay ms: "
            + recognizer.getLastPackageDelay());

    System.exit(0);
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
