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

/**
 * Qwen-Audio-3.0-TTS Text Normalization (TN) Demo
 *
 * <p>Text Normalization is the step that turns "written form" into "spoken form" before acoustic
 * synthesis: digits, units, symbols and abbreviations all have to be expanded into the words a
 * human would actually say. This demo feeds three deliberately hard Chinese passages that are dense
 * with quantities, units, symbols, hotline numbers and polyphonic characters, then prints what to
 * listen for (checkpoints) so you can compare against what you hear.
 */
public class SynthesizeSpeechWithTextNormalization {
  private static final String MODEL = "qwen-audio-3.0-tts-flash";
  private static final String VOICE = "longanfengyue";

  // =========================================================================
  // Test passages and checkpoints
  // =========================================================================
  private static final String[][] CASES = {
    {
      "古代官俸：数量词 + 生僻量词 + 多音字",
      "正一品官，月领禄米150石，俸钱12万文，外加每年绫20匹，罗1匹，绵50两;" + "从九品官，月禄米5石，俸钱8000文，加每年绵12两。",
      "150石→一百五十石(dàn), 12万文→十二万文, 1匹→一匹, 8000文→八千文"
    },
    {
      "医药检测：百分号 + 波浪范围符 + 单位",
      "在一次检测中，1毫升20%甘露醇药液中可查出粒径4～30微米的微粒598个。",
      "20%→百分之二十, 4～30微米→四到三十微米, 598个→五百九十八个"
    },
    {
      "服务热线：号码逐位读 + 时间量",
      "965113供水服务热线24小时受理用户来电、来访、报修、报漏、投诉，" + "做到用户反映的问题件件有落实、件件有反馈。",
      "965113→九六五一一三(逐位), 24小时→二十四小时"
    }
  };

  public static void main(String[] args) {
    System.out.println("======================================================================");
    System.out.println(" Qwen-Audio-3.0-TTS 文本正则化（TN）能力演示");
    System.out.println(" 以下 3 段文本密集包含数量词、单位、符号、号码与多音字，");
    System.out.println(" 请边听边对照每段列出的检查点。");
    System.out.println("======================================================================");

    for (int i = 0; i < CASES.length; i++) {
      String name = CASES[i][0];
      String text = CASES[i][1];
      String checkpoints = CASES[i][2];
      String outputFile = "result_tn_" + (i + 1) + ".mp3";

      System.out.println("\n[" + (i + 1) + "] " + name);
      System.out.println("  原文: " + text);
      System.out.println("  检查点: " + checkpoints);

      synthesize(text, outputFile);
    }

    System.out.println("\n======================================================================");
    System.out.println(" 全部完成，生成的 mp3 文件可反复回听比对。");
    System.out.println("======================================================================");
    System.exit(0);
  }

  private static void synthesize(String text, String outputFile) {
    RealtimeMp3Player audioPlayer = new RealtimeMp3Player();
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
        closeFile();
        latch.countDown();
      }

      @Override
      public void onError(Exception e) {
        audioPlayer.stop();
        System.out.println("  [ERROR] " + e.getMessage());
        closeFile();
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
      SpeechSynthesisParam param =
          SpeechSynthesisParam.builder()
              .model(MODEL)
              .voice(VOICE)
              .apiKey(getDashScopeApiKey())
              .build();

      ReactCallback callback = new ReactCallback();
      SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, callback);
      synthesizer.call(text);
      callback.waitForComplete();

      System.out.println(
          "  requestId: "
              + synthesizer.getLastRequestId()
              + ", first_package_delay: "
              + synthesizer.getFirstPackageDelay()
              + "ms");
      System.out.println("  saved to: " + outputFile);
    } catch (FileNotFoundException | InterruptedException e) {
      throw new RuntimeException(e);
    }
  }

  private static String getDashScopeApiKey() {
    String dashScopeApiKey = null;
    try {
      ApiKey apiKey = new ApiKey();
      dashScopeApiKey = apiKey.getApiKey(null);
    } catch (NoApiKeyException e) {
      System.out.println("No API key found in environment.");
    }
    if (dashScopeApiKey == null) {
      dashScopeApiKey = "your-dashscope-api-key";
    }
    return dashScopeApiKey;
  }
}
