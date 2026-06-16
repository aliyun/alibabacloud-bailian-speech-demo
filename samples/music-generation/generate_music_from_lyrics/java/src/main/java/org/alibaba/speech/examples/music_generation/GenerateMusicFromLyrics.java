/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package org.alibaba.speech.examples.music_generation;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class GenerateMusicFromLyrics {

  private static final String ENDPOINT =
      "https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation";
  private static final String MODEL = "fun-music-v1";
  private static final String LYRICS =
      "[verse]\n"
          + "清晨的阳光穿过窗帘,\n"
          + "咖啡的香气弥漫房间.\n"
          + "翻开昨天未读完的书,\n"
          + "时光就这样悄悄流转.\n\n"
          + "[chorus]\n"
          + "慢慢来不着急,\n"
          + "生活本该如此惬意.\n"
          + "把烦恼都丢进风里,\n"
          + "拥抱每一个晴天雨季.";
  private static final String GENDER = "female";
  private static final String FILE_TO_SAVE = "result.mp3";

  public static void main(String[] args) throws Exception {
    String apiKey = getDashScopeApiKey();

    // Build JSON request body
    JsonObject input = new JsonObject();
    input.addProperty("lyrics", LYRICS);
    input.addProperty("gender", GENDER);

    JsonObject requestBody = new JsonObject();
    requestBody.addProperty("model", MODEL);
    requestBody.add("input", input);

    String jsonBody = requestBody.toString();
    System.out.println("Request body: " + jsonBody);

    // Send HTTP POST request
    HttpURLConnection conn = (HttpURLConnection) new URL(ENDPOINT).openConnection();
    conn.setRequestMethod("POST");
    conn.setRequestProperty("Authorization", "Bearer " + apiKey);
    conn.setRequestProperty("Content-Type", "application/json");
    conn.setDoOutput(true);
    conn.setConnectTimeout(60000);
    conn.setReadTimeout(60000);

    try (OutputStream os = conn.getOutputStream()) {
      os.write(jsonBody.getBytes(StandardCharsets.UTF_8));
    }

    int responseCode = conn.getResponseCode();
    InputStream inputStream =
        (responseCode >= 200 && responseCode < 300) ? conn.getInputStream() : conn.getErrorStream();

    StringBuilder responseBuilder = new StringBuilder();
    try (BufferedReader reader =
        new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8))) {
      String line;
      while ((line = reader.readLine()) != null) {
        responseBuilder.append(line);
      }
    }

    String responseStr = responseBuilder.toString();
    System.out.println("Response: " + responseStr);

    if (responseCode >= 200 && responseCode < 300) {
      Gson gson = new Gson();
      JsonObject responseJson = gson.fromJson(responseStr, JsonObject.class);

      if (responseJson.has("output")
          && responseJson.getAsJsonObject("output").has("audio")
          && responseJson.getAsJsonObject("output").getAsJsonObject("audio").has("url")) {
        String audioUrl =
            responseJson
                .getAsJsonObject("output")
                .getAsJsonObject("audio")
                .get("url")
                .getAsString();
        System.out.println("Music generation successful!");
        System.out.println("Audio URL: " + audioUrl);

        // Download the audio file
        downloadFile(audioUrl, FILE_TO_SAVE);
        System.out.println("Audio saved to: " + FILE_TO_SAVE);
      } else {
        System.out.println("Music generation failed or unexpected response format.");
      }

      if (responseJson.has("usage")) {
        JsonObject usage = responseJson.getAsJsonObject("usage");
        System.out.println(
            "[Usage] input_tokens: " + usage.get("input_tokens").getAsString());
      }
    } else {
      System.out.println("Request failed with code: " + responseCode);
    }

    System.exit(0);
  }

  private static void downloadFile(String fileUrl, String outputPath) throws IOException {
    URL url = new URL(fileUrl);
    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
    conn.setRequestMethod("GET");

    try (InputStream in = conn.getInputStream();
        FileOutputStream out = new FileOutputStream(outputPath)) {
      byte[] buffer = new byte[4096];
      int bytesRead;
      while ((bytesRead = in.read(buffer)) != -1) {
        out.write(buffer, 0, bytesRead);
      }
    }
  }

  private static String getDashScopeApiKey() {
    String apiKey = System.getenv("DASHSCOPE_API_KEY");
    if (apiKey == null || apiKey.isEmpty()) {
      apiKey = "your-dashscope-api-key";
    }
    return apiKey;
  }
}
