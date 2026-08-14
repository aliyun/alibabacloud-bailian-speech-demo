/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package org.alibaba.speech.examples.speech_recognition;

import com.alibaba.dashscope.audio.asr.transcription.Transcription;
import com.alibaba.dashscope.audio.asr.transcription.TranscriptionParam;
import com.alibaba.dashscope.audio.asr.transcription.TranscriptionQueryParam;
import com.alibaba.dashscope.audio.asr.transcription.TranscriptionResult;
import com.alibaba.dashscope.audio.asr.transcription.TranscriptionTaskResult;
import com.alibaba.dashscope.common.TaskStatus;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import com.alibaba.dashscope.utils.Constants;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * A demo of file transcription with a custom vocabulary, using qwen-audio-3.0-asr-flash-filetrans.
 * It submits the task asynchronously and polls the task status with fetch() until it succeeds or
 * fails. for more information, please refer to https://help.aliyun.com/document_detail/2712535.html
 */
public class RecognizeSpeechTransFetch {
  // supported model : 'qwen-audio-3.0-asr-flash-filetrans'
  private static final String MODEL = "qwen-audio-3.0-asr-flash-filetrans";

  // the audio url, must be accessible from the public network
  private static final String AUDIO_URL =
      "https://gw.alipayobjects.com/os/bmw-prod/0574ee2e-f494-45a5-820f-63aee583045a.wav";

  // poll interval and max attempts to avoid waiting forever
  private static final long POLL_INTERVAL_MS = 1000;
  private static final int MAX_POLL_ATTEMPTS = 180;

  public static void main(String[] args) {
    // the qwen-audio filetrans model is served under a workspace-specific endpoint
    Constants.baseHttpApiUrl =
        "https://" + getWorkspaceId() + ".cn-beijing.maas.aliyuncs.com/api/v1";

    try {
      // Build an instant custom vocabulary. Key: hotword text, Value: weight, which accepts
      // [1, 5] (regular hotword, 4 recommended) or 50 (super hotword). A super hotword boosts
      // recall dramatically, but at most 50 of them are allowed and only the
      // qwen-audio-3.0-asr-flash-streaming, -filetrans and -flash series support it.
      Map<String, Integer> vocabulary = new HashMap<>();
      vocabulary.put("通义千问", 50); // super hotword
      vocabulary.put("阿里巴巴", 4);
      vocabulary.put("百炼", 4);

      // language_hints (optional): zh=Chinese, en=English. Leave it unset to let the
      // model detect the language automatically. This model supports up to 4 values.
      TranscriptionParam param =
          TranscriptionParam.builder()
              .apiKey(getDashScopeApiKey())
              .model(MODEL)
              .parameter("vocabulary", vocabulary)
              .parameter("language_hints", new String[] {"zh", "en"})
              .fileUrls(Arrays.asList(AUDIO_URL))
              .build();

      Transcription transcription = new Transcription();

      // asyncCall submits the task and returns immediately with a task id
      TranscriptionResult result = transcription.asyncCall(param);
      String taskId = result.getTaskId();
      if (taskId == null) {
        System.err.println("task submission failed: " + result.getOutput());
        System.exit(1);
      }
      System.out.println("task submitted, requestId: " + result.getRequestId());
      System.out.println("taskId: " + taskId);

      // poll the task status with fetch() until it succeeds or fails
      TranscriptionQueryParam queryParam =
          TranscriptionQueryParam.FromTranscriptionParam(param, taskId);
      TaskStatus status = null;
      for (int i = 0; i < MAX_POLL_ATTEMPTS; i++) {
        result = transcription.fetch(queryParam);
        status = result.getTaskStatus();
        System.out.println("current status: " + status);
        if (status == TaskStatus.SUCCEEDED || status == TaskStatus.FAILED) {
          break;
        }
        Thread.sleep(POLL_INTERVAL_MS);
      }

      if (status != TaskStatus.SUCCEEDED || !printResults(result)) {
        System.exit(1);
      }
    } catch (Exception e) {
      e.printStackTrace();
      System.exit(1);
    }

    System.exit(0);
  }

  /** Print the transcription results. Returns true when all sub-tasks succeeded. */
  private static boolean printResults(TranscriptionResult result) throws Exception {
    List<TranscriptionTaskResult> subTasks = result.getResults();
    if (subTasks == null || subTasks.isEmpty()) {
      System.err.println("no sub-tasks found in result.");
      return false;
    }

    boolean allSucceeded = true;
    for (TranscriptionTaskResult subTask : subTasks) {
      System.out.println("file url: " + subTask.getFileUrl());
      TaskStatus subStatus = subTask.getSubTaskStatus();
      System.out.println("sub-task status: " + subStatus);
      if (subStatus == TaskStatus.SUCCEEDED) {
        downloadAndPrintResult(subTask.getTranscriptionUrl());
      } else {
        allSucceeded = false;
        System.err.println("sub-task failed: " + subTask.getMessage());
      }
    }
    return allSucceeded;
  }

  /** Download the transcription_url and print the JSON content. */
  private static void downloadAndPrintResult(String url) throws Exception {
    if (url == null || url.isEmpty()) {
      System.out.println("transcription url is empty.");
      return;
    }

    HttpURLConnection connection = (HttpURLConnection) new URL(url).openConnection();
    connection.setRequestMethod("GET");
    connection.setConnectTimeout(10000);
    connection.setReadTimeout(30000);
    if (connection.getResponseCode() != 200) {
      System.err.println("failed to download result, http code: " + connection.getResponseCode());
      return;
    }

    GsonBuilder gsonBuilder = new GsonBuilder().setPrettyPrinting();
    try (BufferedReader reader =
        new BufferedReader(
            new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))) {
      JsonObject jsonResult = gsonBuilder.create().fromJson(reader, JsonObject.class);
      System.out.println("recognition result:");
      System.out.println(gsonBuilder.create().toJson(jsonResult));
    } finally {
      connection.disconnect();
    }
  }

  private static String getWorkspaceId() {
    return System.getenv().getOrDefault("DASHSCOPE_WORKSPACE_ID", "your-workspace-id");
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
