package org.example.recognition;

import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionResult;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;

import java.io.FileInputStream;
import java.nio.ByteBuffer;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;


class RealtimeRecognizeTask implements Runnable {
    private Path filepath;

    public RealtimeRecognizeTask(Path filepath) {
        this.filepath = filepath;
    }

    /**
     * Set your DashScope API key. More information: <a
     * href="https://help.aliyun.com/document_detail/2712195.html">...</a> In
     * fact, if you have set DASHSCOPE_API_KEY in your environment variable, you
     * can ignore this, and the SDK will automatically get the api_key from the
     * environment variable
     * */
    private static String getDashScopeApiKey() throws NoApiKeyException {
        String dashScopeApiKey = null;
        try {
            ApiKey apiKey = new ApiKey();
            dashScopeApiKey =
                    apiKey.getApiKey(null); // Retrieve from environment variable.
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

    @Override
    public void run() {
        // Create recognition params
        // you can customize the recognition parameters, like model, format,
        // sample_rate for more information, please refer to
        // https://help.aliyun.com/document_detail/2712536.html
        RecognitionParam param =
                null;
        try {
            param = RecognitionParam.builder()
                    .model("paraformer-realtime-v1")
                    .format("pcm") // 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you
                    // can check the supported formats in the document
                    .sampleRate(16000) // supported 8000、16000
                    .apiKey(
                            getDashScopeApiKey()) // use getDashScopeApiKey to get api key.
                    .build();
        } catch (NoApiKeyException e) {
            throw new RuntimeException(e);
        }
        Recognition recognizer = new Recognition();
        CountDownLatch latch = new CountDownLatch(1);

        String threadName = Thread.currentThread().getName();

        ResultCallback<RecognitionResult> callback =
                new ResultCallback<RecognitionResult>() {
                    @Override
                    public void onEvent(RecognitionResult message) {
                        if (message.isSentenceEnd()) {
                            System.out.println("[" + threadName + "] Fix:" + message.getSentence().getText());
                        } else {
                            System.out.println("[" + threadName + "] Result: " + message.getSentence().getText());
                        }
                    }

                    @Override
                    public void onComplete() {
                        System.out.println("[" + threadName + "] Recognition complete");
                        latch.countDown();
                    }

                    @Override
                    public void onError(Exception e) {
                        System.out.println("[" + threadName + "] RecognitionCallback error: " + e.getMessage());
                    }
                };
        // set param & callback
        recognizer.call(param, callback);
        // Please replace the path with your audio file path
        System.out.println("[" + threadName + "] Input file_path is: " + this.filepath);
        // Read file and send audio by chunks
        try (FileInputStream fis = new FileInputStream(this.filepath.toFile())) {
            // chunk size set to 10 seconds for 16KHz sample rate
            byte[] buffer = new byte[32000 * 10];
            int bytesRead;
            // Loop to read chunks of the file
            while ((bytesRead = fis.read(buffer)) != -1) {
                ByteBuffer byteBuffer;
                // Handle the last chunk which might be smaller than the buffer size
                System.out.println("[" + threadName + "] bytesRead: " + bytesRead);
                if (bytesRead < buffer.length) {
                    byteBuffer = ByteBuffer.wrap(buffer, 0, bytesRead);
                } else {
                    byteBuffer = ByteBuffer.wrap(buffer);
                }
                // Send the ByteBuffer to the recognition instance
                recognizer.sendAudioFrame(byteBuffer);
            }
            System.out.println(LocalDateTime.now());
        } catch (Exception e) {
            e.printStackTrace();
        }

        recognizer.stop();
        // wait for the recognition to complete
        try {
            latch.await();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

}


public class RecognizeSpeechFromFilesByRealtimeMode {
    public static void main(String[] args)
            throws NoApiKeyException, InterruptedException {
        String currentDir = System.getProperty("user.dir");
        // Please replace the path with your audio source
        Path[] filePaths = {
                Paths.get(currentDir, "hello_world_male_16k_16bit_mono.wav"),
                Paths.get(currentDir, "hello_world_male_16k_16bit_mono.wav"),
                Paths.get(currentDir, "hello_world_male_16k_16bit_mono.wav"),
        };
        // Use ThreadPool to run recognition tasks
        ExecutorService executorService = Executors.newFixedThreadPool(10);
        for (Path filepath:filePaths) {
            executorService.submit(new RealtimeRecognizeTask(filepath));
        }
        executorService.shutdown();
        // wait for all tasks to complete
        executorService.awaitTermination(1, TimeUnit.MINUTES);
        System.exit(0);
    }


}