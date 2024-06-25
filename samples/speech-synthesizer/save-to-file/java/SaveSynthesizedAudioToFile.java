package org.aliyun.bailian;

import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;

/**
 * this demo showcases how to use Alibaba Cloud's DashScope model for real-time synthesis and saving MP3 audio to file.
 */
public class SaveSynthesizedAudioToFile {
    public static void SyncAudioDataToFile() {
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
                        .format(SpeechSynthesisAudioFormat.MP3_22050HZ_MONO_256KBPS)
                        .apiKey(dashScopeApiKey)
                        .build();

        // Create a speech synthesizer
        SpeechSynthesizer synthesizer = new SpeechSynthesizer(param,null);

        File file = new File("output.mp3");
        // use call methods to get audio data
        ByteBuffer audio = synthesizer.call(textToSynthesize);
        try (FileOutputStream fos = new FileOutputStream(file)) {
            fos.write(audio.array());
            System.out.println("synthesis done!");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static void main(String[] args) {
        SyncAudioDataToFile();
        System.exit(0);
    }
}
