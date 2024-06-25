package org.aliyun.bailian;

import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;
import java.io.FileNotFoundException;
import java.util.Arrays;

/**
 * this demo showcases how to use Alibaba Cloud's DashScope model for synthesis
 * llm streaming output text and playback of MP3 audio streams. Note that this
 * demo presents a simplified usage. For adjustments regarding audio format and
 * sample rate, please refer to the documentation.
 */
public class PlayLLMTextToSpeakerByStreamingInStreamingOut {
  static RealtimeMp3Player audioPlayer =
      new RealtimeMp3Player(); // use to play mp3
  public static void LLMTextToPlayer()
      throws NoApiKeyException, InputRequiredException {
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

    /*******  Call the Generative AI Model to get streaming text *******/
    // Prepare for the LLM call
    Generation gen = new Generation();
    Message userMsg = Message.builder()
                          .role(Role.USER.getValue())
                          .content("请介绍一下你自己")
                          .build();
    GenerationParam genParam =
        GenerationParam.builder()
            .apiKey(dashScopeApiKey)
            .model("qwen-turbo")
            .messages(Arrays.asList(userMsg))
            .resultFormat(GenerationParam.ResultFormat.MESSAGE)
            .topP(0.8)
            .incrementalOutput(true)
            .build();

    // Prepare the speech synthesis task
    SpeechSynthesisParam param =
        SpeechSynthesisParam.builder()
            .model("cosyvoice-v1")
            .voice("longxiaochun")
            .format(SpeechSynthesisAudioFormat.MP3_22050HZ_MONO_256KBPS)
            .apiKey(dashScopeApiKey)
            .build();
    SpeechSynthesizer synthesizer =
        new SpeechSynthesizer(param, new ReactCallback());

    // Get LLM result stream
    Flowable<GenerationResult> result = gen.streamCall(genParam);
    result.blockingForEach(message -> {
      String text =
          message.getOutput().getChoices().get(0).getMessage().getContent();
      System.out.println("LLM output：" + text);
      // send llm result to synthesizer
      synthesizer.streamingCall(text);
    });
    synthesizer.streamingComplete();
  }
  public static void main(String[] args)
      throws FileNotFoundException, InterruptedException, NoApiKeyException,
             InputRequiredException {
    LLMTextToPlayer();
  }
}
