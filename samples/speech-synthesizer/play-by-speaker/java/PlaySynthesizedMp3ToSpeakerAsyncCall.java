package org.aliyun.bailian;

import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import java.io.FileNotFoundException;

/*
 * This demo showcases how to use Alibaba Cloud's DashScope model for real-time synthesis and playback of MP3 audio streams.
 * Note that this demo presents a simplified usage. For adjustments regarding audio format and sample rate,
 * please refer to the documentation.
 */
public class PlaySynthesizedMp3ToSpeakerAsyncCall {
    // use to play mp3. You need import RealtimeMp3Player.java
    static RealtimeMp3Player audioPlayer = new RealtimeMp3Player();

    public static void main(String[] args) throws FileNotFoundException {
        // Set your DashScope API key. More information: https://help.aliyun.com/document_detail/2712195.html
        // in fact,if you have set DASHSCOPE_API_KEY in your environment variable,
        // you can ignore this, and the sdk will automatically get the api_key from the environment variable
        String dashScopeApiKey = null;

        try {
            ApiKey apiKey = new ApiKey();
            dashScopeApiKey = apiKey.getApiKey(null); // from environment variable.
        } catch (NoApiKeyException e) {
            System.out.println("No api key found in environment.");
        }
        if (dashScopeApiKey == null) {
            //if you can not set api_key in your environment variable,
            //you can set it here by code
            dashScopeApiKey = "your-dashscope-api-key";
        }

        String textToSynthesize = "欢迎体验阿里云百炼大模型语音合成服务！";

        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        .model("cosyvoice-v1")
                        .voice("longxiaochun")
                        .apiKey(dashScopeApiKey)
                        .build();
        System.out.println("init params done");

        // Start the player
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
        // Create a speech synthesizer
        SpeechSynthesizer synthesizer =
                new SpeechSynthesizer(param, new ReactCallback());

        // Start the synthesizer with Text
        System.out.printf("start synthesizer : %s \n", textToSynthesize);
        synthesizer.call(textToSynthesize);
        System.out.print("requestId: " + synthesizer.getLastRequestId());
    }
}
