/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package org.alibaba.speech.examples.speech_recognition;

import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.audio.asr.vocabulary.Vocabulary;
import com.alibaba.dashscope.audio.asr.vocabulary.VocabularyService;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import com.alibaba.dashscope.utils.Constants;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * A demo of streaming recognition with a pre-created custom vocabulary, using
 * qwen-audio-3.0-asr-flash-streaming. The full flow is: create a vocabulary -> get its id -> pass
 * the id when recognizing -> delete the vocabulary. for more information, please refer to
 * https://help.aliyun.com/document_detail/2712536.html
 */
public class RecognizeSpeechVocabulary {
  // supported model : 'qwen-audio-3.0-asr-flash-streaming'
  private static final String MODEL = "qwen-audio-3.0-asr-flash-streaming";

  // the local audio file, relative to the JVM working directory (the java module directory)
  private static final String AUDIO_RELATIVE_PATH =
      "../../../../samples/sample-data/hello_world_male_16k_16bit_mono.wav";

  public static void main(String[] args) throws NoApiKeyException, InputRequiredException {
    String apiKey = getDashScopeApiKey();
    initDashScopeEndpoint();

    // Build the custom vocabulary. "text" is the hotword, "weight" accepts [1, 5] (regular
    // hotword, 4 recommended) or 50 (super hotword). A super hotword boosts recall dramatically,
    // but at most 50 of them are allowed and only the qwen-audio-3.0-asr-flash-streaming,
    // -filetrans and -flash series support it.
    JsonArray vocabularyJson = new JsonArray();

    // a regular hotword
    JsonObject hotword = new JsonObject();
    hotword.addProperty("text", "语音实验室");
    hotword.addProperty("weight", 4);
    vocabularyJson.add(hotword);

    // a super hotword
    JsonObject superHotword = new JsonObject();
    superHotword.addProperty("text", "通义千问");
    superHotword.addProperty("weight", 50);
    vocabularyJson.add(superHotword);

    VocabularyService service = new VocabularyService(apiKey);

    Vocabulary vocabulary = null;
    try {
      vocabulary = service.createVocabulary(MODEL, "testpfx", vocabularyJson);
      System.out.println("vocabulary created with id: " + vocabulary.getVocabularyId());

      if (!"OK".equals(service.queryVocabulary(vocabulary.getVocabularyId()).getStatus())) {
        System.err.println("vocabulary status is not OK.");
        System.exit(1);
      }
      System.out.println("vocabulary status is OK, starting recognition...");

      Path filePath = Paths.get(System.getProperty("user.dir"), AUDIO_RELATIVE_PATH).normalize();
      File audioFile = filePath.toFile();
      if (!audioFile.exists()) {
        System.err.println("audio file not found: " + filePath);
        System.err.println("current working directory: " + System.getProperty("user.dir"));
        System.exit(1);
      }
      System.out.println("recognizing local file: " + filePath);

      RecognitionParam param =
          RecognitionParam.builder()
              .apiKey(apiKey)
              .model(MODEL)
              .format("wav") // 'pcm', 'wav', 'opus', 'speex', 'aac', 'amr'
              .sampleRate(16000) // supported 8000, 16000
              .vocabularyId(vocabulary.getVocabularyId())
              .build();

      Recognition recognizer = new Recognition();
      try {
        String result = recognizer.call(param, audioFile);
        System.out.println("recognition result: " + result);
      } finally {
        recognizer.getDuplexApi().close(1000, "bye");
      }
    } catch (Exception e) {
      e.printStackTrace();
      System.exit(1);
    } finally {
      // always delete the vocabulary to avoid consuming the quota
      if (vocabulary != null) {
        try {
          service.deleteVocabulary(vocabulary.getVocabularyId());
          System.out.println("vocabulary deleted.");
        } catch (Exception e) {
          System.err.println("failed to delete vocabulary: " + e.getMessage());
        }
      }
    }

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
