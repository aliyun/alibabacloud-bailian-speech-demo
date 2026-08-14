/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package org.alibaba.speech.examples.speech_synthesizer;

import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.concurrent.CountDownLatch;
import org.alibaba.speech.utils.RealtimeMp3Player;

/*
 * This demo showcases how to use Alibaba Cloud's DashScope model for real-time synthesis and playback of MP3 audio streams.
 * Note that this demo presents a simplified usage. For adjustments regarding audio format and sample rate,
 * please refer to the documentation.
 */
public class SynthesizeSpeechFromTextByQwenAudioTTSModel {
  // supported models : 'qwen-audio-3.0-tts-flash'、'qwen-audio-3.0-tts-plus'
  private static final String MODEL = "qwen-audio-3.0-tts-flash";

  // choose the voice matching the language of your text
  private static final String DEFAULT_VOICE = "longanfengyue";

  public static void main(String[] args) {
    String textToSynthesize = "今天的天气真不错！我们一起出去玩吧！";

    // ========================================================================
    // Example 1: Default style — synthesize plain text with the voice's native style
    // ========================================================================
    System.out.println("\n=== Example 1: Default style ===");
    synthesisTextToSpeechAndPlay(
        textToSynthesize, DEFAULT_VOICE, MODEL, null, "result_default.mp3");

    // ========================================================================
    // Example 2: Instruction — control speaking style via natural language
    // The instruction describes the desired voice persona, speed, tone, etc.
    // ========================================================================
    System.out.println("\n=== Example 2: Style instruction ===");
    String instructionStyle = "年轻活泼的女性声音，声音清脆甜美，语速很快，带有明显的上扬语调，适合介绍时尚产品";
    synthesisTextToSpeechAndPlay(
        textToSynthesize, DEFAULT_VOICE, MODEL, instructionStyle, "result_instruction_style.mp3");

    // ========================================================================
    // Example 3: Instruction — synthesize in a specific dialect
    // ========================================================================
    System.out.println("\n=== Example 3: Dialect instruction ===");
    String instructionDialect = "请用河南话表达";
    synthesisTextToSpeechAndPlay(
        textToSynthesize, DEFAULT_VOICE, MODEL, instructionDialect, "result_instruction_dialect.mp3");

    // ========================================================================
    // Example 4: Emotion & rich-language tags embedded in text
    // Control tags (e.g. [excited]) set emotion for following text.
    // Rich-language tags (e.g. [laughing]) insert sound effects at that position.
    // Supported tags: [sad], [excited], [angry], [serious], [whispers], [laughing],
    // [sighing], [giggles], [cough], etc. Full list in the official documentation.
    // ========================================================================
    System.out.println("\n=== Example 4: Emotion & rich-language tags ===");
    String textWithEmotion = "[excited]今天的天气真不错！[laughing]我们一起出去玩吧！";
    synthesisTextToSpeechAndPlay(
        textWithEmotion, DEFAULT_VOICE, MODEL, null, "result_emotion_tags.mp3");

    System.exit(0);
  }

  /**
   * Synthesize speech with given text, play the synthesized audio in real-time and save it into
   * outputFile. The optional 'instruction' controls the speaking style, emotion or dialect.
   */
  public static void synthesisTextToSpeechAndPlay(
      String text, String voice, String model, String instruction, String outputFile) {
    // use to play mp3. You need import RealtimeMp3Player.java
    RealtimeMp3Player audioPlayer = new RealtimeMp3Player();
    // Start the player
    audioPlayer.start();

    class ReactCallback extends ResultCallback<SpeechSynthesisResult> {
      final CountDownLatch latch = new CountDownLatch(1);
      final FileOutputStream fos;

      ReactCallback() throws FileNotFoundException {
        this.fos = new FileOutputStream(new File(outputFile));
      }

      @Override
      public void onEvent(SpeechSynthesisResult message) {
        if (message.getAudioFrame() != null) {
          // Write Audio to player
          audioPlayer.write(message.getAudioFrame());
          try {
            // save audio to file
            fos.write(message.getAudioFrame().array());
          } catch (IOException e) {
            throw new RuntimeException(e);
          }
        }
      }

      @Override
      public void onComplete() {
        audioPlayer.stop();
        System.out.println("speech synthesis task complete successfully.");
        closeFile();
        latch.countDown();
      }

      @Override
      public void onError(Exception e) {
        audioPlayer.stop();
        System.out.println("speech synthesis task failed: " + e.getMessage());
        e.printStackTrace();
        closeFile();
        // wake up the main thread on failure, otherwise it waits forever
        latch.countDown();
      }

      void closeFile() {
        try {
          fos.close();
        } catch (IOException e) {
          e.printStackTrace();
        }
      }

      void waitForComplete() throws InterruptedException {
        latch.await();
      }
    }

    try {
      // Create a speech synthesizer
      // you can customize the synthesis parameters, like voice, format, sample_rate
      SpeechSynthesisParam.SpeechSynthesisParamBuilder<?, ?> paramBuilder =
          SpeechSynthesisParam.builder().model(model).voice(voice).apiKey(getDashScopeApiKey());
      if (instruction != null && !instruction.isEmpty()) {
        paramBuilder.instruction(instruction);
      }

      ReactCallback callback = new ReactCallback();
      SpeechSynthesizer synthesizer = new SpeechSynthesizer(paramBuilder.build(), callback);

      // Start the synthesizer with Text
      System.out.println("Synthesized text: " + text);
      synthesizer.call(text);
      callback.waitForComplete();

      System.out.println(
          "[Metric] requestId: "
              + synthesizer.getLastRequestId()
              + ", first package delay ms: "
              + synthesizer.getFirstPackageDelay());
    } catch (FileNotFoundException | InterruptedException e) {
      throw new RuntimeException(e);
    }
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
