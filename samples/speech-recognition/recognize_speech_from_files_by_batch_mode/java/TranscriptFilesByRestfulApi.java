/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package org.aliyun.bailian;
import com.alibaba.dashscope.audio.asr.transcription.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import com.google.gson.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.*;
import java.net.HttpURLConnection;
import java.util.Arrays;
import java.util.List;

public class TranscriptFilesByRestfulApi {

    public static void main(String[] args) throws NoApiKeyException {
        // create transcription params, use getDashScopeApiKey to get api key.
        TranscriptionParam param =
            TranscriptionParam.builder()
            .apiKey("your-dashscope-api-key")
            .model("paraformer-v1") // 'paraformer-8k-v1', 'paraformer-mtl-v1'
            .fileUrls(
                Arrays.asList(
                "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_example_1.wav",
                "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/sample_video_poetry.mp4",
                "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/long_audio_demo_cn.mp3")
            .build();
        try {
            Transcription transcription = new Transcription();
            // post request to transcribe service
            TranscriptionResult result = transcription.asyncCall(param);
            // waiting for transcription finish
            result =
                    transcription.wait(
                            TranscriptionQueryParam.FromTranscriptionParam(param, result.getTaskId()));
            // get Transcription result after waiting
            List<TranscriptionTaskResult> taskResultList = result.getResults();
            if (taskResultList != null && !taskResultList.isEmpty()) {
                for (TranscriptionTaskResult taskResult : taskResultList) {
                    // get Transcription rersult url
                    String transcriptionUrl = taskResult.getTranscriptionUrl();
                    // get transcription result by http get
                    HttpURLConnection connection =
                            (HttpURLConnection) new URL(transcriptionUrl).openConnection();
                    connection.setRequestMethod("GET");
                    connection.connect();
                    BufferedReader reader =
                            new BufferedReader(new InputStreamReader(connection.getInputStream()));
                    // format json print
                    Gson gson = new GsonBuilder().setPrettyPrinting().create();
                    System.out.println(gson.toJson(gson.fromJson(reader, JsonObject.class)));
                }

            }
        } catch (Exception e) {
            System.out.println("error: " + e);
        }
        System.exit(0);
    }

    /**
     * Set your DashScope API key. More information: <a href="https://help.aliyun.com/document_detail/2712195.html">...</a>
     * In fact, if you have set DASHSCOPE_API_KEY in your environment variable,
     * you can ignore this, and the SDK will automatically get the api_key from the environment variable
     * */
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
