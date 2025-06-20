[comment]: # (title and brief introduction of the sample)
# 多模态对话服务 API 集成
简体中文 | [English](./README_EN.md)


### :point_right: 前置条件

1. #### 开通多模态对话服务
    在运行此示例之前，您需要开通多模态对话服务，并在多模态对话服务控制台中创建应用并进行必要配置，发布应用。

2. #### 配置阿里云百炼 API-KEY

    在运行此示例之前，您需要在对话服务控制台中获取 app_id、workspace_id，然后获取阿里云百炼 API_KEY，并进行必要的环境配置。有关 API-KEY 的详细配置步骤，请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

3. #### Java 运行环境

   在运行此示例之前，您需要安装 Java 运行环境和 Maven 构建工具。

### :point_right: 运行示例

您可以通过执行 run.sh（Linux、Mac 系统）或 run.bat（Windows 系统）来运行此示例。

在运行示例之前，请修改文件以填入必要的 app_id、workspace_id 和访问 api_key。示例将使用 Push2talk 模式调用服务，输入"1加1等于多少"的音频识别并回复文本和音频。
示例程序提供了多种模式的测试示例。默认情况下，它运行 Push2talk 模式示例。您可以修改 main() 函数来切换不同的模式。

### 快速集成

#### 1. 添加依赖

**Maven 配置**
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

#### 2. 基础配置

```java
import com.alibaba.dashscope.multimodal.MultiModalDialog;
import com.alibaba.dashscope.multimodal.MultiModalDialogCallback;
import com.alibaba.dashscope.multimodal.MultiModalRequestParam;
import com.alibaba.dashscope.multimodal.State;
import com.alibaba.dashscope.utils.Constants;

public class MultiModalDialogExample {
    
    // 配置参数
    private static final String WORKSPACE_ID = "your_workspace_id";
    private static final String APP_ID = "your_app_id";
    private static final String API_KEY = "your_api_key";
    private static final String MODEL = "multimodal-dialog";
    
    public static void main(String[] args) {
        // 设置 WebSocket API URL
        Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
        
        // 创建测试实例
        MultiModalDialogExample example = new MultiModalDialogExample();
        example.testPush2Talk();
    }
}
```

#### 3. 实现回调处理器

```java
public class DialogCallbackImpl extends MultiModalDialogCallback {
    
    @Override
    public void onConnected() {
        System.out.println("✅ WebSocket 连接已建立");
    }

    @Override
    public void onStarted(String dialogId) {
        System.out.println("🚀 对话已开始，ID: " + dialogId);
    }

    @Override
    public void onStateChanged(State.DialogState state) {
        switch (state) {
            case LISTENING:
                System.out.println("👂 系统正在监听...");
                break;
            case THINKING:
                System.out.println("🤔 AI 正在思考...");
                break;
            case RESPONDING:
                System.out.println("💬 AI 正在回应...");
                break;
        }
    }

    @Override
    public void onSpeechAudioData(ByteBuffer audioData) {
        // 处理接收到的音频数据
        System.out.println("🔊 接收到音频数据: " + audioData.remaining() + " 字节");
    }

    @Override
    public void onError(String dialogId, String errorCode, String errorMsg) {
        System.err.println("❌ 错误: " + errorCode + " - " + errorMsg);
    }

    @Override
    public void onClosed() {
        System.out.println("🔌 连接已关闭");
    }
}
```

#### 4. Push2Talk 模式示例

```java
public void testPush2Talk() {
    // 构建请求参数
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

    // 创建对话实例
    MultiModalDialog conversation = new MultiModalDialog(params, new DialogCallbackImpl());
    
    try {
        // 开始对话
        conversation.start();
        
        // 等待监听状态
        waitForListeningState(conversation);
        
        // 开始语音识别
        conversation.startSpeech();
        
        // 发送音频数据
        sendAudioFromFile(conversation, "path/to/audio.wav");
        
        // 停止语音识别
        conversation.stopSpeech();
        
        // 等待对话完成
        Thread.sleep(5000);
        
        // 停止对话
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
            Thread.sleep(100); // 模拟实时音频流
        }
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```

### 交互模式

#### 1. Push2Talk 模式
- **特点**: 按下说话，松开停止
- **适用场景**: APP或者玩具通过按钮说话
- **实现方式**: 手动调用 `startSpeech()` 和 `stopSpeech()`

```java
// Java
conversation.startSpeech();
// 发送音频数据
conversation.stopSpeech();
```

#### 2. Tap2Talk 模式
- **特点**: 点击开始，自动结束检测
- **适用场景**: 支持唤醒的场景，或者按键开始
- **实现方式**: 只调用 `startSpeech()`，系统自动检测结束

#### 3. Duplex 模式
- **特点**: 全双工通信，支持打断
- **适用场景**: 实时对话交互
- **实现方式**: 直接发送音频数据，无需手动控制

### 功能特性

#### 图片问答（VQA）功能

```java
// 使用 URL 图片
public void testImageVQAWithURL() {
    JsonObject imageObject = new JsonObject();
    imageObject.addProperty("type", "url");
    imageObject.addProperty("value", "https://example.com/image.jpg");
    
    List<Object> images = Arrays.asList(imageObject);
    
    MultiModalRequestParam.UpdateParams updateParams = 
        MultiModalRequestParam.UpdateParams.builder()
            .images(images)
            .build();
    
    conversation.requestToRespond("prompt", "描述这张图片", updateParams);
}
```

#### 文本转语音（TTS）功能

```java
// 发送文本合成请求
String textToSynthesize = "你好，这是一段测试文本。";
conversation.requestToRespond("transcript", textToSynthesize, null);
```

### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>