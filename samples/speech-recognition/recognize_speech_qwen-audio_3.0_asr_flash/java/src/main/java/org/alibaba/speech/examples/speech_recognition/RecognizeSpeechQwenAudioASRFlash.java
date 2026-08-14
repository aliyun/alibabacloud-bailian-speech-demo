/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package org.alibaba.speech.examples.speech_recognition;

import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import java.io.IOException;
import java.util.concurrent.TimeUnit;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

/**
 * A demo of qwen-audio-3.0-asr-flash speech recognition in non-streaming mode with conversation
 * context. The context helps to improve the recognition accuracy of proper nouns. for more
 * information, please refer to https://help.aliyun.com/document_detail/2712536.html
 */
public class RecognizeSpeechQwenAudioASRFlash {
  // supported model : 'qwen-audio-3.0-asr-flash'
  private static final String MODEL = "qwen-audio-3.0-asr-flash";

  // the audio url, must be accessible from the public network, or a base64 data uri
  private static final String AUDIO_URL =
      "https://gw.alipayobjects.com/os/bmw-prod/0574ee2e-f494-45a5-820f-63aee583045a.wav";

  private static final MediaType JSON = MediaType.parse("application/json");

  public static void main(String[] args) {
    OkHttpClient client =
        new OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(60, TimeUnit.SECONDS)
            .build();
    Gson gson = new Gson();

    String url =
        "https://"
            + getWorkspaceId()
            + ".cn-beijing.maas.aliyuncs.com"
            + "/api/v1/services/aigc/multimodal-generation/generation";

    Request request =
        new Request.Builder()
            .url(url)
            .post(RequestBody.create(gson.toJson(buildRequestBody()), JSON))
            .addHeader("Authorization", "Bearer " + getDashScopeApiKey())
            .addHeader("Content-Type", "application/json")
            // X-DashScope-SSE controls whether to return results in SSE streaming mode.
            // set to 'enable' for incremental results, 'disable' for the final result only.
            .addHeader("X-DashScope-SSE", "disable")
            .build();

    try (Response response = client.newCall(request).execute()) {
      if (!response.isSuccessful() || response.body() == null) {
        System.err.println("request failed: " + response.code() + " " + response.message());
        if (response.body() != null) {
          System.err.println(response.body().string());
        }
        System.exit(1);
      }

      JsonObject jsonResponse = gson.fromJson(response.body().string(), JsonObject.class);
      System.out.println("recognition result: " + extractText(jsonResponse));
    } catch (IOException e) {
      e.printStackTrace();
      System.exit(1);
    }

    System.exit(0);
  }

  /**
   * Extract the recognized text from the response. The asr-flash model returns the text at
   * output.text, while the generic multimodal shape carries it at
   * output.choices[0].message.content[0].text.
   */
  private static String extractText(JsonObject jsonResponse) {
    JsonObject output = jsonResponse.getAsJsonObject("output");
    if (output == null) {
      return "";
    }
    if (output.has("text") && !output.get("text").isJsonNull()) {
      return output.get("text").getAsString();
    }
    if (!output.has("choices")) {
      return "";
    }
    JsonArray choices = output.getAsJsonArray("choices");
    if (choices.size() == 0) {
      return "";
    }
    JsonArray content =
        choices.get(0).getAsJsonObject().getAsJsonObject("message").getAsJsonArray("content");
    if (content.size() == 0) {
      return "";
    }
    return content.get(0).getAsJsonObject().get("text").getAsString();
  }

  /**
   * Build the multimodal request body. The two leading text messages act as the conversation
   * context, and the last message carries the audio to recognize.
   */
  private static JsonObject buildRequestBody() {
    JsonArray messages = new JsonArray();
    messages.add(textMessage("user", "input_text", "你好啊"));
    messages.add(textMessage("assistant", "text", "你好啊，我是通义千问，有什么可以帮助你的？"));

    JsonObject audioPart = new JsonObject();
    audioPart.addProperty("type", "input_audio");
    JsonObject inputAudio = new JsonObject();
    inputAudio.addProperty("data", AUDIO_URL);
    audioPart.add("input_audio", inputAudio);
    JsonArray audioContent = new JsonArray();
    audioContent.add(audioPart);
    JsonObject audioMessage = new JsonObject();
    audioMessage.addProperty("role", "user");
    audioMessage.add("content", audioContent);
    messages.add(audioMessage);

    JsonObject input = new JsonObject();
    input.add("messages", messages);

    JsonObject parameters = new JsonObject();
    parameters.addProperty("format", "wav");
    parameters.addProperty("sample_rate", 16000);

    JsonObject root = new JsonObject();
    root.addProperty("model", MODEL);
    root.add("input", input);
    root.add("parameters", parameters);
    return root;
  }

  private static JsonObject textMessage(String role, String type, String text) {
    JsonObject textPart = new JsonObject();
    textPart.addProperty("type", type);
    textPart.addProperty("text", text);
    JsonArray content = new JsonArray();
    content.add(textPart);
    JsonObject message = new JsonObject();
    message.addProperty("role", role);
    message.add("content", content);
    return message;
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
