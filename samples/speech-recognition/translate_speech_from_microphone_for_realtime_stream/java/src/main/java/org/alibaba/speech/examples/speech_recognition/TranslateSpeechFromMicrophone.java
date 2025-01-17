/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package org.alibaba.speech.examples.speech_recognition;

import com.alibaba.dashscope.audio.asr.translation.TranslationRecognizerParam;
import com.alibaba.dashscope.audio.asr.translation.TranslationRecognizerRealtime;
import com.alibaba.dashscope.audio.asr.translation.results.Translation;
import com.alibaba.dashscope.exception.ApiException;
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
 * This demo showcases how to use Alibaba Cloud's DashScope model for recognition from microphone
 * audio input to text Type 'q' to finish recording and recognition.
 */
public class TranslateSpeechFromMicrophone {
  public static String target_language = "en";

  public static void main(String[] args) {
    // set exit flags
    boolean[] shouldExit = {false};
    Object exitFlag = new Object();

    // Start a new thread to record and recognize
    new Thread(
            () -> {
              try {
                startRecordingAndTranslation(exitFlag, shouldExit);
              } catch (Exception e) {
                e.printStackTrace();
                System.exit(0);
              }
            })
        .start();
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

    System.out.println("Press 'Ctrl+C' to stop recording and translation...");
    frame.addKeyListener(
        new KeyAdapter() {
          @Override
          public void keyPressed(KeyEvent e) {
            if (e.isControlDown() && e.getKeyCode() == KeyEvent.VK_C) {
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

  private static void startRecordingAndTranslation(Object exitFlag, boolean[] shouldExit)
      throws ApiException, NoApiKeyException {
    // Create a Flowable<ByteBuffer> for streaming audio data
    Flowable<ByteBuffer> audioSource = createAudioSourceWithControl(exitFlag, shouldExit);
    // 创建Recognizer
    TranslationRecognizerRealtime translator = new TranslationRecognizerRealtime();
    // 创建TranslationRecognizerParam，audioFrames参数中传入上面创建的Flowable<ByteBuffer>
    TranslationRecognizerParam param =
        TranslationRecognizerParam.builder()
            .model("gummy-realtime-v1")
            .format("pcm") // 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you
            // can check the supported formats in the document
            .sampleRate(16000) // supported 8000、16000
            .apiKey(getDashScopeApiKey())
            .transcriptionEnabled(true)
            .translationEnabled(true)
            .translationLanguages(new String[] {target_language})
            .build();

    // Stream call interface for streaming audio to recognizer
    translator
        .streamCall(param, audioSource)
        .blockingForEach(
            result -> {
              if (result.getTranscriptionResult() != null) {
                // 打印最终结果
                if (result.isSentenceEnd()) {
                  System.out.println("Fix: " + result.getTranscriptionResult().getText());
                  System.out.println("Stash: " + result.getTranscriptionResult().getStash());
                } else {
                  System.out.println("Temp Result:" + result.getTranscriptionResult().getText());
                }
              }
              if (result.getTranslationResult() != null) {
                Translation targetTranslation =
                    result.getTranslationResult().getTranslation(target_language);
                if (targetTranslation != null) {
                  if (result.isSentenceEnd()) {
                    System.out.println(
                        "Fix to " + target_language + ": " + targetTranslation.getText());
                    System.out.println(
                        "Stash to " + target_language + ": " + targetTranslation.getStash());
                  } else {
                    System.out.println(
                        "Temp Result:"
                            + result.getTranslationResult().getTranslation("en").getText());
                  }
                }
              }
              if (result.isSentenceEnd()) {
                System.out.println(
                    "\tRequestId: " + result.getRequestId() + " Usage: " + result.getUsage());
              }
            });
    System.out.println("Recognition onComplete! , exit program...");

    System.out.println(
        "[Metric] requestId: "
            + translator.getLastRequestId()
            + ", first package delay ms: "
            + translator.getFirstPackageDelay()
            + ", last package delay ms: "
            + translator.getLastPackageDelay());

    System.exit(0);
  }

  private static Flowable<ByteBuffer> createAudioSourceWithControl(
      Object exitFlag, boolean[] shouldExit) {
    // Create a Flowable<ByteBuffer> for streaming audio data
    return Flowable.create(
        emitter -> {
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
        },
        BackpressureStrategy.BUFFER);
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
