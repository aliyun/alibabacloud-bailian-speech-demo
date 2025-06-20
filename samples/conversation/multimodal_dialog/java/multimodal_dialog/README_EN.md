# Multimodal Conversation Service API Integration

English | [简体中文](./README.md)

### :point_right: Prerequisites

1. #### Enable Multimodal Dialog Service
    Before running this sample, you need to enable the multimodal dialog service. Create an application in the multimodal dialog service console and perform necessary configurations, publish the application.

2. #### Configure Alibaba Cloud Bailian API-KEY

    Before running this sample, you need to obtain the app_id, workspace_id in the dialog service conslose, then obtain the Alibaba Cloud Bailian API_KEY, and perform necessary environment configuration. For detailed configuration steps regarding the API-KEY, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

3. #### Java Runtime Environment

   Before running this sample, you need to install the Java runtime environment and Maven build tool.

### :point_right: Running the Sample

You can run this sample by executing run.sh (Linux, Mac systems) or run.bat (Windows systems). 

Before running the sample, please modify the file to fill in the necessary app_id, workspace_id, and access api_key. The sample will use Push2talk mode to call the service, input audio recognition of "1 plus 1 equals what" and reply with text and audio.
The sample program provides test examples for multiple modes. By default, it runs the Push2talk mode example. You can modify the main() function to switch between different modes.

### Quick Integration

#### 1. Add Dependencies

**Maven Configuration**
```xml
<dependencies>
    <!-- DashScope SDK -->
    <dependency>
        <groupId>com.alibaba</groupId>
        <artifactId>dashscope-sdk-java</artifactId>
        <version>2.20.4</version>
    </dependency>
</dependencies>
```

#### 2. Basic Configuration

```java
import com.alibaba.dashscope.multimodal.MultiModalDialog;
import com.alibaba.dashscope.multimodal.MultiModalDialogCallback;
import com.alibaba.dashscope.multimodal.MultiModalRequestParam;
import com.alibaba.dashscope.multimodal.State;
import com.alibaba.dashscope.utils.Constants;

public class MultiModalDialogExample {
    
    // Configuration parameters
    private static final String WORKSPACE_ID = "your_workspace_id";
    private static final String APP_ID = "your_app_id";
    private static final String API_KEY = "your_api_key";
    private static final String MODEL = "multimodal-dialog";
    
    public static void main(String[] args) {
        // Set WebSocket API URL
        Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
        
        // Create test instance
        MultiModalDialogExample example = new MultiModalDialogExample();
        example.testPush2Talk();
    }
}
```

#### 3. Implement Callback Handler

```java
public class DialogCallbackImpl extends MultiModalDialogCallback {
    
    @Override
    public void onConnected() {
        System.out.println("✅ WebSocket connection established");
    }

    @Override
    public void onStarted(String dialogId) {
        System.out.println("🚀 Dialog started, ID: " + dialogId);
    }

    @Override
    public void onStateChanged(State.DialogState state) {
        switch (state) {
            case LISTENING:
                System.out.println("👂 System is listening...");
                break;
            case THINKING:
                System.out.println("🤔 AI is thinking...");
                break;
            case RESPONDING:
                System.out.println("💬 AI is responding...");
                break;
        }
    }

    @Override
    public void onSpeechAudioData(ByteBuffer audioData) {
        // Handle received audio data
        System.out.println("🔊 Received audio data: " + audioData.remaining() + " bytes");
    }

    @Override
    public void onError(String dialogId, String errorCode, String errorMsg) {
        System.err.println("❌ Error: " + errorCode + " - " + errorMsg);
    }

    @Override
    public void onClosed() {
        System.out.println("🔌 Connection closed");
    }
}
```

#### 4. Push2Talk Mode Example

```java
public void testPush2Talk() {
    // Build request parameters
    MultiModalRequestParam params = MultiModalRequestParam.builder()
        .customInput(
            MultiModalRequestParam.CustomInput.builder()
                .workspaceId(WORKSPACE_ID)
                .appId(APP_ID)
                .build())
        .upStream(
            MultiModalRequestParam.UpStream.builder()
                .mode("push2talk")
                .audioFormat("pcm")
                .build())
        .downStream(
            MultiModalRequestParam.DownStream.builder()
                .voice("longxiaochun_v2")
                .sampleRate(48000)
                .build())
        .clientInfo(
            MultiModalRequestParam.ClientInfo.builder()
                .userId("demo_user")
                .device(MultiModalRequestParam.ClientInfo.Device.builder()
                    .uuid("demo_device")
                    .build())
                .build())
        .apiKey(API_KEY)
        .model(MODEL)
        .build();

    // Create dialog instance
    MultiModalDialog conversation = new MultiModalDialog(params, new DialogCallbackImpl());
    
    try {
        // Start dialog
        conversation.start();
        
        // Wait for listening state
        waitForListeningState(conversation);
        
        // Start speech recognition
        conversation.startSpeech();
        
        // Send audio data
        sendAudioFromFile(conversation, "path/to/audio.wav");
        
        // Stop speech recognition
        conversation.stopSpeech();
        
        // Wait for dialog completion
        Thread.sleep(5000);
        
        // Stop dialog
        conversation.stop();
        
    } catch (Exception e) {
        e.printStackTrace();
    }
}

private void sendAudioFromFile(MultiModalDialog conversation, String filePath) {
    try (AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new File(filePath))) {
        byte[] buffer = new byte[3200];
        int bytesRead;
        
        while ((bytesRead = audioInputStream.read(buffer)) != -1) {
            conversation.sendAudioData(ByteBuffer.wrap(buffer, 0, bytesRead));
            Thread.sleep(100); // Simulate real-time audio streaming
        }
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```

### Interaction Modes

#### 1. Push2Talk Mode
- **Features**: Press to talk, release to stop
- **Use Cases**: Precise control of recording timing
- **Implementation**: Manually call `startSpeech()` and `stopSpeech()`

```java
// Java
conversation.startSpeech();
// Send audio data
conversation.stopSpeech();
```

#### 2. Tap2Talk Mode
- **Features**: Tap to start, automatic end detection
- **Use Cases**: Natural voice interaction
- **Implementation**: Only call `startSpeech()`, system automatically detects end

#### 3. Duplex Mode
- **Features**: Full-duplex communication with interruption support
- **Use Cases**: Real-time dialog interaction
- **Implementation**: Send audio data directly without manual control



### Features

####  Visual Q&A (VQA) Feature

```java
// Using URL-based images
public void testImageVQAWithURL() {
    JsonObject imageObject = new JsonObject();
    imageObject.addProperty("type", "url");
    imageObject.addProperty("value", "https://example.com/image.jpg");
    
    List<Object> images = Arrays.asList(imageObject);
    
    MultiModalRequestParam.UpdateParams updateParams = 
        MultiModalRequestParam.UpdateParams.builder()
            .images(images)
            .build();
    
    conversation.requestToRespond("prompt", "Describe this image", updateParams);
}
```

#### Text-to-Speech (TTS) Feature

```java

// Send text synthesis request
    String textToSynthesize = "Hello, this is a test text.";
    conversation.requestToRespond("transcript", textToSynthesize, null);
```



### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>

