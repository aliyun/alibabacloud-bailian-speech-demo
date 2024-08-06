/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package org.aliyun.bailian;

import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;

import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;

// This demo showcases how to use Alibaba Cloud's DashScope model for real-time synthesis and playback of MP3 audio streams.
public class SynthesizeSpeechFromText {
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
                        .voice("loongstella")
                        .apiKey(dashScopeApiKey)
                        .build();
        System.out.println("init params done");

        // Create a speech synthesizer
        SpeechSynthesizer synthesizer = new SpeechSynthesizer(param,null);

        String textToSynthesize = "想不到时间过得这么快！昨天和你视频聊天，看到你那自豪又满意的笑容，我的心里呀，就如同喝了一瓶蜜一样甜呢！真心为你开心呢！";

        // Start the synthesizer with Text
        System.out.printf("start synthesizer : %s \n", textToSynthesize);
        ByteBuffer audio = synthesizer.call(textToSynthesize);
        try (FileOutputStream fos = new FileOutputStream("result.mp3")) {
            fos.write(audio.array());
            System.out.println("synthesis done!");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        System.out.print("requestId: " + synthesizer.getLastRequestId());
        System.exit(0);
    }
}
