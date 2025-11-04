package org.alibaba.speech.examples.speech_plus;

import com.alibaba.dashscope.multimodal.MultiModalDialog;
import com.alibaba.dashscope.multimodal.MultiModalDialogCallback;
import com.alibaba.dashscope.multimodal.MultiModalRequestParam;
import com.alibaba.dashscope.multimodal.State;
import com.alibaba.dashscope.protocol.ConnectionConfigurations;
import com.alibaba.dashscope.protocol.okhttp.OkHttpClientFactory;
import com.alibaba.dashscope.utils.Constants;
import com.google.gson.JsonObject;
import lombok.extern.slf4j.Slf4j;
import okhttp3.ConnectionPool;

import java.io.File;
import java.io.FileInputStream;
import java.nio.ByteBuffer;
import java.util.HashMap;
import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

/**
 * Multi-modal dialog test cases for demonstrating various interaction modes
 * including push-to-talk, tap-to-talk, duplex communication, text synthesis,
 * visual Q&A, and agent DJ functionality.
 *
 * @author songsong.shao
 * @date 2025/4/28
 */

@Slf4j
class MultiModalDialogConcurrent implements Runnable {
    // Constants for audio processing
    private static final int AUDIO_CHUNK_SIZE = 3200; // Audio chunk size in bytes
    private static final int SLEEP_INTERVAL_MS = 100;  // Sleep interval in milliseconds
    private static final int WAIT_TIMEOUT_MS = 2000;   // Wait timeout in milliseconds

    // State management variables
    private static State.DialogState currentState;
    private static int enterListeningTimes = 2;

    // Configuration parameters - should be set before running tests
    public static String workspaceId = "";
    public static String appId = "";
    public static String dialogId = "";
    public static String apiKey = "";
    public static String model = "";
    public static String audioFile = "";
    public MultiModalDialogCallbackImpl callback;


    public MultiModalDialogConcurrent(String fileName, MultiModalDialogCallbackImpl callback) { //实际生产可以传入为音频流、MultiModalDialogCallback回调等
        currentState = State.DialogState.IDLE;
        audioFile = fileName;
        this.callback = callback;
    }


    @Override
    public void run() {
        //在子线程中运行对话实例
        testMultimodalPush2Talk();
    }

    /**
     * Test push-to-talk mode interaction
     * Flow: Set push2talk -> Wait for listening -> Start speech -> Send audio -> Stop speech -> Wait for response
     */
    public void testMultimodalPush2Talk() {
        log.info("############ Starting Push2Talk Test ############");
        MultiModalDialog conversation;
        final boolean[] isFinish = {false};
        final AtomicInteger listeningCounter = new AtomicInteger(0);
        // 使用 AtomicReference 来共享状态引用
        final AtomicReference<State.DialogState> currentStateRef = new AtomicReference<>(currentState);

        try {
            // Build request parameters for push-to-talk mode
            MultiModalRequestParam params = buildBaseRequestParams("push2talk");

            conversation = new MultiModalDialog(params, callback);
            callback.setConversationResources(conversation, currentStateRef, listeningCounter);
            //打印当前连接数
            ConnectionPool connectionPool =  OkHttpClientFactory.getOkHttpClient().connectionPool();
            int totalConnections = connectionPool.connectionCount();
            int idleConnections = connectionPool.idleConnectionCount();
            int activeConnections = totalConnections - idleConnections;

            log.info("=== OkHttp Connection Pool Status ===");
            log.info("Total Connections: {}", totalConnections);
            log.info("Idle Connections: {}", idleConnections);
            log.info("Active Connections: {}", activeConnections);

            // Start the conversation
            conversation.start();

            // Wait for the system to enter listening state
            waitForListeningState(currentStateRef);

            //在对话启动后随机等待一段时间，模拟不同长度的用户请求
            Random random = new Random();
            int randomNumber = random.nextInt(10) + 1;
            try {
                Thread.sleep(1000 * randomNumber);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }

            // Start speech recognition
            conversation.startSpeech();

            // Send audio data from file
            sendAudioFromFile(audioFile, conversation);

            // Stop speech recognition
            conversation.stopSpeech();

            // Wait for conversation completion
            waitForConversationCompletion(2);

            // Clean up
            stopConversation(conversation);

        } catch (Exception e) {
            log.error("Error in push2talk test: ", e);
        } finally {
            log.info("############ Push2Talk Test Completed ############");
        }
    }


    // ==================== Helper Methods ====================

    /**
     * Build base request parameters with common configuration
     *
     * @param mode The interaction mode (push2talk, tap2talk, duplex)
     * @return Configured MultiModalRequestParam
     */
    private MultiModalRequestParam buildBaseRequestParams(String mode) {
        return MultiModalRequestParam.builder()
                .customInput(
                        MultiModalRequestParam.CustomInput.builder()
                                .workspaceId(workspaceId)
                                .appId(appId)
                                .build())
                .upStream(
                        MultiModalRequestParam.UpStream.builder()
                                .mode(mode)
                                .audioFormat("pcm")
                                .passThroughParams(new HashMap<String, Object>() {{
                                    put("sample_rate", 16000);
                                }})
                                .build())
                .downStream(
                        MultiModalRequestParam.DownStream.builder()
                                .voice("longwan")
                                .audioFormat("pcm")
                                .intermediateText("transcript")
                                .sampleRate(48000)
                                .build())
                .clientInfo(MultiModalRequestParam.ClientInfo.builder()
                        .userId("abbc")
                        .build())
                .apiKey(apiKey)
                .model(model)
                .build();
    }

    /**
     * Wait for the system to enter listening state
     */
    private void waitForListeningState(AtomicReference<State.DialogState> stateRef) {
        while (State.DialogState.LISTENING != stateRef.get()) {
            try {
                Thread.sleep(SLEEP_INTERVAL_MS);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Interrupted while waiting for listening state", e);
            }
        }
        log.info("System entered listening state");
    }

    /**
     * Send audio data from a file to the conversation
     *
     * @param filePath Path to the audio file
     */
    private void sendAudioFromFile(String filePath, MultiModalDialog conversation) {
        File audioFile = new File(filePath);

        if (!audioFile.exists()) {
            log.error("Audio file not found: {}", filePath);
            return;
        }

        try (FileInputStream audioInputStream = new FileInputStream(audioFile)) {
            byte[] audioBuffer = new byte[AUDIO_CHUNK_SIZE];
            int bytesRead;
            int totalBytesRead = 0;

            log.info("Starting to send audio data from: {}", filePath);

            // Read and send audio data in chunks
            while ((bytesRead = audioInputStream.read(audioBuffer)) != -1) {
                totalBytesRead += bytesRead;

                // Send audio chunk to conversation
                conversation.sendAudioData(ByteBuffer.wrap(audioBuffer, 0, bytesRead));

                // Add small delay to simulate real-time audio streaming
                Thread.sleep(SLEEP_INTERVAL_MS);
            }

            log.info("Finished sending audio data. Total bytes sent: {}", totalBytesRead);

        } catch (Exception e) {
            log.error("Error sending audio from file: {}", filePath, e);
        }
    }


    /**
     * Wait for conversation completion
     *
     * @param listeningTimes Expected number of listening state entries
     */
    private void waitForConversationCompletion(int listeningTimes) {
        while (enterListeningTimes < listeningTimes) {
            try {
                Thread.sleep(WAIT_TIMEOUT_MS);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Interrupted while waiting for conversation completion", e);
            }
        }
        log.info("Conversation completed after {} listening cycles", listeningTimes);
    }

    /**
     * Stop the conversation and clean up resources
     */
    private void stopConversation(MultiModalDialog conversation) {
        try {
            if (conversation != null) {
                conversation.stop();
                Thread.sleep(1000); // Allow time for cleanup
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            log.warn("Interrupted while stopping conversation");
        }
    }


}

/**
 * Implementation of MultiModalDialogCallback for handling various conversation events
 */
@Slf4j
class MultiModalDialogCallbackImpl extends MultiModalDialogCallback {
    private MultiModalDialog conversation;
    private AtomicReference<State.DialogState> currentStateRef;
    private AtomicInteger listeningTimes;

    public void setConversationResources(MultiModalDialog conversation, AtomicReference<State.DialogState> currentStateRef, AtomicInteger listeningTimes) {
        this.conversation = conversation;
        this.currentStateRef = currentStateRef;
        this.listeningTimes = listeningTimes;
    }

    @Override
    public void onConnected() {
        log.info("WebSocket connection established");
    }

    @Override
    public void onStarted(String dialogId) {
        log.info("Dialog started with ID: {}", dialogId);
    }

    @Override
    public void onStopped(String dialogId) {
        log.info("Dialog stopped with ID: {}", dialogId);
        if (conversation != null) {
            conversation.getDuplexApi().close(1000, "local close");
        }
    }

    @Override
    public void onSpeechStarted(String dialogId) {
        log.info("Speech recognition started for dialog: {}", dialogId);
    }

    @Override
    public void onSpeechEnded(String dialogId) {
        log.info("Speech recognition ended for dialog: {}", dialogId);
    }

    @Override
    public void onError(String dialogId, String errorCode, String errorMsg) {
        log.error("Error occurred - Dialog: {}, Code: {}, Message: {}", dialogId, errorCode, errorMsg);
        if (conversation != null) {
            listeningTimes.incrementAndGet();
            conversation.getDuplexApi().close(1001, "error, close connection");
        }
    }

    @Override
    public void onStateChanged(State.DialogState state) {
        log.info("Dialog state changed to: {}", state);
        // 更新共享的状态引用
        if (currentStateRef != null) {
            currentStateRef.set(state);
        }

        if (state == State.DialogState.LISTENING) {
            listeningTimes.incrementAndGet();
            log.info("Entered listening state" + listeningTimes.get());
        }
    }

    @Override
    public void onSpeechAudioData(ByteBuffer audioData) {
    }

    @Override
    public void onRespondingStarted(String dialogId) {
        log.info("Response generation started for dialog: {}", dialogId);
        if (conversation != null) {
            conversation.localRespondingStarted();
        }
    }

    @Override
    public void onRespondingEnded(String dialogId, JsonObject jsonObject) {
        log.info("Response generation ended for dialog: {}", dialogId);
        if (conversation != null) {
            conversation.localRespondingEnded();
        }
    }

    @Override
    public void onRespondingContent(String dialogId, JsonObject content) {
        log.info("Response content received - Dialog: {}, Content: {}", dialogId, content);
    }

    @Override
    public void onSpeechContent(String dialogId, JsonObject content) {
        log.info("Speech content received - Dialog: {}, Content: {}", dialogId, content);
    }

    @Override
    public void onRequestAccepted(String dialogId) {
        log.info("Request accepted for dialog: {}", dialogId);
    }

    @Override
    public void onClosed() {
        log.info("Connection closed");
        if (conversation != null) {
            listeningTimes.incrementAndGet();
        }
    }
}

@Slf4j
public class MultiModalDialogConcurrentTest{
    /**
     * Main method to run the test cases
     * Configure the required parameters before running
     */
    public static void main(String[] args) throws InterruptedException {
        log.info("############ Initializing Multi-modal Dialog Tests ############");
        //调整连接池大小。默认连接池为 32，如果您的场景并发较高，可以调大连接池数量，避免卡顿。
        Constants.connectionConfigurations = ConnectionConfigurations.builder()
                .connectionPoolSize(500)
                .maximumAsyncRequests(500)
                .maximumAsyncRequestsPerHost(500)
                .build();

        checkoutEnv("DASHSCOPE_CONNECTION_POOL_SIZE", 500);
        checkoutEnv("DASHSCOPE_MAXIMUM_ASYNC_REQUESTS", 500);
        checkoutEnv("DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST", 500);
        // Configure WebSocket API URL
        Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
        log.info("WebSocket API URL: {}", Constants.baseWebsocketApiUrl);


        // Configure test parameters (replace with actual values)
        MultiModalDialogConcurrent.workspaceId = "your_workspace_id";
        MultiModalDialogConcurrent.appId = "your_app_id";
        MultiModalDialogConcurrent.apiKey = "your_api_key";
        MultiModalDialogConcurrent.model = "multimodal-dialog";


        int runTimes = 4;
        // Create the pool of dialog objects
        ExecutorService executorService = Executors.newFixedThreadPool(runTimes);

        for (int i = 0; i < 20; i++) {
            // 输入参数，可以替换为外部请求；回调可以增加参数来做结果输出或者信号同步
            executorService.submit(new MultiModalDialogConcurrent("../../../../sample-data/1_plus_1.wav", new MultiModalDialogCallbackImpl()));
        }

        // Shut down the ExecutorService and wait for all tasks to complete
        executorService.shutdown();
        executorService.awaitTermination(1, TimeUnit.MINUTES);

        log.info("############ Multi-modal Dialog Tests Completed ############");
        System.exit(0);
    }

    public static void checkoutEnv(String envName, int defaultSize) {
        if (System.getenv(envName) != null) {
            System.out.println("[ENV CHECK]: " + envName + " "
                    + System.getenv(envName));
        } else {
            System.out.println("[ENV CHECK]: " + envName
                    + " Using Default which is " + defaultSize);
        }
    }
}