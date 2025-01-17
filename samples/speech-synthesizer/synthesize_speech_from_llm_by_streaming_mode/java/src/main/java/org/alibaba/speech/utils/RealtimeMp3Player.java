/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */
package org.alibaba.speech.utils;

import java.io.IOException;
import java.io.PipedInputStream;
import java.io.PipedOutputStream;
import java.nio.ByteBuffer;
import java.util.concurrent.CountDownLatch;
import javazoom.jl.decoder.JavaLayerException;
import javazoom.jl.player.advanced.AdvancedPlayer;
import javazoom.jl.player.advanced.PlaybackEvent;
import javazoom.jl.player.advanced.PlaybackListener;

// JLayer library is utilized in this demo for audio decoding and playback, but you can employ other
// methods suited to your needs.
public class RealtimeMp3Player {

  // audio player
  private static AdvancedPlayer player;
  // init pipe stream, input/output
  private static PipedOutputStream pipedOutputStream; // use to write audio data to pipe stream
  private static PipedInputStream pipedInputStream; // use to read audio data from pipe stream
  CountDownLatch latch = new CountDownLatch(1);

  public void start() {
    try {
      System.out.println("build pipe stream for audio to play");
      pipedOutputStream = new PipedOutputStream();
      pipedInputStream = new PipedInputStream(pipedOutputStream, 1024 * 256);
    } catch (IOException e) {
      e.printStackTrace();
    }

    new Thread(
            () -> {
              try {
                player = new AdvancedPlayer(pipedInputStream);

                // Create a listener to respond to playback events
                player.setPlayBackListener(
                    new PlaybackListener() {
                      @Override
                      public void playbackFinished(PlaybackEvent event) {
                        System.out.println("Playback finished.");
                        latch.countDown();
                        System.exit(0);
                      }
                    });

                // System.out.println("player start");
                player.play();
              } catch (JavaLayerException e) {
                e.printStackTrace();
              }
            })
        .start();
  }

  // write audio data to pipe stream
  public void write(ByteBuffer audioData) {
    try {
      pipedOutputStream.write(audioData.array());
      pipedOutputStream.flush();
      // System.out.printf("write audio data to pipe stream %d \n", audioData.array().length);
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

  // stop feed audio data to pipe stream
  public void stop() {
    // System.out.println("Stop AudioPlayer data feed");
    try {
      pipedOutputStream.close();
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
    try {
      latch.await();
    } catch (InterruptedException e) {
      throw new RuntimeException(e);
    }
    System.out.println("AudioPlayerStoped");
  }
}
