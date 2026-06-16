/*
 * Copyright (C) Alibaba Group. All Rights Reserved.
 * MIT License (https://opensource.org/licenses/MIT)
 */

package org.alibaba.speech.examples.omni;

import com.alibaba.dashscope.audio.omni.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import javax.sound.sampled.*;
import java.nio.ByteBuffer;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;
import java.util.function.Function;

/**
 * Omni Realtime Conversation Example - with Function Calling
 * Demonstrates how to use real-time voice dialogue combined with local tool calling
 */
public class OmniWithFunctionCall {

    public static void main(String[] args) {
        try {
            // Initialize components
            AudioPlayer audioPlayer = new AudioPlayer();
            ToolRegistry toolRegistry = new ToolRegistry();
            ConversationHandler handler = new ConversationHandler(audioPlayer, toolRegistry);

            // Create and configure conversation
            OmniRealtimeParam param = OmniRealtimeParam.builder()
                    .model("qwen3.5-omni-plus-realtime")
                    .apikey(System.getenv("DASHSCOPE_API_KEY"))
                    .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
                    .build();

            OmniRealtimeConversation conversation = new OmniRealtimeConversation(param, handler);
            conversation.connect();

            // Configure session parameters
            configureSession(conversation, toolRegistry);

            // Start audio capture
            startAudioCapture(conversation, handler);

            // Clean up resources
            cleanup(conversation, audioPlayer);

        } catch (NoApiKeyException e) {
            System.err.println("API KEY not found: please set environment variable DASHSCOPE_API_KEY");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void configureSession(OmniRealtimeConversation conversation, ToolRegistry toolRegistry) {
        HashMap<String, Object> additionalConfig = new HashMap<>();
        additionalConfig.put("tools", toolRegistry.buildToolsDefinition());

        conversation.updateSession(OmniRealtimeConfig.builder()
                .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
                .voice("Tina")
                .enableTurnDetection(true)
                .enableInputAudioTranscription(true)
                .parameters(additionalConfig)
                .build());

        System.out.println("Function calling enabled. Please start speaking (press Ctrl+C to exit)...");
    }

    private static void startAudioCapture(OmniRealtimeConversation conversation, ConversationHandler handler)
            throws LineUnavailableException {
        AudioFormat format = new AudioFormat(16000, 16, 1, true, false);
        TargetDataLine mic = AudioSystem.getTargetDataLine(format);
        mic.open(format);
        mic.start();

        ByteBuffer buffer = ByteBuffer.allocate(3200);
        while (!handler.getShouldStop().get()) {
            int bytesRead = mic.read(buffer.array(), 0, buffer.capacity());
            if (bytesRead > 0) {
                conversation.appendAudio(Base64.getEncoder().encodeToString(buffer.array()));

                // Check and process pending tool calls
                if (handler.hasPendingToolCalls()) {
                    System.out.println("*** create response after call tools");
                    handler.processPendingToolCalls(conversation);
                    conversation.createResponse(null, Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT));
                    System.out.println("======TOOL CALL END======");
                }
            }
            try {
                Thread.sleep(20);
            } catch (InterruptedException ignored) {}
        }

        mic.close();
    }

    private static void cleanup(OmniRealtimeConversation conversation, AudioPlayer audioPlayer) {
        try {
            conversation.close(1000, "Normal termination");
            audioPlayer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * Audio Player - responsible for sequential audio playback
     */
    static class AudioPlayer {
        private final SourceDataLine line;
        private final Queue<byte[]> audioQueue = new ConcurrentLinkedQueue<>();
        private final Thread playerThread;
        private final AtomicBoolean shouldStop = new AtomicBoolean(false);

        public AudioPlayer() throws LineUnavailableException {
            AudioFormat format = new AudioFormat(24000, 16, 1, true, false);
            line = AudioSystem.getSourceDataLine(format);
            line.open(format);
            line.start();

            playerThread = new Thread(this::playLoop, "AudioPlayer");
            playerThread.start();
        }

        private void playLoop() {
            while (!shouldStop.get()) {
                byte[] audio = audioQueue.poll();
                if (audio != null) {
                    line.write(audio, 0, audio.length);
                } else {
                    try {
                        Thread.sleep(10);
                    } catch (InterruptedException ignored) {}
                }
            }
        }

        public void play(String base64Audio) {
            audioQueue.add(Base64.getDecoder().decode(base64Audio));
        }

        public void close() {
            shouldStop.set(true);
            try {
                playerThread.join(1000);
            } catch (InterruptedException ignored) {}
            line.drain();
            line.close();
        }
    }

    /**
     * Tool Registry - manages available tools and their implementations
     */
    static class ToolRegistry {
        private final Map<String, Function<JsonObject, String>> tools = new ConcurrentHashMap<>();
        private final Map<String, JsonObject> pendingToolCalls = new ConcurrentHashMap<>();

        public ToolRegistry() {
            registerDefaultTools();
        }

        private void registerDefaultTools() {
            registerTool("get_current_weather", this::getCurrentWeather);
            registerTool("get_flight_price", this::getFlightPrice);
            registerTool("get_train_price", this::getTrainPrice);
        }

        public void registerTool(String name, Function<JsonObject, String> handler) {
            tools.put(name, handler);
        }

        /**
         * Build tool definitions (OpenAI format)
         */
        public List<Map<String, Object>> buildToolsDefinition() {
            List<Map<String, Object>> definitions = new ArrayList<>();

            definitions.add(createFunctionDefinition(
                    "get_current_weather",
                    "当你想查询指定城市的天气时非常有用。",
                    createParamsSchema(
                            Collections.singletonMap("location",
                                    createProperty("string", "城市或县区，比如北京市、杭州市、余杭区等。")),
                            Collections.singletonList("location")
                    )
            ));

            Map<String, Object> flightProps = new HashMap<>();
            flightProps.put("src", createProperty("string", "飞机起飞的城市，比如北京市、杭州市等。"));
            flightProps.put("dst", createProperty("string", "飞机降落的城市，比如北京市、杭州市区等。"));
            definitions.add(createFunctionDefinition(
                    "get_flight_price",
                    "当你想查询飞机票价格时非常有用。",
                    createParamsSchema(flightProps, Arrays.asList("src", "dst"))
            ));

            Map<String, Object> trainProps = new HashMap<>();
            trainProps.put("src", createProperty("string", "火车出发的城市，比如北京市、杭州市等。"));
            trainProps.put("dst", createProperty("string", "火车到达的城市，比如北京市、杭州市区等。"));
            definitions.add(createFunctionDefinition(
                    "get_train_price",
                    "当你想查询火车票价格时非常有用。",
                    createParamsSchema(trainProps, Arrays.asList("src", "dst"))
            ));

            return definitions;
        }

        private Map<String, Object> createFunctionDefinition(String name, String description, Map<String, Object> parameters) {
            Map<String, Object> function = new HashMap<>();
            function.put("name", name);
            function.put("description", description);
            function.put("parameters", parameters);

            Map<String, Object> tool = new HashMap<>();
            tool.put("type", "function");
            tool.put("function", function);
            return tool;
        }

        private Map<String, Object> createParamsSchema(Map<String, Object> properties, List<String> required) {
            Map<String, Object> schema = new HashMap<>();
            schema.put("type", "object");
            schema.put("properties", properties);
            schema.put("required", required);
            return schema;
        }

        private Map<String, Object> createProperty(String type, String description) {
            Map<String, Object> prop = new HashMap<>();
            prop.put("type", type);
            prop.put("description", description);
            return prop;
        }

        /**
         * Add a tool call to the pending queue
         */
        public void addPendingToolCall(String callId, JsonObject toolCall) {
            pendingToolCalls.put(callId, toolCall);
        }

        /**
         * Check if there are pending tool calls
         */
        public boolean hasPendingToolCalls() {
            return !pendingToolCalls.isEmpty();
        }

        /**
         * Process all pending tool calls
         */
        public void processPendingToolCalls(OmniRealtimeConversation conversation) {
            if (pendingToolCalls.isEmpty()) {
                return;
            }

            for (Map.Entry<String, JsonObject> entry : pendingToolCalls.entrySet()) {
                String callId = entry.getKey();
                JsonObject toolCall = entry.getValue();

                String result = executeTool(toolCall);
                sendToolResult(conversation, callId, result);
            }

            pendingToolCalls.clear();
        }

        private String executeTool(JsonObject toolCall) {
            String functionName = toolCall.get("name").getAsString();
            JsonObject arguments = new Gson().fromJson(
                    toolCall.get("arguments").getAsString(),
                    JsonObject.class
            );

            System.out.println("[Tool Call] start handling: " + functionName + ", args: " + arguments);

            Function<JsonObject, String> handler = tools.get(functionName);
            if (handler == null) {
                return "Tool not found on client, call failed.";
            }

            String result = handler.apply(arguments);
            System.out.println("[Tool Call] response: " + result);
            return result;
        }

        private void sendToolResult(OmniRealtimeConversation conversation, String callId, String output) {
            JsonObject item = new JsonObject();
            item.addProperty("id", "item_" + UUID.randomUUID().toString().replace("-", ""));
            item.addProperty("type", "function_call_output");
            item.addProperty("call_id", callId);
            item.addProperty("output", output);

            conversation.createItem(item);
        }

        // ===== Tool Implementations =====

        private String getCurrentWeather(JsonObject args) {
            String location = args.get("location").getAsString();
            return location + " today: haze turning to sunny, temperature 4/-4C, light breeze";
        }

        private String getFlightPrice(JsonObject args) {
            String src = args.get("src").getAsString();
            String dst = args.get("dst").getAsString();
            return src + " to " + dst + " flight ticket costs 200~300 USD.";
        }

        private String getTrainPrice(JsonObject args) {
            String src = args.get("src").getAsString();
            String dst = args.get("dst").getAsString();
            return src + " to " + dst + " train ticket costs 100~200 RMB.";
        }
    }

    /**
     * Conversation Handler - processes WebSocket events
     */
    static class ConversationHandler extends OmniRealtimeCallback {
        private final AudioPlayer audioPlayer;
        private final ToolRegistry toolRegistry;
        private final AtomicBoolean shouldStop = new AtomicBoolean(false);
        private final AtomicReference<StringBuilder> responseTextRef = new AtomicReference<>(new StringBuilder());

        private long lastPackageTime = 0;
        private boolean isFirstText = true;
        private boolean isFirstAudio = true;

        public ConversationHandler(AudioPlayer audioPlayer, ToolRegistry toolRegistry) {
            this.audioPlayer = audioPlayer;
            this.toolRegistry = toolRegistry;
        }

        public AtomicBoolean getShouldStop() {
            return shouldStop;
        }

        @Override
        public void onOpen() {
            System.out.println("Connection established");
        }

        @Override
        public void onClose(int code, String reason) {
            System.out.println("Connection closed");
            shouldStop.set(true);
        }

        @Override
        public void onEvent(JsonObject message) {
            String type = message.get("type").getAsString();

            switch (type) {
                case "session.created":
                    handleSessionCreated(message);
                    break;
                case "conversation.item.input_audio_transcription.completed":
                    handleTranscriptionCompleted(message);
                    break;
                case "response.audio_transcript.delta":
                case "response.text.delta":
                    handleTextDelta(message);
                    break;
                case "response.audio.delta":
                    handleAudioDelta(message);
                    break;
                case "input_audio_buffer.speech_started":
                    handleSpeechStarted();
                    break;
                case "input_audio_buffer.speech_stopped":
                    handleSpeechStopped();
                    break;
                case "response.function_call_arguments.done":
                    handleFunctionCall(message);
                    break;
                case "response.done":
                    handleResponseDone();
                    break;
                default:
                    break;
            }
        }

        private void handleSessionCreated(JsonObject message) {
            String sessionId = message.get("session").getAsJsonObject().get("id").getAsString();
            System.out.println("start session: " + sessionId);
        }

        private void handleTranscriptionCompleted(JsonObject message) {
            System.out.println("question: " + message.get("transcript").getAsString());
        }

        private void handleTextDelta(JsonObject message) {
            if (isFirstText) {
                isFirstText = false;
                System.out.println("first text latency from vad end: " +
                        (System.currentTimeMillis() - lastPackageTime) + " ms");
            }
            String text = message.get("delta").getAsString();
            responseTextRef.get().append(text);
        }

        private void handleAudioDelta(JsonObject message) {
            if (isFirstAudio) {
                isFirstAudio = false;
                System.out.println("first audio latency from vad end: " +
                        (System.currentTimeMillis() - lastPackageTime) + " ms");
            }
            System.out.println("audio interval: " + (System.currentTimeMillis() - lastPackageTime) + " ms");
            lastPackageTime = System.currentTimeMillis();
            audioPlayer.play(message.get("delta").getAsString());
        }

        private void handleSpeechStarted() {
            System.out.println("======VAD Speech Start======");
        }

        private void handleSpeechStopped() {
            System.out.println("======VAD Speech End======");
            lastPackageTime = System.currentTimeMillis();
            isFirstText = true;
            isFirstAudio = true;
        }

        private void handleFunctionCall(JsonObject message) {
            System.out.println("======TOOL CALL======");
            String callId = message.get("call_id").getAsString();
            toolRegistry.addPendingToolCall(callId, message);
        }

        private void handleResponseDone() {
            System.out.println("======RESPONSE DONE======");
            System.out.println("all response text: " + responseTextRef.get());
            responseTextRef.set(new StringBuilder());
        }

        /**
         * Check if there are pending tool calls
         */
        public boolean hasPendingToolCalls() {
            return toolRegistry.hasPendingToolCalls();
        }

        /**
         * Process all pending tool calls
         */
        public void processPendingToolCalls(OmniRealtimeConversation conversation) {
            toolRegistry.processPendingToolCalls(conversation);
        }
    }
}
