package org.alibaba.speech.examples.speech_synthesizer;

import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
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
import org.alibaba.speech.utils.RealtimeMp3Player;

public class CloneVoiceAndSynthesisTextAndPlay {

  static RealtimeMp3Player audioPlayer = new RealtimeMp3Player(); // use to play mp3
  private static String[] textArray = {"你好，欢迎使用阿里巴巴通义语音实验室的音色复刻服务～"};

  public static void SyncAudioDataToPlayer(String yourVoice)
      throws FileNotFoundException, InterruptedException, NoApiKeyException {
    // Set your DashScope API key. More information:
    // https://help.aliyun.com/document_detail/2712195.html
    // in fact,if you have set DASHSCOPE_API_KEY in your environment variable,
    // you can ignore this, and the sdk will automatically get the api_key from the environment
    // variable
    // start audio player
    audioPlayer.start();
    class ReactCallback extends ResultCallback<SpeechSynthesisResult> {
      FileOutputStream fos;

      ReactCallback() throws FileNotFoundException {
        File file = new File("output.mp3");
        fos = new FileOutputStream(file);
      }

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
        try {
          fos.close();
        } catch (IOException e) {
          throw new RuntimeException(e);
        }
        System.out.println("synthesis onComplete!");
      }

      @Override
      public void onError(Exception e) {
        audioPlayer.stop();
        System.out.println("synthesis onError!");
        e.printStackTrace();
      }
    }

    String model = "cosyvoice-v3-flash";
    SpeechSynthesisParam param =
        SpeechSynthesisParam.builder()
            .model(model)
            .voice(yourVoice)
            .format(SpeechSynthesisAudioFormat.MP3_22050HZ_MONO_256KBPS)
            .apiKey(getDashScopeApiKey())
            .build();

    SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, new ReactCallback());

    // Start the synthesizer with streaming in text
    System.out.printf("Start Synthesis Text: ");
    for (String text : textArray) {
      System.out.printf(text);
      synthesizer.streamingCall(text);
      Thread.sleep(100);
    }
    System.out.printf("\n");
    try {
      synthesizer.streamingComplete();
    } catch (RuntimeException e) {
      System.out.println("recv runtime error " + e);
    }
    System.out.println(
        "[Metric] requestId: "
            + synthesizer.getLastRequestId()
            + ", first package delay ms: "
            + synthesizer.getFirstPackageDelay());
  }

  public static Voice CreateCloneVoice(String audioUrl)
      throws NoApiKeyException, InputRequiredException {
    VoiceEnrollmentService service = new VoiceEnrollmentService(getDashScopeApiKey());
    System.out.println("Start Cloning Your Voice...");
    Voice new_voice = service.createVoice("cosyvoice-v3-flash", "demo", audioUrl);
    System.out.println("request_Id: " + service.getLastRequestId());
    System.out.println("Voice Clone Done.");
    System.out.println("your new voice is " + new_voice.getVoiceId());
    Voice[] voices_list = service.listVoice("demo", 0, 10);
    System.out.println("request_Id: " + service.getLastRequestId());
    System.out.println("your current voices list:");
    for (Voice voice : voices_list) {
      System.out.println(voice);
    }
    return new_voice;
  }

  public static void DeleteVoiceByPrefix(String prefix)
      throws NoApiKeyException, InputRequiredException {
    VoiceEnrollmentService service = new VoiceEnrollmentService(getDashScopeApiKey());
    Voice[] voices_list = service.listVoice(prefix);
    for (Voice voice : voices_list) {
      service.deleteVoice(voice.getVoiceId());
      System.out.println("request_Id: " + service.getLastRequestId());
      System.out.println("voice " + voice + " deleted");
    }
  }

  public static void main(String[] args)
      throws FileNotFoundException, InterruptedException, NoApiKeyException,
          InputRequiredException {
    String audioUrl =
        "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/cosyvoice/210024_happy.wav";
    Voice yourClonedVoice = CreateCloneVoice(audioUrl);
    SyncAudioDataToPlayer(yourClonedVoice.getVoiceId());
    // DeleteVoiceByPrefix("demo");
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
