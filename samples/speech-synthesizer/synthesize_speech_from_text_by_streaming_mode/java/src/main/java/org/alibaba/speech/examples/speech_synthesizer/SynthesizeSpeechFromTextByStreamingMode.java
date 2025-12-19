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
public class SynthesizeSpeechFromTextByStreamingMode {
  // use to play mp3. You need import RealtimeMp3Player.java
  static RealtimeMp3Player audioPlayer = new RealtimeMp3Player();

  public static void main(String[] args) throws FileNotFoundException, NoApiKeyException {

    String textToSynthesize = "想不到时间过得这么快！昨天和你视频聊天，看到你那自豪又满意的笑容，我的心里呀，就如同喝了一瓶蜜一样甜呢！真心为你开心呢！";

    SpeechSynthesisParam param =
        SpeechSynthesisParam.builder()
            .model("cosyvoice-v3-flash")
            .voice("longanhuan")
            .apiKey(getDashScopeApiKey())
            .build();
    System.out.println("init params done");

    // Start the player
    audioPlayer.start();

    class ReactCallback extends ResultCallback<SpeechSynthesisResult> {
      public CountDownLatch latch = new CountDownLatch(1);
      File file = new File("result.mp3");
      FileOutputStream fos = new FileOutputStream(file);

      ReactCallback() throws FileNotFoundException {}

      @Override
      public void onEvent(SpeechSynthesisResult message) {
        // Write Audio to player
        if (message.getAudioFrame() != null) {
          audioPlayer.write(message.getAudioFrame());
          try {
            fos.write(message.getAudioFrame().array());
          } catch (IOException e) {
            throw new RuntimeException(e);
          }
        }
      }

      @Override
      public void onComplete() {
        audioPlayer.stop();
        System.out.println("synthesis onComplete!");
        latch.countDown();
      }

      @Override
      public void onError(Exception e) {
        audioPlayer.stop();
        System.out.println("synthesis onError!");
        e.printStackTrace();
      }

      public void waitForComplete() throws InterruptedException {
        latch.await();
      }
    }
    // Create a speech synthesizer
    ReactCallback callback = new ReactCallback();
    SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, callback);

    // Start the synthesizer with Text
    System.out.printf("start synthesizer : %s \n", textToSynthesize);
    synthesizer.call(textToSynthesize);
    try {
      callback.waitForComplete();
    } catch (InterruptedException e) {
      throw new RuntimeException(e);
    }
    System.out.println(
        "[Metric] requestId: "
            + synthesizer.getLastRequestId()
            + ", first package delay ms: "
            + synthesizer.getFirstPackageDelay());
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
