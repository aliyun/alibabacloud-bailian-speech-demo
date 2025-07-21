package org.alibaba.speech.examples.omni;

import com.alibaba.dashscope.audio.omni.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.JsonObject;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.TargetDataLine;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.Base64;
import java.util.concurrent.atomic.AtomicReference;
import org.alibaba.speech.utils.RealtimePcmPlayer;


public class OmniServerVad {
    static boolean EnableVisionInput = true;
    public static void main(String[] args) throws InterruptedException, LineUnavailableException {
        String imageB64 = null;
        if (EnableVisionInput) {
            File imageFile = new File("data/cat_480p.jpg");
            byte[] image = new byte[(int) imageFile.length()];
            try {
                FileInputStream fis = new FileInputStream(imageFile);
                fis.read(image);
                fis.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
            imageB64 = Base64.getEncoder().encodeToString(image);
        }

        OmniRealtimeParam param = OmniRealtimeParam.builder()
                .model("qwen-omni-turbo-realtime-latest")
                // .apikey("your-dashscope-api-key")
                .build();

        RealtimePcmPlayer audioPlayer = new RealtimePcmPlayer(24000);

        OmniRealtimeConversation conversation = null;
        final AtomicReference<OmniRealtimeConversation> conversationRef = new AtomicReference<>(null);
        conversation = new OmniRealtimeConversation(param, new OmniRealtimeCallback() {
            @Override
            public void onOpen() {
                System.out.println("connection opened");
            }
            @Override
            public void onEvent(JsonObject message) {
                String type = message.get("type").getAsString();
                switch(type) {
                    case "session.created":
                        System.out.println("start session: " + message.get("session").getAsJsonObject().get("id").getAsString());
                        break;
                    case "conversation.item.input_audio_transcription.completed":
                        System.out.println("question: " + message.get("transcript").getAsString());
                        break;
                    case "response.audio_transcript.delta":
                        System.out.println("got llm response delta: " + message.get("delta").getAsString());
                        break;
                    case "response.audio.delta":
                        String recvAudioB64 = message.get("delta").getAsString();
                        audioPlayer.write(recvAudioB64);
                        break;
                    case "input_audio_buffer.speech_started":
                        System.out.println("======VAD Speech Start======");
                        audioPlayer.cancel();
                        break;
                    case "response.done":
                        System.out.println("======RESPONSE DONE======");
                        if (conversationRef.get() != null) {
                            System.out.println("[Metric] response: " + conversationRef.get().getResponseId() +
                                    ", first text delay: " + conversationRef.get().getFirstTextDelay() +
                                    " ms, first audio delay: " + conversationRef.get().getFirstAudioDelay() + " ms");
                        }
                        break;
                    default:
                        break;
                }
            }
            @Override
            public void onClose(int code, String reason) {
                System.out.println("connection closed code: " + code + ", reason: " + reason);
            }
        });
        conversationRef.set(conversation);
        try {
            conversation.connect();
        } catch (NoApiKeyException e) {
            throw new RuntimeException(e);
        }
        OmniRealtimeConfig config = OmniRealtimeConfig.builder()
                .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
                .voice("Chelsie")
                .enableTurnDetection(true)
                .enableInputAudioTranscription(true)
                .InputAudioTranscription("gummy-realtime-v1")
                .build();
        conversation.updateSession(config);
        long last_photo_time = System.currentTimeMillis();
        try {
            // 创建音频格式
            AudioFormat audioFormat = new AudioFormat(16000, 16, 1, true, false);
            // 根据格式匹配默认录音设备
            TargetDataLine targetDataLine =
                    AudioSystem.getTargetDataLine(audioFormat);
            targetDataLine.open(audioFormat);
            // 开始录音
            targetDataLine.start();
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            long start = System.currentTimeMillis();
            // 录音50s并进行实时转写
            while (System.currentTimeMillis() - start < 50000) {
                int read = targetDataLine.read(buffer.array(), 0, buffer.capacity());
                if (read > 0) {
                    buffer.limit(read);
                    String audioB64 = Base64.getEncoder().encodeToString(buffer.array());
                    // 将录音音频数据发送给流式识别服务
                    conversation.appendAudio(audioB64);
                    if (EnableVisionInput && System.currentTimeMillis() - last_photo_time > 500) {
                        // 每间隔500ms发送一次图片
                        conversation.appendVideo(imageB64);
                        last_photo_time = System.currentTimeMillis();
                    }
                    buffer = ByteBuffer.allocate(1024);
                    // 录音速率有限，防止cpu占用过高，休眠一小会儿
                    Thread.sleep(20);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        conversation.commit();
        conversation.createResponse(null, null);
        conversation.close(1000, "bye");
        audioPlayer.waitForComplete();
        audioPlayer.shutdown();
        System.exit(0);
    }
}
