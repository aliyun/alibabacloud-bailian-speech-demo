/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package org.alibaba.speech.examples.speech_synthesizer;

import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.audio.ttsv2.enrollment.Voice;
import com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentService;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.concurrent.CountDownLatch;
import org.alibaba.speech.utils.RealtimeMp3Player;

/*
 * This demo showcases how to clone your voice by Alibaba Cloud's DashScope model, then synthesize
 * and play MP3 audio streams in real-time with the cloned voice.
 * Note that this demo presents a simplified usage. For adjustments regarding audio format and sample rate,
 * please refer to the documentation.
 */
public class CloneVoiceByQwenAudioTTSModel {
  // supported models : 'qwen-audio-3.0-tts-flash'、'qwen-audio-3.0-tts-plus'
  // the voice enrollment and the speech synthesis must use the same model
  private static final String MODEL = "qwen-audio-3.0-tts-flash";

  // the prefix of your cloned voice name
  private static final String PREFIX = "demo";

  public static void main(String[] args) throws NoApiKeyException, InputRequiredException {
    // we presume you have already recorded audio and get the downloadable url.
    // the url must be accessible from the public network.
    String audioUrl =
        "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/cosyvoice/210024_happy.wav";
    if (args.length > 0) {
      audioUrl = args[0];
    }

    String textToSynthesize = "今天的天气真不错！我们一起出去玩吧！";

    // you can either synthesize text with a new cloned voice
    Voice yourClonedVoice = createCloneVoice(audioUrl, PREFIX, MODEL);
    // or use the voice id which has been created before
    // String voiceId = "qwen-audio-demo-xxxxxx";
    synthesisTextToSpeechAndPlay(
        textToSynthesize, yourClonedVoice.getVoiceId(), MODEL, "result.mp3");

    // you can delete the voices filtered by prefix
    // deleteVoiceByPrefix(PREFIX);

    System.exit(0);
  }

  /** Clone a new voice with the given audio, and return the new voice. */
  public static Voice createCloneVoice(String audioUrl, String prefix, String model)
      throws NoApiKeyException, InputRequiredException {
    VoiceEnrollmentService service = new VoiceEnrollmentService(getDashScopeApiKey());
    System.out.println("start cloning your voice...");
    Voice newVoice = service.createVoice(model, prefix, audioUrl);
    System.out.println("requestId: " + service.getLastRequestId());
    System.out.println("voice clone done.");
    System.out.println("your new voice is: " + newVoice.getVoiceId());

    Voice[] voicesList = service.listVoice(prefix, 0, 10);
    System.out.println("requestId: " + service.getLastRequestId());
    System.out.println("your current voices list:");
    for (Voice voice : voicesList) {
      System.out.println(voice);
    }
    return newVoice;
  }

  /** Delete the voices filtered by prefix, to avoid occupying your voice quota. */
  public static void deleteVoiceByPrefix(String prefix)
      throws NoApiKeyException, InputRequiredException {
    VoiceEnrollmentService service = new VoiceEnrollmentService(getDashScopeApiKey());
    Voice[] voicesList = service.listVoice(prefix);
    for (Voice voice : voicesList) {
      service.deleteVoice(voice.getVoiceId());
      System.out.println("requestId: " + service.getLastRequestId());
      System.out.println("voice " + voice + " deleted");
    }
  }

  /**
   * Synthesize speech with your cloned voice, play the synthesized audio in real-time and save it
   * into outputFile.
   */
  public static void synthesisTextToSpeechAndPlay(
      String text, String voice, String model, String outputFile) {
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
      SpeechSynthesisParam param =
          SpeechSynthesisParam.builder()
              .model(model)
              .voice(voice)
              .apiKey(getDashScopeApiKey())
              .build();

      ReactCallback callback = new ReactCallback();
      SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, callback);

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
