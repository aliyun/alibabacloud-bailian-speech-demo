/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package org.alibaba.speech.examples.speech_synthesizer;

import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import io.reactivex.Flowable;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.Objects;
import org.alibaba.speech.utils.RealtimeMp3Player;

/**
 * this demo showcases how to use Alibaba Cloud's DashScope model for synthesis llm streaming output
 * text and playback of MP3 audio streams. Note that this demo presents a simplified usage. For
 * adjustments regarding audio format and sample rate, please refer to the documentation.
 */
public class SynthesizeSpeechFromLlmByStreamingMode {
  static RealtimeMp3Player audioPlayer = new RealtimeMp3Player(); // use to play mp3

  public static void LLMTextToPlayer(String text_to_query)
      throws NoApiKeyException, InputRequiredException {

    // start audio player
    audioPlayer.start();
    class ReactCallback extends ResultCallback<SpeechSynthesisResult> {
      ReactCallback() {}

      @Override
      public void onEvent(SpeechSynthesisResult message) {
        // Write Audio to player
        if (message.getAudioFrame() != null) {
          audioPlayer.write(message.getAudioFrame());
        }
      }

      @Override
      public void onComplete() {
        audioPlayer.stop();
        System.out.println("synthesis onComplete!");
      }

      @Override
      public void onError(Exception e) {
        audioPlayer.stop();
        System.out.println("synthesis onError!");
        e.printStackTrace();
      }
    }

    /** ***** Call the Generative AI Model to get streaming text ****** */
    // Prepare for the LLM call
    Generation gen = new Generation();
    Message systemMsg =
        Message.builder()
            .role(Role.SYSTEM.getValue())
            .content("你是一个闲聊型语音AI助手，主要任务是和用户展开日常性的友善聊天。请不要回复使用任何格式化文本，回复要求口语化，不要使用markdown格式或者列表。")
            .build();
    Message userMsg = Message.builder().role(Role.USER.getValue()).content(text_to_query).build();
    GenerationParam genParam =
        GenerationParam.builder()
            .apiKey(getDashScopeApiKey())
            .model("qwen-plus")
            .messages(Arrays.asList(systemMsg, userMsg))
            .resultFormat(GenerationParam.ResultFormat.MESSAGE)
            .topP(0.8)
            .incrementalOutput(true)
            .build();

    // Prepare the speech synthesis task
    SpeechSynthesisParam param =
        SpeechSynthesisParam.builder()
            .model("cosyvoice-v2")
            .voice("longhua_v2")
            .apiKey(getDashScopeApiKey())
            .build();
    SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, new ReactCallback());
    System.out.println("Query: " + text_to_query);

    // Get LLM result stream
    Flowable<GenerationResult> result = gen.streamCall(genParam);
    System.out.print("LLM output: ");
    result.blockingForEach(
        message -> {
          String text = message.getOutput().getChoices().get(0).getMessage().getContent();
          System.out.print(text);
          if (!Objects.equals(text, "")) {
            // send llm result to synthesizer
            synthesizer.streamingCall(text);
          }
        });
    System.out.print("\n");
    synthesizer.streamingComplete();
    System.out.println(
        "[Metric] requestId: "
            + synthesizer.getLastRequestId()
            + ", first package delay ms: "
            + synthesizer.getFirstPackageDelay());
  }

  public static void main(String[] args)
      throws FileNotFoundException, InterruptedException, NoApiKeyException,
          InputRequiredException {
    String text_to_query = "番茄炒鸡蛋怎么做？";
    LLMTextToPlayer(text_to_query);
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
