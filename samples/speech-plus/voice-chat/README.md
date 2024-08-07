
[comment]: # (title and brief introduction of the sample)
## 语音对话聊天
语音对话聊天(Voice Chat)是目前最火热、最前沿的语音交互方式。通过结合文本大模型的语音理解能力，实现语音进语音的沟通交流。

[comment]: # (list of scenarios of the sample)
### :point_right: 适用场景

| 应用场景         | 典型用法   | 使用说明                |
|--------------|--------|---------------------|
| **语音对话聊天场景** | 语音对话聊天 | *通过语音与大语言模型进行对话聊天*  |
| **虚拟人直播**    | 虚拟人语音直播  | *通过语音与大语言模型与用户连麦对话* |


## Python

[comment]: # (prerequisites)
### :point_right: 前提条件

1. #### 配置阿里云百炼API-KEY

    在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

1. #### 安装Python依赖

    阿里云百炼SDK运行环境需要Python 3.8及以上版本。您可以使用以下命令来安装本示例的依赖：
    ```commandline
    pip3 install -r requirements.txt
    ```

[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例


```commandline
python3 voice_chat_demo.py
```

本示例提供了一个简化的GUI 界面，用来触发交互。点击button后，会自动调用百炼SDK的接口，实现语音交互。

<img src="../../../docs/image/voice-chat.png" width="400"/>

本示例调用了实时语音识别服务，通过检测SpeechEnd来实现语音自动判停。示例UI会block等待识别结束，允许下一次点击收音。

程序调用过程为：

<img src="../../../docs/image/voice-chat-sequence.png" width="400"/>


**请注意：** 
- 回调方式：
    
  示例展示的是一种简单的调用过程，为了方便演示，识别结束的回调通过Event通知主线程，故主线程会block等待识别结束。 在您的实际应用中，请根据实际情况选择合适的回调方式。

  或者您可以不使用自动的方式结束录音和识别，而通过主动触发的方式实施。
  - 录音和播放：
    
      为了方便演示，示例中集成了简单的录音和播放功能。您可以灵活在业务中进行调整，比如通过流的方式从您的客户端输入输出流式音频。


[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../docs/image/groups.png" width="400"/>
