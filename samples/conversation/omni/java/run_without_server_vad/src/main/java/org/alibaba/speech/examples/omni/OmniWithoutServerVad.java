package org.alibaba.speech.examples.omni;

import com.alibaba.dashscope.audio.omni.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.JsonObject;

import javax.sound.sampled.LineUnavailableException;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.Base64;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicReference;

import org.alibaba.speech.utils.RealtimePcmPlayer;

public class OmniWithoutServerVad {

    public static void main(String[] args) throws InterruptedException, LineUnavailableException {
        File audioFile = new File("data/q1_16khz.pcm");
        OmniRealtimeParam param = OmniRealtimeParam.builder()
                .model("qwen-omni-turbo-realtime-latest")
                // .apikey("your-dashscope-api-key")
                .build();
        AtomicReference<CountDownLatch> responseDoneLatch = new AtomicReference<>(null);
        responseDoneLatch.set(new CountDownLatch(1));

        RealtimePcmPlayer audioPlayer = new RealtimePcmPlayer(24000);
        final AtomicReference<OmniRealtimeConversation> conversationRef = new AtomicReference<>(null);
        OmniRealtimeConversation conversation = new OmniRealtimeConversation(param, new OmniRealtimeCallback() {
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
                    case "response.done":
                        System.out.println("======RESPONSE DONE======");
                        if (conversationRef.get() != null) {
                            System.out.println("[Metric] response: " + conversationRef.get().getResponseId() +
                                    ", first text delay: " + conversationRef.get().getFirstTextDelay() +
                                    " ms, first audio delay: " + conversationRef.get().getFirstAudioDelay() + " ms");
                        }
                        responseDoneLatch.get().countDown();
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
                .enableTurnDetection(false)
                .build();
        conversation.updateSession(config);

        try {
            FileInputStream fis = new FileInputStream(audioFile);
            byte[] buffer = new byte[3200];
            int bytesRead;
            // Loop to read chunks of the file
            while ((bytesRead = fis.read(buffer)) != -1) {
                ByteBuffer byteBuffer;
                if (bytesRead < buffer.length) {
                    byteBuffer = ByteBuffer.wrap(buffer, 0, bytesRead);
                } else {
                    byteBuffer = ByteBuffer.wrap(buffer);
                }
                // Send the ByteBuffer to the recognition instance
                String audioB64 = Base64.getEncoder().encodeToString(byteBuffer.array());
                conversation.appendAudio(audioB64);
                Thread.sleep(100);
                buffer = new byte[3200];
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        conversation.commit();
        conversation.createResponse(null, null);
        // wait until response is done.
        responseDoneLatch.get().await();
        conversation.close(1000, "bye");
        audioPlayer.waitForComplete();
        audioPlayer.shutdown();
        System.exit(0);
    }
}
