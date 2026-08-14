/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package org.alibaba.speech.examples.speech_recognition;

import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import com.alibaba.dashscope.utils.Constants;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * A demo of the most basic streaming file recognition with qwen-audio-3.0-asr-flash-streaming: read
 * a local audio file and print the recognition result.
 *
 * <p>Advanced capabilities are demonstrated in dedicated samples: the dialog context in
 * recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-context and the pre-created vocabulary
 * in recognize_speech_qwen-audio-3.0-asr-flash-streaming-with-vocabulary.
 *
 * <p>for more information, please refer to https://help.aliyun.com/document_detail/2712536.html
 */
public class RecognizeSpeechFromFile {
  // supported model : 'qwen-audio-3.0-asr-flash-streaming'
  private static final String MODEL = "qwen-audio-3.0-asr-flash-streaming";

  // the local audio file, relative to the JVM working directory (the java module directory)
  private static final String AUDIO_RELATIVE_PATH =
      "../../../../samples/sample-data/hello_world_male_16k_16bit_mono.wav";

  public static void main(String[] args) throws NoApiKeyException {
    initDashScopeEndpoint();

    RecognitionParam param =
        RecognitionParam.builder()
            .apiKey(getDashScopeApiKey())
            .model(MODEL)
            .format("wav") // 'pcm', 'wav', 'opus', 'speex', 'aac', 'amr'
            .sampleRate(16000) // supported 8000, 16000
            .build();

    Path filePath = Paths.get(System.getProperty("user.dir"), AUDIO_RELATIVE_PATH).normalize();
    File audioFile = filePath.toFile();
    if (!audioFile.exists()) {
      System.err.println("audio file not found: " + filePath);
      System.err.println("current working directory: " + System.getProperty("user.dir"));
      System.exit(1);
    }
    System.out.println("recognizing local file: " + filePath);

    Recognition recognizer = new Recognition();
    String result = recognizer.call(param, audioFile);

    try {
      Files.write(Paths.get("result.json"), result.getBytes(StandardCharsets.UTF_8));
      System.out.println("full recognition result is saved into file: result.json");
    } catch (IOException e) {
      System.err.println("failed to save result.json: " + e.getMessage());
    }

    System.out.println("\nthe brief result is:");
    Gson gson = new GsonBuilder().setPrettyPrinting().create();
    JsonObject jsonObject = gson.fromJson(result, JsonObject.class);
    if (jsonObject.has("sentences")) {
      for (JsonElement sentence : jsonObject.get("sentences").getAsJsonArray()) {
        System.out.println(sentence.getAsJsonObject().get("text").getAsString());
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
   * The qwen-audio series models are served under a workspace-specific endpoint, so both the HTTP
   * and the WebSocket base urls have to be redirected to
   * https://{workspace_id}.cn-beijing.maas.aliyuncs.com . The workspace id can be found on the
   * Alibaba Cloud Model Studio console.
   */
  private static void initDashScopeEndpoint() {
    String workspaceId = System.getenv("DASHSCOPE_WORKSPACE_ID");
    if (workspaceId == null || workspaceId.isEmpty()) {
      System.err.println(
          "the environment variable DASHSCOPE_WORKSPACE_ID is required, because the qwen-audio"
              + " series models are served under a workspace-specific endpoint. Please set it to"
              + " your Model Studio workspace id, for example: export"
              + " DASHSCOPE_WORKSPACE_ID=llm-xxxxxx");
      System.exit(1);
    }
    Constants.baseHttpApiUrl = "https://" + workspaceId + ".cn-beijing.maas.aliyuncs.com/api/v1";
    Constants.baseWebsocketApiUrl =
        "wss://" + workspaceId + ".cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
  }

  /**
   * Set your DashScope API key. More information: <a
   * href="https://help.aliyun.com/document_detail/2712195.html">...</a> In fact, if you have set
   * DASHSCOPE_API_KEY in your environment variable, you can ignore this, and the SDK will
   * automatically get the api_key from the environment variable
   */
  private static String getDashScopeApiKey() {
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
