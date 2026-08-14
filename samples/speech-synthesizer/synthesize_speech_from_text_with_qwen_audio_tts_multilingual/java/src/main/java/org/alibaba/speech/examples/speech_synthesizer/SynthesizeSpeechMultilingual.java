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
import java.util.Arrays;
import java.util.concurrent.CountDownLatch;
import org.alibaba.speech.utils.RealtimeMp3Player;

/**
 * Qwen-Audio-3.0-TTS All-in-One Multilingual Speech Synthesis Demo
 *
 * <p>The {@code longanhuan_mtlv7} voice is an all-in-one multilingual voice: one single voice id
 * speaks 16 languages. This demo walks through all of them with the same greeting, so you can hear
 * one voice switch languages back to back while the timbre stays consistent.
 *
 * <p>Two parameters drive the language selection:
 *
 * <ul>
 *   <li>{@code languageHints} — tells the model which language the input text is in
 *   <li>{@code instruction} — explicitly asks the model to speak that language (required for all
 *       languages except Chinese and English)
 * </ul>
 */
public class SynthesizeSpeechMultilingual {
  private static final String MODEL = "qwen-audio-3.0-tts-flash";
  private static final String VOICE = "longanhuan_mtlv7";

  // Each row: { lid, displayName, instruction (null for zh/en), sampleText }
  private static final String[][] LANGUAGES = {
    {"zh", "中文", null, "你好，欢迎使用阿里云百炼语音合成服务。"},
    {
      "en",
      "English",
      null,
      "Hello, welcome to the Alibaba Cloud Model Studio speech synthesis service."
    },
    {"ja", "日本語", "请讲日语。", "こんにちは、アリババクラウドの音声合成サービスへようこそ。"},
    {"ko", "한국어", "请讲韩语。", "안녕하세요, 알리바바 클라우드 음성 합성 서비스에 오신 것을 환영합니다."},
    {
      "fr", "Français", "请讲法语。", "Bonjour, bienvenue au service de synthèse vocale d'Alibaba Cloud."
    },
    {"de", "Deutsch", "请讲德语。", "Hallo, willkommen beim Sprachsynthese-Service von Alibaba Cloud."},
    {
      "ru",
      "Русский",
      "请讲俄语。",
      "Здравствуйте, добро пожаловать в сервис синтеза речи Alibaba Cloud."
    },
    {
      "it", "Italiano", "请讲意大利语。", "Ciao, benvenuto al servizio di sintesi vocale di Alibaba Cloud."
    },
    {
      "es",
      "Español",
      "请讲西班牙语。",
      "Hola, bienvenido al servicio de síntesis de voz de Alibaba Cloud."
    },
    {"pt", "Português", "请讲葡萄牙语。", "Olá, bem-vindo ao serviço de síntese de voz da Alibaba Cloud."},
    {"ar", "العربية", "请讲阿拉伯语。", "مرحبًا، أهلاً بك في خدمة تحويل النص إلى كلام من علي بابا كلاود."},
    {"th", "ไทย", "请讲泰语。", "สวัสดีค่ะ ยินดีต้อนรับสู่บริการสังเคราะห์เสียงของอาลีบาบาคลาวด์"},
    {
      "vi",
      "Tiếng Việt",
      "请讲越南语。",
      "Xin chào, chào mừng bạn đến với dịch vụ tổng hợp giọng nói của Alibaba Cloud."
    },
    {
      "id",
      "Bahasa Indonesia",
      "请讲印尼语。",
      "Halo, selamat datang di layanan sintesis suara Alibaba Cloud."
    },
    {
      "ms",
      "Bahasa Melayu",
      "请讲马来语。",
      "Helo, selamat datang ke perkhidmatan sintesis pertuturan Alibaba Cloud."
    },
    {
      "tl",
      "Filipino",
      "请讲菲律宾语。",
      "Kumusta, maligayang pagdating sa serbisyo ng speech synthesis ng Alibaba Cloud."
    },
  };

  public static void main(String[] args) {
    System.out.println("======================================================================");
    System.out.println(" All-in-One 多语言语音合成：单一音色 " + VOICE + " 连说 " + LANGUAGES.length + " 种语言");
    System.out.println(" 请留意切换语种时，说话人的音色始终保持一致。");
    System.out.println("======================================================================");

    for (int i = 0; i < LANGUAGES.length; i++) {
      String lid = LANGUAGES[i][0];
      String name = LANGUAGES[i][1];
      String instruction = LANGUAGES[i][2];
      String text = LANGUAGES[i][3];
      String outputFile = "result_" + lid + ".mp3";

      System.out.println("\n[" + (i + 1) + "/" + LANGUAGES.length + "] " + name + " (" + lid + ")");
      System.out.println("  instruction: " + instruction);
      System.out.println("  text: " + text);

      synthesize(text, lid, instruction, outputFile);
    }

    System.out.println("\n======================================================================");
    System.out.println(" 全部完成，生成的 mp3 文件可用于对比同一音色在各语种下的表现。");
    System.out.println("======================================================================");
    System.exit(0);
  }

  private static void synthesize(String text, String lid, String instruction, String outputFile) {
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
      SpeechSynthesisParam.SpeechSynthesisParamBuilder<?, ?> paramBuilder =
          SpeechSynthesisParam.builder()
              .model(MODEL)
              .voice(VOICE)
              .languageHints(Arrays.asList(lid))
              .apiKey(getDashScopeApiKey());

      if (instruction != null) {
        paramBuilder.instruction(instruction);
      }

      ReactCallback callback = new ReactCallback();
      SpeechSynthesizer synthesizer = new SpeechSynthesizer(paramBuilder.build(), callback);
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
