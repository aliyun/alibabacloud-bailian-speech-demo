package org.alibaba.speech.examples.omni;

import com.alibaba.dashscope.audio.omni.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.JsonObject;
import org.java_websocket.WebSocket;
import org.java_websocket.handshake.ClientHandshake;
import org.java_websocket.server.WebSocketServer;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.TargetDataLine;
import java.net.InetSocketAddress;
import java.net.UnknownHostException;
import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.Base64;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicReference;
import org.alibaba.speech.utils.RealtimePcmPlayer;


class WsktUtil extends WebSocketServer {
    private static List<WebSocket> clients = new CopyOnWriteArrayList<>();
    private AtomicReference<String> imageFrameB64 = new AtomicReference<>();

    public WsktUtil() throws UnknownHostException {
        super(new InetSocketAddress(5000)); // 指定端口为 8843
    }

    @Override
    public void onOpen(WebSocket conn, ClientHandshake handshake) {
        System.out.println("客户端已连接");
        clients.add(conn);
    }

    @Override
    public void onMessage(WebSocket conn, String message) {
        System.out.println("收到文本消息: " + message);
        // 可以在此处添加消息处理逻辑
    }

    @Override
    public void onMessage(WebSocket conn, ByteBuffer message) {
        super.onMessage(conn, message);
        imageFrameB64.set(Base64.getEncoder().encodeToString(message.array()));
//        System.out.println("收到图片");
    }

    @Override
    public void onClose(WebSocket conn, int code, String reason, boolean remote) {
        System.out.println("客户端已断开连接");
        clients.remove(conn);
    }

    @Override
    public void onError(WebSocket conn, Exception ex) {
        ex.printStackTrace();
    }

    @Override
    public void onStart() {
        System.out.println("WebSocket 服务器启动成功！");
    }

    public String getImageFrameB64() {
        return imageFrameB64.get();
    }
}


public class OmniWithCamera {
    static boolean EnableVisionInput = true;

    public static void main(String[] args) throws InterruptedException, LineUnavailableException, UnknownHostException {


        OmniRealtimeParam param = OmniRealtimeParam.builder()
                .model("qwen-omni-turbo-realtime-latest")
                // .apikey("your-dashscope-api-key")
                .build();

        WsktUtil server = new WsktUtil();
        server.start();
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
                        String imageB64 = server.getImageFrameB64();
                        if (imageB64 != null) {
                            conversation.appendVideo(imageB64);
                            last_photo_time = System.currentTimeMillis();
                        }
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
