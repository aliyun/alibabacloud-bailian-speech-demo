package org.aliyun.bailian;

import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import com.alibaba.dashscope.utils.Constants;
import java.io.FileNotFoundException;
import org.aliyun.bailian.RealtimeMp3Player;

/**
 * this demo showcases how to use Alibaba Cloud's DashScope model for streaming
 * input synthesis and playback of MP3 audio streams. Note that this demo
 * presents a simplified usage. For adjustments regarding audio format and
 * sample rate, please refer to the documentation.
 */
public class PlaySynthesizedMp3ToSpeakerByStreamingInStreamingOut {
  static RealtimeMp3Player audioPlayer =
      new RealtimeMp3Player(); // use to play mp3
  private static String[] textArray = {"流式文本语音合成SDK，",
      "可以将输入的文本", "合成为语音二进制数据，", "相比于非流式语音合成，",
      "流式合成的优势在于实时性", "更强。用户在输入文本的同时",
      "可以听到接近同步的语音输出，", "极大地提升了交互体验，",
      "减少了用户等待时间。", "适用于调用大规模", "语言模型（LLM），以",
      "流式输入文本的方式", "进行语音合成的场景。"};
  public static void SyncAudioDataToPlayer()
      throws FileNotFoundException, InterruptedException {
    // Set your DashScope API key. More information:
    // https://help.aliyun.com/document_detail/2712195.html in fact,if you have
    // set DASHSCOPE_API_KEY in your environment variable, you can ignore this,
    // and the sdk will automatically get the api_key from the environment
    // variable
    String dashScopeApiKey = null;
    try {
      ApiKey apiKey = new ApiKey();
      dashScopeApiKey = apiKey.getApiKey(null); // from environment variable.
    } catch (NoApiKeyException e) {
      System.out.println("No api key found in environment.");
    }
    if (dashScopeApiKey == null) {
      // if you can not set api_key in your environment variable,
      // you can set it here by code
      dashScopeApiKey = "your-dashscope-api-key";
    }
    // start audio player
    audioPlayer.start();
    class ReactCallback extends ResultCallback<SpeechSynthesisResult> {
      ReactCallback() throws FileNotFoundException {}

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

    SpeechSynthesisParam param =
        SpeechSynthesisParam.builder()
            .model("cosyvoice-v1")
            .voice("longxiaochun")
            .format(SpeechSynthesisAudioFormat.MP3_22050HZ_MONO_256KBPS)
            .apiKey(dashScopeApiKey)
            .build();
    SpeechSynthesizer synthesizer =
        new SpeechSynthesizer(param, new ReactCallback());

    // Start the synthesizer with streaming in text
    for (String text : textArray) {
      synthesizer.streamingCall(text);
      Thread.sleep(100);
    }
    synthesizer.streamingComplete();
  }
  public static void main(String[] args)
      throws FileNotFoundException, InterruptedException {
    SyncAudioDataToPlayer();
  }
}
