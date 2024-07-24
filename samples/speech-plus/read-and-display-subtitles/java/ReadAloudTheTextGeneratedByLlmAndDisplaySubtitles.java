package org.example.ttsv2;

import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.ApiKey;
import io.reactivex.Flowable;
import javafx.util.Pair;

import javax.swing.*;
import javax.swing.text.*;
import java.awt.*;
import java.io.FileNotFoundException;
import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.Queue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

class SubtitlePlayer implements Runnable {
    private JTextPane textPane;
    private StyledDocument doc;
    private Thread workThread;
    private Queue<Pair<Boolean, ByteBuffer>> audioQueue;
    private Queue<Pair<Boolean, String>> textQueue;
    private Lock queueLock = new ReentrantLock();
    private RealtimeMp3Player audioPlayer =
            new RealtimeMp3Player();

    private AtomicBoolean stopTask;
    public SubtitlePlayer() {
        JFrame frame = new JFrame("Real-time Subtitle Example");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(1000, 300);

        textPane = new JTextPane();
        textPane.setEditable(false);

        doc = textPane.getStyledDocument();
        JScrollPane scrollPane = new JScrollPane(textPane);
        frame.getContentPane().add(scrollPane, BorderLayout.CENTER);
        frame.setVisible(true);

        stopTask = new AtomicBoolean(false);
        audioQueue = new LinkedList<>();
        textQueue = new LinkedList<>();
        audioPlayer.start();
        workThread = new Thread(this);
        workThread.start();
    }

    public void addTextToLabel(String text) {
        System.out.println("更新上屏幕：##" + text + "##");
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                try {
                    int oldLength = doc.getLength();

                    // Define a style for the regular text
                    Style regularStyle = doc.addStyle("RegularStyle", null);
                    StyleConstants.setFontSize(regularStyle, 16); // Set font size for regular text
                    StyleConstants.setBackground(regularStyle, textPane.getBackground()); // Reset background color

                    doc.insertString(doc.getLength(), text, regularStyle);

                    // Automatically scroll to the bottom
                    textPane.setCaretPosition(doc.getLength());

                    // Define a style for the highlighted text
                    Style highlightStyle = doc.addStyle("HighlightStyle", null);
                    StyleConstants.setFontSize(highlightStyle, 20); // Set a larger font size for highlighted text
                    StyleConstants.setBackground(highlightStyle, Color.GREEN);

                    // Reset previous texts to normal style
                    if (oldLength > 0) {
                        doc.setCharacterAttributes(0, oldLength, regularStyle, false);
                    }

                    // Apply highlight style to the last line
                    int newLength = doc.getLength();
                    String content = textPane.getText();
                    int lastNewLineIndex = content.lastIndexOf("\n", newLength - 2);
                    int highlightStart = lastNewLineIndex < 0 ? 0 : lastNewLineIndex + 1;

                    doc.setCharacterAttributes(highlightStart, newLength - highlightStart, highlightStyle, false);

                } catch (BadLocationException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    public void submitAudio(ByteBuffer audio) {
        queueLock.lock();
        try {
            audioQueue.add(new Pair<>(false, audio));
        } finally {
            queueLock.unlock();
        }
    }

    public void submitText(String text) {
        queueLock.lock();
        try {
            textQueue.add(new Pair<>(false, text));
        } finally {
            queueLock.unlock();
        }
    }

    public void sentenceEnd() {
        queueLock.lock();
        try {
            audioQueue.add(new Pair<>(true, null));
            textQueue.add(new Pair<>(true, null));
        } finally {
            queueLock.unlock();
        }
    }

    public void waitAndRefreshPlayer() {
        System.out.println("wait for player refresh");
        audioPlayer.stop();
        audioPlayer = new RealtimeMp3Player();
        audioPlayer.start();
        System.out.println("player refreshed");
    }

    public void stop() throws InterruptedException {
        System.out.println("SubtitlePlayer stop cmd");
        stopTask.set(true);
        workThread.join();
    }

    public void run(){
        while (true) {
            try {
                Thread.sleep(50);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
            queueLock.lock();
            try {
                System.out.println("player run loop " + stopTask.get() + " audioqueue: " + audioQueue.size() + " textqueue: " + textQueue.size());
                if (stopTask.get() && audioQueue.size() == 0 && textQueue.size() == 0) {
                    break;
                }
                if (audioQueue.size() > 0) {
                    Pair<Boolean, ByteBuffer> audio = audioQueue.peek();
                    if (audio.getKey()) {
                        while (textQueue.size() > 0) {
                            Pair<Boolean, String> text = textQueue.poll();
                            if (text.getKey()) {
                                addTextToLabel("\n");
                                audioQueue.poll();
                            } else {
                                addTextToLabel(text.getValue());
                            }
                        }
                        waitAndRefreshPlayer();
                    } else {
                        audioPlayer.write(audio.getValue());
                        audioQueue.poll();
                    }
                }
                if (textQueue.size() > 0) {
                    Pair<Boolean, String> text = textQueue.peek();
                    if (text.getKey()) {
                        addTextToLabel("\n");
                        while (audioQueue.size() > 0) {
                            Pair<Boolean, ByteBuffer> audio = audioQueue.poll();
                            if (audio.getKey()) {
                                waitAndRefreshPlayer();
                                textQueue.poll();
                            } else {
                                audioPlayer.write(audio.getValue());
                            }
                        }
                    } else {
                        addTextToLabel(text.getValue());
                        textQueue.poll();
                    }
                }
            } finally {
                queueLock.unlock();
            }
        }
        System.out.println("SubtitlePlayer thread stopped");
    }
}

enum TtsType {
    SENTENCE_BEGIN("SENTENCE_BEGIN"),
    SENTENCE_END("SENTENCE_END"),
    TEXT("TEXT");

    private final String description;
    TtsType(String description) {
        this.description = description;
    }
}

class TtsTask {
    public TtsTask(String text, TtsType type) {
        this.text = text;
        this.type = type;
    }
    public TtsType type;
    public String text;

    @Override
    public String toString() {
        return String.format("TtsTask[type: %s, text: %s]", type, text);
    }
}

class CalbackWithSubtitlePlayer extends ResultCallback<SpeechSynthesisResult> {
    private SubtitlePlayer player;
    CalbackWithSubtitlePlayer(SubtitlePlayer player) {
        this.player = player;
    }

    @Override
    public void onEvent(SpeechSynthesisResult message) {
        // Write Audio to player
        if (message.getAudioFrame() != null) {
            player.submitAudio(message.getAudioFrame());
        }
    }

    @Override
    public void onComplete() {
        System.out.println("synthesis onComplete!");
    }

    @Override
    public void onError(Exception e) {
        System.out.println("synthesis onError!");
        e.printStackTrace();
    }
}

class TtsTaskHandler implements Runnable{
    private SubtitlePlayer player;
    private Queue<TtsTask> taskList;
    private Lock queueLock = new ReentrantLock();
    private AtomicBoolean stopTask;
    private SpeechSynthesizer synthesizer;
    private Thread workThread;
    private CalbackWithSubtitlePlayer callback;
    private SpeechSynthesisParam param;

    public TtsTaskHandler(SpeechSynthesisParam param, CalbackWithSubtitlePlayer callback, SubtitlePlayer player) {
        this.param = param;
        this.callback = callback;
        this.player = player;
        this.taskList = new LinkedList<>();
        this.stopTask = new AtomicBoolean(false);
        this.workThread = new Thread(this);
        this.workThread.start();
    }

    public void restartSynthesizer() {
        synthesizer = new SpeechSynthesizer(param, callback);
    }

    public void submitTask(TtsTask task) {
        queueLock.lock();
        try {
            taskList.add(task);
        } finally {
            queueLock.unlock();
        }
    }

    public void stop() throws InterruptedException {
        System.out.println("ttsTaskHandler stop cmd");
        stopTask.set(true);
        workThread.join();
    }

    public void run() {
        restartSynthesizer();
        while(true) {
            try {
                Thread.sleep(50);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
            queueLock.lock();
            try {
                if (stopTask.get() && taskList.size() == 0) {
                    try {
                        System.out.println("ttsTaskHandler waiting player stop");
                        this.player.stop();
                    } catch (InterruptedException e) {
                        throw new RuntimeException(e);
                    }
                    break;
                }
                if (taskList.size() == 0) {
                    continue;
                }
                TtsTask task = taskList.poll();
                switch (task.type) {
                    case SENTENCE_BEGIN:
                        restartSynthesizer();
                        break;
                    case SENTENCE_END:
                        synthesizer.streamingComplete();
                        player.sentenceEnd();
                        break;
                    case TEXT:
                        synthesizer.streamingCall(task.text);
                        player.submitText(task.text);
                        break;
                }
            } finally {
                queueLock.unlock();
            }
        }
        System.out.println("TtsTaskHandler thread stopped");
    }
}

/**
 * this demo showcases how to use Alibaba Cloud's DashScope model for synthesis
 * llm streaming output text and playback of MP3 audio streams. Note that this
 * demo presents a simplified usage. For adjustments regarding audio format and
 * sample rate, please refer to the documentation.
 */
public class ReadAloudTheTextGeneratedByLlmAndDisplaySubtitles {
    public static void LLMTextToPlayer()
            throws NoApiKeyException, InputRequiredException, InterruptedException {
        // Set your DashScope API key. More information:
        // https://help.aliyun.com/document_detail/2712195.html in fact,if you have
        // set DASHSCOPE_API_KEY in your environment variable, you can ignore this,
        // and the sdk will automatically get the api_key from the environment
        // variable
        String dashScopeApiKey = null;
        try {
            ApiKey apiKey = new ApiKey();
            dashScopeApiKey = apiKey.getApiKey(null); // from environment variable.
        } catch (NoApiKeyException e) {
            System.out.println("No api key found in environment.");
        }
        if (dashScopeApiKey == null) {
            // if you can not set api_key in your environment variable,
            // you can set it here by code
            dashScopeApiKey = "your-dashscope-api-key";
        }

        // Prepare the speech synthesis task
        SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                        .model("cosyvoice-v1")
                        .voice("longxiaochun")
                        .apiKey(dashScopeApiKey)
                        .build();
        // prepare player & callback
        SubtitlePlayer player = new SubtitlePlayer();
        CalbackWithSubtitlePlayer callback = new CalbackWithSubtitlePlayer(player);
        TtsTaskHandler ttsTaskHandler = new TtsTaskHandler(param, callback, player);

        /*******  Call the Generative AI Model to get streaming text *******/
        // Prepare for the LLM call
        Generation gen = new Generation();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("请讲一个一百五十字的小故事。")
                .build();
        GenerationParam genParam =
                GenerationParam.builder()
                        .apiKey(dashScopeApiKey)
                        .model("qwen-turbo")
                        .messages(Arrays.asList(userMsg))
                        .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                        .topP(0.8)
                        .incrementalOutput(true)
                        .build();


        // Get LLM result stream
        Flowable<GenerationResult> result = gen.streamCall(genParam);
        result.blockingForEach(message -> {
            String text =
                    message.getOutput().getChoices().get(0).getMessage().getContent();
            System.out.println("LLM output：" + text);
            // send llm result to synthesizer
            if (text.contains("。")) {
                String[] parts = text.split("。");
                ttsTaskHandler.submitTask(new TtsTask(parts[0] + "。", TtsType.TEXT));
                ttsTaskHandler.submitTask(new TtsTask("", TtsType.SENTENCE_END));
                ttsTaskHandler.submitTask(new TtsTask("", TtsType.SENTENCE_BEGIN));
                if (parts.length > 1) {
                    ttsTaskHandler.submitTask(new TtsTask(parts[1], TtsType.TEXT));
                }
            } else {
                ttsTaskHandler.submitTask(new TtsTask(text, TtsType.TEXT));
            }
        });
        ttsTaskHandler.stop();
    }
    public static void main(String[] args)
            throws FileNotFoundException, InterruptedException, NoApiKeyException,
            InputRequiredException {
        LLMTextToPlayer();
        System.exit(0);
    }
}
