/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package org.alibaba.speech.examples.speech_recognition;

import com.alibaba.dashscope.audio.asr.transcription.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import com.google.gson.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.*;
import java.net.HttpURLConnection;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;

class SenseVoiceParser {

  private static final List<String> EMOTION_LIST =
      Arrays.asList("NEUTRAL", "HAPPY", "ANGRY", "SAD");
  private static final List<String> EVENT_LIST =
      Arrays.asList("Speech", "Applause", "BGM", "Laughter");
  private static final List<String> ALL_TAGS =
      Arrays.asList(
          "Speech",
          "Applause",
          "BGM",
          "Laughter",
          "NEUTRAL",
          "HAPPY",
          "ANGRY",
          "SAD",
          "SPECIAL_TOKEN_1");

  /**
   * 本工具用于解析 sensevoice 识别结果
   *
   * @param data json格式的sensevoice转写结果
   * @param keepTrans 是否保留转写文本
   * @param keepEmotions 是否保留情感标签
   * @param keepEvents 是否保留事件标签
   * @return
   */
  public static JsonObject parseSenseVoiceResult(
      JsonObject data, boolean keepTrans, boolean keepEmotions, boolean keepEvents) {

    List<String> tagsToCleanup =
        ALL_TAGS.stream()
            .flatMap(tag -> Stream.of("<|" + tag + "|> ", "<|/" + tag + "|>", "<|" + tag + "|>"))
            .collect(Collectors.toList());

    JsonArray transcripts = data.getAsJsonArray("transcripts");

    for (JsonElement transcriptElement : transcripts) {
      JsonObject transcript = transcriptElement.getAsJsonObject();
      JsonArray sentences = transcript.getAsJsonArray("sentences");

      for (JsonElement sentenceElement : sentences) {
        JsonObject sentence = sentenceElement.getAsJsonObject();
        String text = sentence.get("text").getAsString();

        if (keepEmotions) {
          extractTags(sentence, text, EMOTION_LIST, "emotion");
        }

        if (keepEvents) {
          extractTags(sentence, text, EVENT_LIST, "event");
        }

        if (keepTrans) {
          String cleanText = getCleanText(text, tagsToCleanup);
          sentence.addProperty("text", cleanText);
        } else {
          sentence.remove("text");
        }
      }

      if (keepTrans) {
        transcript.addProperty(
            "text", getCleanText(transcript.get("text").getAsString(), tagsToCleanup));
      } else {
        transcript.remove("text");
      }

      JsonArray filteredSentences = new JsonArray();
      for (JsonElement sentenceElement : sentences) {
        JsonObject sentence = sentenceElement.getAsJsonObject();
        if (sentence.has("text") || sentence.has("emotion") || sentence.has("event")) {
          filteredSentences.add(sentence);
        }
      }
      transcript.add("sentences", filteredSentences);
    }
    return data;
  }

  private static void extractTags(
      JsonObject sentence, String text, List<String> tagList, String key) {
    String pattern = "<\\|(" + String.join("|", tagList) + ")\\|>";
    Pattern compiledPattern = Pattern.compile(pattern);
    Matcher matcher = compiledPattern.matcher(text);
    Set<String> tags = new HashSet<>();

    while (matcher.find()) {
      tags.add(matcher.group(1));
    }

    if (!tags.isEmpty()) {
      JsonArray tagArray = new JsonArray();
      tags.forEach(tagArray::add);
      sentence.add(key, tagArray);
    } else {
      sentence.remove(key);
    }
  }

  private static String getCleanText(String text, List<String> tagsToCleanup) {
    for (String tag : tagsToCleanup) {
      text = text.replace(tag, "");
    }
    return text.replaceAll("\\s{2,}", " ").trim();
  }
}

public class TranscriptFilesByRestfulApi {

  public static void main(String[] args) throws NoApiKeyException {
    // create transcription params, use getDashScopeApiKey to get api key.
    TranscriptionParam param =
        TranscriptionParam.builder()
            .apiKey(getDashScopeApiKey()) // set your apikey in config.Environments.yourApikey
            .model("sensevoice-v1") // 'paraformer-8k-v1', 'paraformer-mtl-v1'
            .fileUrls(
                Arrays.asList(
                    "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_example_1.wav",
                    "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/sample_video_poetry.mp4",
                    "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/long_audio_demo_cn.mp3"))
            .build();
    try {
      Transcription transcription = new Transcription();
      // post request to transcribe service
      TranscriptionResult result = transcription.asyncCall(param);

      System.out.println("RequestId: " + result.getRequestId());
      // waiting for transcription finish
      result =
          transcription.wait(
              TranscriptionQueryParam.FromTranscriptionParam(param, result.getTaskId()));
      // get Transcription result after waiting
      List<TranscriptionTaskResult> taskResultList = result.getResults();
      if (taskResultList != null && !taskResultList.isEmpty()) {
        for (TranscriptionTaskResult taskResult : taskResultList) {
          // get Transcription rersult url
          String transcriptionUrl = taskResult.getTranscriptionUrl();
          // get transcription result by http get
          HttpURLConnection connection =
              (HttpURLConnection) new URL(transcriptionUrl).openConnection();
          connection.setRequestMethod("GET");
          connection.connect();
          BufferedReader reader =
              new BufferedReader(new InputStreamReader(connection.getInputStream()));
          // format json print
          Gson gson = new GsonBuilder().setPrettyPrinting().create();
          JsonElement jsonResult = gson.fromJson(reader, JsonObject.class);
          System.out.println(gson.toJson(jsonResult));
          System.out.println(
              gson.toJson(
                  SenseVoiceParser.parseSenseVoiceResult(
                      jsonResult.getAsJsonObject(), true, true, true)));
        }
      }
    } catch (Exception e) {
      System.out.println("error: " + e);
    }
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
