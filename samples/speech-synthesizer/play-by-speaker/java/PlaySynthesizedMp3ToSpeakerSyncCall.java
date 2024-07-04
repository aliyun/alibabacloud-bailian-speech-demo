package org.aliyun.bailian;

import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import java.nio.ByteBuffer;

// This demo showcases how to use Alibaba Cloud's DashScope model for real-time synthesis and playback of MP3 audio streams.
public class PlaySynthesizedMp3ToSpeakerSyncCall {
    static RealtimeMp3Player audioPlayer = new RealtimeMp3Player(); // use to play mp3

    public static void main(String[] args) {
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

        // set speech synthesis params
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        .model("cosyvoice-v1")
                        .voice("longxiaochun")
                        .apiKey(dashScopeApiKey)
                        .build();
        System.out.println("init params done");

        // Create a speech synthesizer
        SpeechSynthesizer synthesizer = new SpeechSynthesizer(param,null);

        String textToSynthesize = "欢迎体验阿里云百炼大模型语音合成服务！";


        // Start the synthesizer with Text
        ByteBuffer audio = synthesizer.call(textToSynthesize);
        System.out.print("requestId: " + synthesizer.getLastRequestId());
        System.out.printf("start synthesizer : %s \n", textToSynthesize);
        // Start the player
        audioPlayer.start();
        // Write the audio data to the player
        audioPlayer.write(audio);
        // Finish audio feed to the player
        audioPlayer.stop();

    }
}
