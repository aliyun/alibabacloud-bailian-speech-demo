package org.alibaba.speech.examples.speech_recognition;

import com.alibaba.dashscope.audio.asr.translation.TranslationRecognizerChat;
import com.alibaba.dashscope.audio.asr.translation.TranslationRecognizerParam;
import com.alibaba.dashscope.audio.asr.translation.results.TranscriptionResult;
import com.alibaba.dashscope.audio.asr.translation.results.Translation;
import com.alibaba.dashscope.audio.asr.translation.results.TranslationRecognizerResult;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import java.io.ByteArrayOutputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.Channels;
import java.nio.channels.WritableByteChannel;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.TargetDataLine;

class TimeUtils {
  private static final DateTimeFormatter formatter =
      DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

  public static String getTimestamp() {
    return LocalDateTime.now().format(formatter);
  }
}

public class OneSentenceTranslateFromMic {
  public static final String TargetLanguage = "en";

  public static void main(String[] args) throws NoApiKeyException, InterruptedException {

    // 创建Recognizer
    TranslationRecognizerChat translator = new TranslationRecognizerChat();
    // 创建RecognitionParam，audioFrames参数中传入上面创建的Flowable<ByteBuffer>
    TranslationRecognizerParam param =
        TranslationRecognizerParam.builder()
            .model("gummy-chat-v1")
            .format("pcm") // 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you
            // can check the supported formats in the document
            .sampleRate(16000) // supported 8000、16000
            .apiKey(getDashScopeApiKey())
            .transcriptionEnabled(true)
            .translationEnabled(true)
            .translationLanguages(new String[] {TargetLanguage})
            .build();

    // 创建一个Flowable<ByteBuffer>
    Thread thread =
        new Thread(
            () -> {
              try {
                // 创建音频格式
                AudioFormat audioFormat = new AudioFormat(16000, 16, 1, true, false);
                // 根据格式匹配默认录音设备
                TargetDataLine targetDataLine = AudioSystem.getTargetDataLine(audioFormat);
                targetDataLine.open(audioFormat);
                // 开始录音
                targetDataLine.start();
                System.out.println("\t[log] Recording...");
                ByteBuffer buffer = ByteBuffer.allocate(1024);
                long start = System.currentTimeMillis();

                // 缓存录音音频
                ByteArrayOutputStream recordAudioStream = new ByteArrayOutputStream();
                WritableByteChannel channel = Channels.newChannel(recordAudioStream);
                // 录音5s并进行实时转写
                while (System.currentTimeMillis() - start < 50000) {
                  int read = targetDataLine.read(buffer.array(), 0, buffer.capacity());
                  if (read > 0) {
                    buffer.limit(read);
                    // 将录音音频数据发送给流式识别服务
                    if (translator.sendAudioFrame(buffer)) {
                      //                                    System.out.println("Send audio frame, "
                      // + start);
                    } else {
                      System.out.println("\t[log] sentence end, stop sending");
                      break;
                    }
                    ByteBuffer savingBuffer = ByteBuffer.allocate(read);
                    savingBuffer.put(buffer.array(), 0, read);
                    savingBuffer.flip();
                    channel.write(savingBuffer);
                    buffer = ByteBuffer.allocate(1024);
                    // 录音速率有限，防止cpu占用过高，休眠一小会儿
                    Thread.sleep(20);
                  }
                }
                // 保存录音音频
                ByteBuffer recordedAudio = ByteBuffer.wrap(recordAudioStream.toByteArray());
                channel.close();
                recordAudioStream.close();
                String outputFileName = translator.getLastRequestId() + "_record.pcm";
                try (FileOutputStream fos = new FileOutputStream(outputFileName)) {
                  fos.write(recordedAudio.array());
                } catch (IOException e) {
                  throw new RuntimeException(e);
                }
                System.out.println("\t[log] Recorded audio saved to " + outputFileName);
              } catch (LineUnavailableException | InterruptedException | IOException e) {
                throw new RuntimeException(e);
              }
            });

    translator.call(
        param,
        new ResultCallback<TranslationRecognizerResult>() {
          public boolean preEndDetected = false;

          @Override
          public void onEvent(TranslationRecognizerResult result) {
            System.out.println("- - - - - - - - - - -");
            if (result.getTranscriptionResult() != null) {
              TranscriptionResult transcriptionResult = result.getTranscriptionResult();
              System.out.printf(
                  "[%s] transcript : %s\n",
                  TimeUtils.getTimestamp(), transcriptionResult.getText());
            }
            if (result.getTranslationResult() != null) {
              Translation translation =
                  result.getTranslationResult().getTranslation(TargetLanguage);
              if (preEndDetected) {
                if (translation.isPreEndFailed()) {
                  System.out.printf(
                      "[%s] <== [vad pre_end failed] ===>\n", TimeUtils.getTimestamp());
                  preEndDetected = false;
                }
              }
              if (translation.isVadPreEnd()) {
                System.out.printf(
                    "[%s] <== [vad pre_end] ===>\n",
                    TimeUtils.getTimestamp(), translation.getPreEndStartTime());
                preEndDetected = true;
              }
              System.out.printf(
                  "[%s] translate to %s: %s\n",
                  TimeUtils.getTimestamp(), TargetLanguage, translation.getText());
            }
            if (result.isSentenceEnd()) {
              System.out.printf(
                  "request id: %s, usage: %s\n", result.getRequestId(), result.getUsage());
            }
          }

          @Override
          public void onComplete() {
            System.out.println("\t[log] Translation complete");
          }

          @Override
          public void onError(Exception e) {}
        });

    System.out.println("\t[log] Translation started, request_id: " + translator.getLastRequestId());

    thread.start();
    thread.join();
    translator.stop();
    System.out.println(
        "[Metric] requestId: "
            + translator.getLastRequestId()
            + ", first package delay ms: "
            + translator.getFirstPackageDelay()
            + ", last package delay ms: "
            + translator.getLastPackageDelay());
    System.exit(0);
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
