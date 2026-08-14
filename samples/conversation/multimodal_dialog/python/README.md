# 多模态对话示例
简体中文 | [English](./README_EN.md)


### :point_right: 前置条件

1. #### 配置阿里云百炼 API-KEY

    在运行此示例之前，您需要激活阿里云账户，获取阿里云百炼 API_KEY，并进行必要的环境配置。有关 API-KEY 的详细配置步骤，请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### 开启多模态对话服务
    在运行此示例之前，您需要在多模交互服务管控台开通多模态对话服务。并在控制台中创建应用并进行必要配置，发布应用。同时获取 app_id、workspace_id 和 api_key。

3. #### 安装 Python 依赖

    阿里云百炼 SDK 运行环境需要 Python 3.9 或更高版本。您可以使用以下命令安装此示例的依赖项：
    ```commandline
    pip3 install -r requirements.txt
    ```

### :point_right: 运行示例
请修改示例以填入必要的 app_id、workspace_id 和 api_key。您可以使用以下命令运行此示例：

```commandline
export DASHSCOPE_LOGGING_LEVEL='info' # 启用 dashscope SDK 内部日志
python3 run.py
```
示例默认使用 Push2talk 模式调用服务，读取语音文件"1加1等于多少"的音频识别并回复文本和音频回复。

### 快速集成

#### 1. 安装依赖

```bash
pip install dashscope
```

#### 2. 基础配置

```python
from dashscope.multimodal.dialog_state import DialogState
from dashscope.multimodal.multimodal_dialog import MultiModalDialog, MultiModalCallback
from dashscope.multimodal.multimodal_request_params import (
    Upstream, Downstream, ClientInfo, RequestParameters, Device
)

# 配置参数
WORKSPACE_ID = "your_workspace_id"
APP_ID = "your_app_id"
API_KEY = "your_api_key"
MODEL = "multimodal-dialog"
WEBSOCKET_URL = "wss://dashscope.aliyuncs.com/api-ws/v1/inference"
```

#### 3. 实现回调处理器

```python
class ChatCallback(MultiModalCallback):
    """对话回调处理器"""
    
    def on_connected(self):
        print("✅ WebSocket 连接已建立")

    def on_started(self, dialog_id: str):
        print(f"对话已开始，ID: {dialog_id}")

    def on_state_changed(self, state: DialogState):
        state_messages = {
            DialogState.LISTENING: "👂 系统正在监听...",
            DialogState.THINKING: "🤔 AI 正在思考...",
            DialogState.RESPONDING: "💬 AI 正在回应..."
        }
        print(state_messages.get(state, f"状态变更: {state}"))

    def on_speech_audio_data(self, data: bytes):
        print(f"接收到音频数据: {len(data)} 字节")

    def on_error(self, error: Exception):
        print(f"❌ 错误: {error}")

    def on_close(self, close_status_code: int, close_msg: str):
        print(f"连接已关闭 - 状态: {close_status_code}, 消息: {close_msg}")
```

#### 4. 对话管理器

```python
class MultiModalConversation:
    """多模态对话管理器"""
    
    def __init__(self, app_id: str, workspace_id: str, api_key: str, 
                 conversation_mode: str = "push2talk"):
        # 配置上行参数
        up_stream = Upstream(
            type="AudioOnly", 
            mode=conversation_mode, 
            audio_format="pcm"
        )
        
        # 配置客户端信息
        client_info = ClientInfo(
            user_id="demo_user", 
            device=Device(uuid="demo_device")
        )
        
        # 配置请求参数
        request_params = RequestParameters(
            upstream=up_stream,
            downstream=Downstream(voice="longxiaochun_v2", sample_rate=48000),
            client_info=client_info
        )

        # 初始化对话实例
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
        """开始对话"""
        self.conversation.start("")
        print("🎯 对话已开始")

    def send_audio_file(self, file_path: str):
        """发送音频文件"""
        # 等待监听状态
        while self.conversation.get_dialog_state() != DialogState.LISTENING:
            time.sleep(0.1)
        
        # 开始语音识别
        self.conversation.start_speech()
        
        # 流式发送音频数据
        with open(file_path, "rb") as f:
            while True:
                data = f.read(3200)
                if not data:
                    break
                self.conversation.send_audio_data(data)
                time.sleep(0.1)
        
        # 停止语音识别（Push2Talk 模式）
        if self.conversation.get_conversation_mode() == "push2talk":
            self.conversation.stop_speech()

    def stop_conversation(self):
        """停止对话"""
        self.conversation.stop()
        print("🛑 对话已停止")
```

#### 5. 完整示例

```python
import time

def main():
    """主函数"""
    print("🚀 启动多模态对话演示")
    
    # 配置参数
    config = {
        'app_id': "your_app_id",
        'workspace_id': "your_workspace_id",
        'api_key': "your_api_key",
        'conversation_mode': "push2talk"
    }
    
    # 验证配置
    if not all([config['app_id'], config['workspace_id'], config['api_key']]):
        print("❌ 请配置 app_id、workspace_id 和 api_key")
        return
    
    try:
        # 创建对话实例
        conversation = MultiModalConversation(**config)
        
        # 开始对话
        conversation.start_conversation()
        
        # 发送音频文件
        conversation.send_audio_file("path/to/audio.wav")
        
        # 等待处理完成
        time.sleep(10)
        
        # 停止对话
        conversation.stop_conversation()
        
        print("✅ 演示完成")
        
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == '__main__':
    main()
```

### 交互模式

#### 1. Push2Talk 模式
- **特点**: 按下说话，松开停止
- **适用场景**: APP或者玩具通过按钮说话
- **实现方式**: 手动调用 `start_speech()` 和 `stop_speech()`


#### 2. Tap2Talk 模式
- **特点**: 点击开始，自动结束检测
- **适用场景**: 支持唤醒的场景，或者按键开始
- **实现方式**: 只调用 `start_speech()`，系统自动检测结束

#### 3. Duplex 模式
- **特点**: 全双工通信，支持打断
- **适用场景**: 实时对话交互
- **实现方式**: 直接发送音频数据，无需手动控制

### 功能特性

#### 文本转语音（TTS）功能

```python
# 发送文本合成请求
conversation.request_to_respond("transcript", "你好，这是一段测试文本。", None)
```

#### 图片问答 (VQA) 功能
调用流程：
1. 文本或语音请求（例如：看看前面是什么）
2. 服务返回"visual_qa" 意图
3. 端侧执行拍照任务，通过request_to_respond接口上传图片url或者base64数据（支持180KB以下图片大小）
4. 返回图片问答回复
``` 
python3 run_vqa.py
```

#### 视频对话（LiveAI）功能
调用流程：
1. 设置上行请求交互类型为"AudioAndVideo"
2. 在第一次接收到Listening信号之后，发送voicechat_video_channel 执行，类型为connect（Demo中send_connect_video_command方法）
3. 开始间隔500ms发送视频帧图片，仅支持base64编码（180KB以下）（Demo中send_video_frame_data_loop方法）

4. Q1：语音请求"看一下图像中有什么东西"
5. 返回描述信息
6. Q2：语音请求"看一下都是什么颜色"
7. 返回描述信息
``` 
python3 run_live_ai.py
```


### :point_right: 技术支持
<img src="../../../../docs/image/group.png" width="400"/>
