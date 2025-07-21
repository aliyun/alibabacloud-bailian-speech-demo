package org.alibaba.speech.utils;

import javax.sound.sampled.*;
import java.io.IOException;
import java.util.Base64;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicBoolean;

public class RealtimePcmPlayer {
    private int sampleRate;
    private SourceDataLine line;
    private AudioFormat audioFormat;
    private Thread decoderThread;
    private Thread playerThread;
    private AtomicBoolean stopped = new AtomicBoolean(false);
    private Queue<String> b64AudioBuffer = new ConcurrentLinkedQueue<>();
    private Queue<byte[]> RawAudioBuffer = new ConcurrentLinkedQueue<>();

    // 构造函数初始化音频格式和音频线路
    public RealtimePcmPlayer(int sampleRate) throws LineUnavailableException {
        this.sampleRate = sampleRate;
        this.audioFormat = new AudioFormat(this.sampleRate, 16, 1, true, false);
        DataLine.Info info = new DataLine.Info(SourceDataLine.class, audioFormat);
        line = (SourceDataLine) AudioSystem.getLine(info);
        line.open(audioFormat);
        line.start();
        decoderThread = new Thread(new Runnable() {
            @Override
            public void run() {
                while (!stopped.get()) {
                    String b64Audio = b64AudioBuffer.poll();
                    if (b64Audio != null) {
                        byte[] rawAudio = Base64.getDecoder().decode(b64Audio);
                        RawAudioBuffer.add(rawAudio);
                    } else {
                        try {
                            Thread.sleep(100);
                        } catch (InterruptedException e) {
                            throw new RuntimeException(e);
                        }
                    }
                }
            }
        });
        playerThread = new Thread(new Runnable() {
            @Override
            public void run() {
                while (!stopped.get()) {
                    byte[] rawAudio = RawAudioBuffer.poll();
                    if (rawAudio != null) {
                        try {
                            playChunk(rawAudio);
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        } catch (InterruptedException e) {
                            throw new RuntimeException(e);
                        }
                    } else {
                        try {
                            Thread.sleep(100);
                        } catch (InterruptedException e) {
                            throw new RuntimeException(e);
                        }
                    }
                }
            }
        });
        decoderThread.start();
        playerThread.start();
    }

    // 播放一个音频块并阻塞直到播放完成
    private void playChunk(byte[] chunk) throws IOException, InterruptedException {
        if (chunk == null || chunk.length == 0) return;

        int bytesWritten = 0;
        while (bytesWritten < chunk.length) {
            bytesWritten += line.write(chunk, bytesWritten, chunk.length - bytesWritten);
        }
        int audioLength = chunk.length / (this.sampleRate*2/1000);
        // 等待缓冲区中的音频播放完成
        Thread.sleep(audioLength - 10);
    }

    public void write(String b64Audio) {
        b64AudioBuffer.add(b64Audio);
    }

    public void cancel() {
        b64AudioBuffer.clear();
        RawAudioBuffer.clear();
    }

    public void waitForComplete() throws InterruptedException {
        while (!b64AudioBuffer.isEmpty() || !RawAudioBuffer.isEmpty()) {
            Thread.sleep(100);
        }
        line.drain();
    }

    public void shutdown() throws InterruptedException {
        stopped.set(true);
        decoderThread.join();
        playerThread.join();
        if (line != null && line.isRunning()) {
            line.drain();
            line.close();
        }
    }
}
