简体中文 | [English](README_EN.md)

# qwen-audio-realtime

**qwen-audio-realtime** API 的 Python SDK 与示例 —— 基于 WebSocket 的实时语音对话服务。

## 简介

qwen-audio-realtime 是一个基于 WebSocket 的实时语音对话服务。本仓库提供了一个轻量级的 Python SDK，以及若干示例应用，展示如何在其上构建语音智能体。

SDK（`fun_realtime/`）负责底层的 WebSocket 连接、事件序列化、会话配置和音频编解码工具。它有意保持精简 —— 没有轮次状态机，也没有内置路由器 —— 因此可以方便地集成到你自己的架构中。

示例应用（`demo_app/`）展示了三种常见模式：

- **陪伴对话**（`companion_chat.py`）：仅通过提示工程实现的个性化语音陪伴。
- **工具智能体**（`tool_agent.py`）：支持函数调用的语音智能体。
- **推理智能体**（`reasoning_agent.py`）：双模式路由，复杂问题会转交给外部推理流水线处理。

## 快速开始

### 安装 SDK

```bash
pip install -e .
```

SDK 仅依赖 `websockets`，无需音频硬件库。

### 配置

模型与 endpoint 统一集中在 [`demo_app/config.py`](demo_app/config.py) 中，三个场景的 instructions 统一集中在 [`demo_app/prompts.py`](demo_app/prompts.py) 中。你可以直接编辑文件，或通过环境变量覆盖：

> ⚠️ **必填项**：`DASHSCOPE_API_KEY` 与 `FUN_REALTIME_SPACE_ID` 必须设置，二者共同决定服务认证与请求 endpoint。 参考：[Dashscope 设置](https://help.aliyun.com/zh/model-studio/qwen-api-via-dashscope)

```bash
# 必填：API key
export DASHSCOPE_API_KEY=your-key

# 必填：百炼 space_id，会拼接为 wss://{space_id}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime
export FUN_REALTIME_SPACE_ID=your-bailian-space-id

# 可选：模型
export FUN_REALTIME_MODEL=qwen-audio-3.0-realtime-plus

# 可选：直接覆盖完整 endpoint（优先级高于 space_id）
export FUN_REALTIME_BASE_URL=wss://your-bailian-space-id.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime
```

Web 示例启动后会通过 `/api/prompts` 接口从 `prompts.py` 动态加载 instructions，修改 `prompts.py` 后刷新页面即可生效。

### 运行示例

```bash
# 示例额外依赖（麦克风/扬声器）
pip install pyaudio

# 场景 A：陪伴对话（最简单）
python3 -m demo_app.companion_chat

# 场景 B：工具智能体
python3 -m demo_app.tool_agent

# 场景 C：推理智能体
python3 -m demo_app.reasoning_agent

# Web 示例（浏览器端，包含全部三个场景）
python3 -m demo_app.web.server
# 打开 http://localhost:8080
```

## 项目结构

```
├── fun_realtime/              # SDK（pip install fun-realtime）
│   ├── client.py              # RealtimeClient：WebSocket 连接与事件 I/O
│   ├── types.py               # 事件类型、SessionConfig、TurnDetection
│   └── audio.py               # PCM ↔ Base64 编解码、WAV 读写
├── demo_app/                  # 应用示例
│   ├── companion_chat.py      # 场景 A：个性化陪伴对话
│   ├── tool_agent.py          # 场景 B：函数调用智能体
│   ├── reasoning_agent.py     # 场景 C：对话 + 推理双模式
│   ├── prompts.py             # 共享的系统提示约束与各场景 instructions
│   ├── config.py              # 模型与 endpoint 集中配置
│   ├── web/                   # 浏览器端示例
│   │   ├── server.py          # HTTP + WebSocket 代理，提供 /api/prompts
│   │   └── index.html         # 单页应用（3 个场景）
│   └── utils/
│       ├── mic_speaker.py     # 麦克风与扬声器（pyaudio）
│       └── audio_file.py      # 以 WAV 文件作为音频源（无需硬件）
├── pyproject.toml             # 包配置
└── requirements-demo.txt      # 示例额外依赖
```

## SDK 使用

SDK 有意保持轻量 —— 它只提供协议原语，而非一个 opinionated 的框架。

### 最小示例

```python
import asyncio
from fun_realtime import RealtimeClient, SessionConfig, TurnDetection, EventType

async def main():
    async with RealtimeClient(api_key="your-key", model="qwen-audio-3.0-realtime-plus") as client:
        await client.update_session(SessionConfig(
            instructions="You are a helpful assistant.",
            turn_detection=TurnDetection(type="smart_turn"),
        ))

        # 发送音频（来自任意来源的原始 PCM 字节）
        await client.send_audio(pcm_bytes)

        # 接收事件
        async for event in client:
            if event.type == EventType.RESPONSE_AUDIO_DELTA:
                audio_pcm = base64_to_pcm(event.audio_delta_b64)
                # ... 播放音频
            elif event.type == EventType.RESPONSE_FUNCTION_CALL_ARGS_DONE:
                fc = event.function_call
                result = my_function(fc.name, fc.parse_arguments())
                await client.send_function_output(fc.call_id, result)

asyncio.run(main())
```

### 核心 API

| 方法 | 说明 |
|------|------|
| `RealtimeClient(api_key, model, base_url)` | 创建客户端 |
| `client.connect()` / `async with client` | 打开 WebSocket |
| `client.update_session(SessionConfig)` | 配置会话（音色、提示词、工具、VAD） |
| `client.send_audio(pcm_bytes)` | 流式发送原始 PCM 音频 |
| `client.send_audio_base64(b64_str)` | 流式发送 Base64 编码的 PCM |
| `client.create_response()` | 手动触发一次回复 |
| `client.cancel_response()` | 取消当前回复 |
| `client.send_function_output(call_id, output)` | 返回函数调用结果 |
| `client.send_event(dict)` | 发送任意事件（逃生通道） |
| `async for event in client` | 迭代服务器事件 |
| `client.recv()` | 接收单个事件 |

### 音频工具

```python
from fun_realtime import pcm_to_base64, base64_to_pcm, read_wav_as_pcm, write_pcm_as_wav, pcm_chunks

# 读取 WAV 文件为 PCM（自动重采样到 16kHz）
pcm = read_wav_as_pcm("input.wav", target_sample_rate=16000)

# 切分为小块以实时发送
for chunk in pcm_chunks(pcm, chunk_duration_s=0.1):
    await client.send_audio(chunk)

# 保存接收到的音频
write_pcm_as_wav("output.wav", received_pcm, sample_rate=24000)
```

### Web 示例

```bash
export DASHSCOPE_API_KEY=your-key
python3 -m demo_app.web.server
# 打开 http://localhost:8080
```

浏览器端示例包含三个可切换的场景标签页、基于调度计划的音频播放、打断处理、客户端 VAD 延迟测量，以及工具调用可视化。

## 三种场景

### A. 陪伴对话（`companion_chat.py`）

纯提示工程 —— 配置一个角色人设即可开始对话。展示了最小的 SDK 使用面：连接、配置、发送音频、处理音频回复与打断。**约 50 行应用代码。**

### B. 工具智能体（`tool_agent.py`）

增加函数调用能力 —— 在 SessionConfig 中注册工具 schema，处理 `RESPONSE_FUNCTION_CALL_ARGS_DONE` 事件，调用本地函数，并通过 `send_function_output()` 返回结果。**约 80 行应用代码。**

### C. 推理智能体（`reasoning_agent.py`）

双模式路由 —— 简单问题由 realtime API 直接快速回复；复杂问题会被拦截、取消，并路由到外部推理流水线，最后将结果注入回当前会话。展示了 `cancel_response()`、用于任意协议操作的 `send_event()`，以及集成多智能体后端的模式。**约 100 行应用代码。**

## 设计哲学

- **SDK = 原语**：连接、事件、音频编解码。没有轮次状态机，没有内置路由器。
- **demo_app = 模式**：应用层逻辑放在这里，展示最佳实践，但不固化到 SDK 中。
- **逃生通道**：`send_event()` 允许你发送任意 WebSocket 消息；`ServerEvent.raw` 提供完整 JSON。SDK 不会限制高级用法。
