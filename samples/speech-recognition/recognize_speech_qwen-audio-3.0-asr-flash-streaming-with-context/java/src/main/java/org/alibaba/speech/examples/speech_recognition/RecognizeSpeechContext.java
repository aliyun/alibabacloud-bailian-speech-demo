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
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * A demo focusing on the conversation context (<code>context</code>) of
 * qwen-audio-3.0-asr-flash-streaming. The context is passed through the <code>input</code>
 * parameter of RecognitionParam and helps the model recognize domain-specific words, proper nouns
 * and follow-up utterances more accurately.
 *
 * <p>Two ways to use the context are demonstrated:
 *
 * <ol>
 *   <li>dialog history: previous user utterances and assistant replies
 *   <li>domain word list: a <code>user</code> message carrying domain terms only
 * </ol>
 *
 * <p>Constraints of the context (enforced by the service):
 *
 * <ul>
 *   <li>at most 5 <code>input_text</code> messages and 5 <code>text</code> messages, the latest are
 *       kept
 *   <li>the total text length of one round must not exceed 400 characters
 *   <li>messages must be ordered by round, and the <code>user</code> message of one round must come
 *       before its <code>assistant</code> message
 *   <li>requires dashscope SDK &gt;= 2.22.23
 * </ul>
 *
 * for more information, please refer to https://help.aliyun.com/document_detail/2712536.html
 */
public class RecognizeSpeechContext {
  // supported model : 'qwen-audio-3.0-asr-flash-streaming'
  private static final String MODEL = "qwen-audio-3.0-asr-flash-streaming";

  // the local audio file, relative to the JVM working directory (the java module directory)
  private static final String AUDIO_RELATIVE_PATH =
      "../../../../samples/sample-data/hello_world_male_16k_16bit_mono.wav";

  // the service keeps at most 5 messages for each content type
  private static final int MAX_MESSAGES_PER_TYPE = 5;

  // the total text length of one round must not exceed 400 characters
  private static final int MAX_CONTEXT_TEXT_LENGTH = 400;

  /** A single round of the conversation history. */
  private static class Message {
    final String role;
    final String text;

    Message(String role, String text) {
      this.role = role;
      this.text = text;
    }
  }

  public static void main(String[] args) throws NoApiKeyException {
    initDashScopeEndpoint();

    Path filePath = Paths.get(System.getProperty("user.dir"), AUDIO_RELATIVE_PATH).normalize();
    File audioFile = filePath.toFile();
    if (!audioFile.exists()) {
      System.err.println("audio file not found: " + filePath);
      System.err.println("current working directory: " + System.getProperty("user.dir"));
      System.exit(1);
    }
    System.out.println("recognizing local file: " + filePath);

    // ---- Example 1 : baseline, recognize without any context ----
    System.out.println("\n=== Example 1: without context (baseline) ===");
    recognizeSpeechWithContext(audioFile, null);

    // ---- Example 2 : dialog history as context ----
    // note the order: the `user` message of one round comes before its `assistant` message.
    System.out.println("\n=== Example 2: dialog history as context ===");
    List<Message> dialogHistory =
        Arrays.asList(
            new Message("user", "你好啊"),
            new Message("assistant", "你好啊，我是通义千问，有什么可以帮助你的？"),
            new Message("user", "帮我看看今天的会议纪要"),
            new Message("assistant", "好的，今天的会议主要讨论了语音识别模型的迭代计划。"));
    recognizeSpeechWithContext(audioFile, dialogHistory);

    // ---- Example 3 : domain word list as context ----
    // besides the dialog history, a single `user` message can also carry a list of domain terms.
    // This is useful when there is no dialog history but the audio contains many proper nouns.
    System.out.println("\n=== Example 3: domain word list as context ===");
    List<Message> domainTerms =
        Arrays.asList(new Message("user", "相关术语：语音实验室、通义千问、百炼平台、声音复刻、热词表、说话人分离"));
    recognizeSpeechWithContext(audioFile, domainTerms);

    // ---- Example 4 : context exceeding the limits is trimmed ----
    // 7 user messages and a very long text are provided on purpose to show how buildContext()
    // keeps the latest 5 messages per type and truncates the text to 400 characters.
    System.out.println("\n=== Example 4: context exceeding the limits is trimmed ===");
    List<Message> oversizedHistory = new ArrayList<>();
    for (int i = 1; i <= 7; i++) {
      oversizedHistory.add(new Message("user", "第" + i + "轮的历史内容"));
    }
    StringBuilder longReply = new StringBuilder();
    for (int i = 0; i < 60; i++) {
      longReply.append("这是一段很长的回复。"); // far beyond 400 characters
    }
    oversizedHistory.add(new Message("assistant", longReply.toString()));
    recognizeSpeechWithContext(audioFile, oversizedHistory);

    System.exit(0);
  }

  /**
   * Convert a simple conversation history list into the <code>input</code> structure required by
   * the service:
   *
   * <pre>
   * {
   *   "context": [
   *     {"role": "user",      "content": [{"type": "input_text", "text": "..."}]},
   *     {"role": "assistant", "content": [{"type": "text",       "text": "..."}]}
   *   ]
   * }
   * </pre>
   *
   * The <code>user</code> role carries the recognition result of previous rounds or a domain word
   * list, the <code>assistant</code> role carries the replies of the LLM. Returns null when there
   * is no valid history.
   */
  private static Map<String, Object> buildContext(List<Message> historyMessages) {
    if (historyMessages == null || historyMessages.isEmpty()) {
      return null;
    }

    // keep at most MAX_MESSAGES_PER_TYPE messages for each role, the latest win
    List<Message> userMessages = new ArrayList<>();
    List<Message> assistantMessages = new ArrayList<>();
    for (Message msg : historyMessages) {
      if ("user".equals(msg.role)) {
        userMessages.add(msg);
      } else if ("assistant".equals(msg.role)) {
        assistantMessages.add(msg);
      }
    }
    List<Message> kept = new ArrayList<>();
    kept.addAll(
        userMessages.subList(
            Math.max(0, userMessages.size() - MAX_MESSAGES_PER_TYPE), userMessages.size()));
    kept.addAll(
        assistantMessages.subList(
            Math.max(0, assistantMessages.size() - MAX_MESSAGES_PER_TYPE),
            assistantMessages.size()));

    List<Map<String, Object>> contextList = new ArrayList<>();
    int totalLength = 0;
    for (Message msg : historyMessages) {
      if (!kept.contains(msg)) {
        continue;
      }
      String text = msg.text;
      if (msg.role == null || text == null || text.isEmpty()) {
        continue;
      }

      // truncate from the tail once the total length limit is reached
      int remaining = MAX_CONTEXT_TEXT_LENGTH - totalLength;
      if (remaining <= 0) {
        System.out.println(
            "[context] total text length limit reached, the remaining messages are dropped.");
        break;
      }
      if (text.length() > remaining) {
        text = text.substring(0, remaining);
        System.out.println("[context] message truncated to fit the 400-character limit.");
      }
      totalLength += text.length();

      // user -> input_text, assistant -> text
      Map<String, Object> content = new HashMap<>();
      content.put("type", "user".equals(msg.role) ? "input_text" : "text");
      content.put("text", text);

      Map<String, Object> message = new HashMap<>();
      message.put("role", msg.role);
      message.put("content", Arrays.asList(content));
      contextList.add(message);
    }

    if (contextList.isEmpty()) {
      return null;
    }
    Map<String, Object> input = new HashMap<>();
    input.put("context", contextList);
    return input;
  }

  /** Recognize a local audio file, optionally carrying a conversation context. */
  private static void recognizeSpeechWithContext(File audioFile, List<Message> conversationHistory)
      throws NoApiKeyException {
    Map<String, Object> input = buildContext(conversationHistory);
    if (input != null) {
      System.out.println(
          "[context] "
              + ((List<?>) input.get("context")).size()
              + " message(s) sent to the service.");
    } else {
      System.out.println("[context] no context is sent.");
    }

    RecognitionParam.RecognitionParamBuilder<?, ?> builder =
        RecognitionParam.builder()
            .apiKey(getDashScopeApiKey())
            .model(MODEL)
            .format("wav") // 'pcm', 'wav', 'opus', 'speex', 'aac', 'amr'
            .sampleRate(16000); // supported 8000, 16000

    // the context is passed through the `input` parameter
    if (input != null) {
      builder.input(input);
    }
    RecognitionParam param = builder.build();

    Recognition recognizer = new Recognition();
    String result = recognizer.call(param, audioFile);

    System.out.println("the brief result is:");
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
