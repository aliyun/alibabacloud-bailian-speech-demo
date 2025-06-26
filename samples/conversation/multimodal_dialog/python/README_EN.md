# Multimodal Conversation Simple Example

English | [简体中文](./README.md)

### :point_right: Prerequisites

1. #### Configure Alibaba Cloud Bailian API-KEY

    Before running this sample, you need to activate an Alibaba Cloud account, obtain the Alibaba Cloud Bailian API_KEY, and perform necessary environment configuration. For detailed configuration steps regarding the API-KEY, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### Enable Multimodal Conversation Service
    Before running this sample, you need to enable the multimodal conversation service. Create an application in the multimodal conversation service console and perform necessary configurations, publish the application, and obtain the app_id, workspace_id, and access api_key.

3. #### Install Python Dependencies

    The Alibaba Cloud Bailian SDK runtime environment requires Python 3.9 or higher. You can use the following command to install the dependencies for this sample:
    ```commandline
    pip3 install -r requirements.txt
    ```

### :point_right: Running the Sample
Please modify the sample to fill in the necessary app_id, workspace_id, and api_key. You can run this sample using the following command:

```commandline
export DASHSCOPE_LOGGING_LEVEL='info' # Enable dashscope SDK internal logging
python3 run.py
```

When the sample runs, it will use Push2talk mode to call the service, input audio recognition of "1 plus 1 equals what" and reply with text and audio.


### Quick Integration

#### 1. Install Dependencies

```bash
pip install dashscope
```

#### 2. Basic Configuration

```python
from dashscope.multimodal.dialog_state import DialogState
from dashscope.multimodal.multimodal_dialog import MultiModalDialog, MultiModalCallback
from dashscope.multimodal.multimodal_request_params import (
    Upstream, Downstream, ClientInfo, RequestParameters, Device
)

# Configuration parameters
WORKSPACE_ID = "your_workspace_id"
APP_ID = "your_app_id"
API_KEY = "your_api_key"
MODEL = "multimodal-dialog"
WEBSOCKET_URL = "wss://dashscope.aliyuncs.com/api-ws/v1/inference"
```

#### 3. Implement Callback Handler

```python
class ChatCallback(MultiModalCallback):
    """Dialog callback handler"""
    
    def on_connected(self):
        print("✅ WebSocket connection established")

    def on_started(self, dialog_id: str):
        print(f"Dialog started, ID: {dialog_id}")

    def on_state_changed(self, state: DialogState):
        state_messages = {
            DialogState.LISTENING: "👂 System is listening...",
            DialogState.THINKING: "🤔 AI is thinking...",
            DialogState.RESPONDING: "💬 AI is responding..."
        }

    def on_speech_audio_data(self, data: bytes):
        print(f"Received audio data: {len(data)} bytes")

    def on_error(self, error: Exception):
        print(f"❌ Error: {error}")

    def on_close(self, close_status_code: int, close_msg: str):
        print(f"Connection closed - Status: {close_status_code}, Message: {close_msg}")
```

#### 4. Dialog Manager

```python
class MultiModalConversation:
    """Multi-modal dialog manager"""
    
    def __init__(self, app_id: str, workspace_id: str, api_key: str, 
                 conversation_mode: str = "push2talk"):
        # Configure upstream parameters
        up_stream = Upstream(
            type="AudioOnly", 
            mode=conversation_mode, 
            audio_format="pcm"
        )
        
        # Configure client information
        client_info = ClientInfo(
            user_id="demo_user", 
            device=Device(uuid="demo_device")
        )
        
        # Configure request parameters
        request_params = RequestParameters(
            upstream=up_stream,
            downstream=Downstream(voice="longxiaochun_v2", sample_rate=48000),
            client_info=client_info
        )

        # Initialize dialog instance
        self.conversation = MultiModalDialog(
            app_id=app_id,
            workspace_id=workspace_id,
            url=WEBSOCKET_URL,
            request_params=request_params,
            multimodal_callback=ChatCallback(),
            api_key=api_key,
            model=MODEL
        )

    def start_conversation(self):
        """Start conversation"""
        self.conversation.start("")
        print("🎯 Conversation started")

    def send_audio_file(self, file_path: str):
        """Send audio file"""
        # Wait for listening state
        while self.conversation.get_dialog_state() != DialogState.LISTENING:
            time.sleep(0.1)
        
        # Start speech recognition
        self.conversation.start_speech()
        
        # Stream audio data
        with open(file_path, "rb") as f:
            while True:
                data = f.read(3200)
                if not data:
                    break
                self.conversation.send_audio_data(data)
                time.sleep(0.1)
        
        # Stop speech recognition (Push2Talk mode)
        if self.conversation.get_conversation_mode() == "push2talk":
            self.conversation.stop_speech()

    def stop_conversation(self):
        """Stop conversation"""
        self.conversation.stop()
        print("🛑 Conversation stopped")
```

#### 5. Complete Example

```python
import time

def main():
    """Main function"""
    print("🚀 Starting multi-modal dialog demo")
    
    # Configuration parameters
    config = {
        'app_id': "your_app_id",
        'workspace_id': "your_workspace_id",
        'api_key': "your_api_key",
        'conversation_mode': "push2talk"
    }
    
    # Validate configuration
    if not all([config['app_id'], config['workspace_id'], config['api_key']]):
        print("❌ Please configure app_id, workspace_id, and api_key")
        return
    
    try:
        # Create conversation instance
        conversation = MultiModalConversation(**config)
        
        # Start conversation
        conversation.start_conversation()
        
        # Send audio file
        conversation.send_audio_file("path/to/audio.wav")
        
        # Wait for processing completion
        time.sleep(10)
        
        # Stop conversation
        conversation.stop_conversation()
        
        print("✅ Demo completed")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
```

### Interaction Modes

#### 1. Push2Talk Mode
- **Features**: Press to talk, release to stop
- **Use Cases**: Precise control of recording timing
- **Implementation**: Manually call `start_speech()` and `stop_speech()`

#### 2. Tap2Talk Mode
- **Features**: Tap to start, automatic end detection
- **Use Cases**: Natural voice interaction
- **Implementation**: Only call `start_speech()`, system automatically detects end

#### 3. Duplex Mode
- **Features**: Full-duplex communication with interruption support
- **Use Cases**: Real-time dialog interaction
- **Implementation**: Send audio data directly without manual control


### Features

####  Visual Q&A (VQA) Feature
```python
from dashscope.multimodal.multimodal_request_params import RequestToRespondParameters

def test_image_vqa_url(conversation, image_url: str, question: str):
    """VQA using URL-based images"""
    # Build image parameters
    image = {"type": "url", "value": image_url}
    images_params = RequestToRespondParameters(images=[image])
    
    # Send VQA request
    conversation.request_to_respond("prompt", question, parameters=images_params)
```

#### Text-to-Speech (TTS) Feature

```python
# Send text synthesis request
        conversation.request_to_respond("transcript", "Hello, this is a test text.", None)
```

#### Image Question Answering (VQA) Feature

Call flow:
1. Text or voice request (e.g., "What's in front?")
2. Service returns "visual_qa" intent
3. Client executes photo capture task, uploads image URL or base64 data through request_to_respond interface (supports images under 180KB)
4. Returns image Q&A response
```
python3 run_vqa.py
```

#### Video Conversation (LiveAI) Feature

Call flow:
1. Set upstream request interaction type to "AudioAndVideo"
2. After receiving the first Listening signal, send voicechat_video_channel command with type "connect" (send_connect_video_command method in Demo)
3. Start sending video frame images at 500ms intervals, only supports base64 encoding (under 180KB) (send_video_frame_data_loop method in Demo)
4. Q1: Voice request "What's in the image?"
5. Returns description information
6. Q2: Voice request "What colors are there?"
7. Returns description information
```
python3 run_live_ai.py
```


### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
