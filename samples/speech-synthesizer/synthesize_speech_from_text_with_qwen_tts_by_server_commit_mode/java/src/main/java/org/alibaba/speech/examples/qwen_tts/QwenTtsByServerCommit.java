package org.alibaba.speech.examples.qwen_tts;

import com.alibaba.dashscope.audio.qwen_tts_realtime.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.JsonObject;
import org.alibaba.speech.utils.RealtimePcmPlayer;

import javax.sound.sampled.LineUnavailableException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicReference;

public class QwenTtsByServerCommit {
    static String[] textToSynthesize = {
        "对吧~我就特别喜欢这种超市",
        "尤其是过年的时候",
        "去逛超市",
        "就会觉得",
        "超级超级开心！",
        "想买好多好多的东西呢！"
    };
    public static void main(String[] args) throws InterruptedException, LineUnavailableException {

        QwenTtsRealtimeParam param = QwenTtsRealtimeParam.builder()
                .model("qwen-tts-realtime")
                // .apikey("your-api-key")
                .build();

        RealtimePcmPlayer audioPlayer = new RealtimePcmPlayer(24000);

        AtomicReference<CountDownLatch> completeLatch = new AtomicReference<>(new CountDownLatch(1));

        QwenTtsRealtime qwenTtsRealtime = null;
        final AtomicReference<QwenTtsRealtime> qwenTtsRef = new AtomicReference<>(null);
        qwenTtsRealtime = new QwenTtsRealtime(param, new QwenTtsRealtimeCallback() {
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
                    case "response.audio.delta":
                        String recvAudioB64 = message.get("delta").getAsString();
                        audioPlayer.write(recvAudioB64);
                        break;
                    case "response.done":
                        System.out.println("response " + qwenTtsRef.get().getResponseId() + " done");
                        completeLatch.get().countDown();
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
        qwenTtsRef.set(qwenTtsRealtime);
        try {
            qwenTtsRealtime.connect();
        } catch (NoApiKeyException e) {
            throw new RuntimeException(e);
        }
        QwenTtsRealtimeConfig config = QwenTtsRealtimeConfig.builder()
                .voice("Chelsie")
                .responseFormat(QwenTtsRealtimeAudioFormat.PCM_24000HZ_MONO_16BIT)
                .mode("server_commit")
                .build();
        qwenTtsRealtime.updateSession(config);
        for (String text:textToSynthesize) {
            qwenTtsRealtime.appendText(text);
            Thread.sleep(100);
        }
        qwenTtsRealtime.finish();
        completeLatch.get().await();
        audioPlayer.waitForComplete();
        audioPlayer.shutdown();
        System.out.println("[Metric] session: " + qwenTtsRealtime.getSessionId() +
                ", first audio delay: " + qwenTtsRealtime.getFirstAudioDelay() + " ms");
        System.exit(0);
    }
}
