package org.aliyun.bailian;

import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import io.reactivex.BackpressureStrategy;
import io.reactivex.Flowable;

import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.nio.ByteBuffer;
import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.TargetDataLine;
import javax.swing.*;

/**
 * This demo showcases how to use Alibaba Cloud's DashScope model for recognition from microphone audio input to text
 * Type 'q' to finish recording and recognition.
 */
public class RecognitionFromMicrophone {

    public static void main(String[] args) {
        //set exit flags
        boolean[] shouldExit = {false};
        Object exitFlag = new Object();

        // Start a new thread to record and recognize
        new Thread(() -> {
            try {
                startRecordingAndRecognition( exitFlag, shouldExit);
            } catch (NoApiKeyException e) {
                throw new RuntimeException(e);
            }
        }).start();
        // Exit the program
        waitForExitSignal(exitFlag, shouldExit);
    }

    // Wait for exit signal by key press.
    private static void waitForExitSignal(Object exitFlag, boolean[] shouldExit) {

        // Create a hidden JFrame to capture key events
        JFrame frame = new JFrame();
        frame.setUndecorated(true);
        frame.setSize(1, 1);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        System.out.println("Press 'q' then 'Enter' to quit...");
        frame.addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                if (e.getKeyChar() == 'q') {
                    synchronized (exitFlag) {
                        shouldExit[0] = true;
                        exitFlag.notifyAll(); // 通知录音线程退出
                    }
                    System.out.println("Exit signal received. Exiting...");
                }
            }
        });
        frame.setVisible(true);


    }

    private static void startRecordingAndRecognition(Object exitFlag, boolean[] shouldExit) throws NoApiKeyException {
        // Create a Flowable<ByteBuffer> for streaming audio data
        Flowable<ByteBuffer> audioSource = createAudioSourceWithControl(exitFlag, shouldExit);
        // Create speech Recognizer
        Recognition recognizer = new Recognition();
        // Create RecognitionParam, pass the Flowable<ByteBuffer> to audioFrames parameter
        RecognitionParam param = RecognitionParam.builder()
                .model("paraformer-realtime-v1")
                .format("pcm")
                .sampleRate(16000)
                .apiKey(getDashScopeApiKey())
                .build();

        // Stream call interface for streaming audio to recognizer
        recognizer.streamCall(param, audioSource)
                .blockingForEach(result -> {
                    // Subscribe to the output result
                    if (result.isSentenceEnd()) {
                        System.out.println("Final Result: " + result.getSentence().getText());
                    } else {
                        System.out.println("Intermediate Result: " + result.getSentence().getText());
                    }
                });
        System.out.println("Recognition onComplete! , exit program...");
        System.exit(0);
    }

    private static Flowable<ByteBuffer> createAudioSourceWithControl(Object exitFlag, boolean[] shouldExit) {
        // Create a Flowable<ByteBuffer> for streaming audio data
        return Flowable.create(emitter -> {
            try {
                AudioFormat audioFormat = new AudioFormat(16000, 16, 1, true, false);
                TargetDataLine targetDataLine = AudioSystem.getTargetDataLine(audioFormat);
                targetDataLine.open(audioFormat);
                targetDataLine.start();
                ByteBuffer buffer = ByteBuffer.allocate(1024);

                while (!shouldExit[0]) {
                    int read = targetDataLine.read(buffer.array(), 0, buffer.capacity());
                    if (read > 0) {
                        buffer.limit(read);
                        emitter.onNext(buffer);
                        buffer = ByteBuffer.allocate(1024);
                        Thread.sleep(20); // Small delay to control CPU usage
                    }
                    synchronized (exitFlag) {
                        if (shouldExit[0]) {
                            emitter.onComplete();
                            break;
                        }
                    }
                }
            } catch (Exception e) {
                emitter.onError(e);
                System.exit(0);
            }
        }, BackpressureStrategy.BUFFER);
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
