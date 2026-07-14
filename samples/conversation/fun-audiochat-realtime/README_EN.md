[简体中文](README.md) | English

# qwen-audio-realtime

Python SDK and examples for the **qwen-audio-realtime** API — a WebSocket-based real-time voice conversation service.

## Introduction

qwen-audio-realtime is a WebSocket-based real-time voice conversation service. This repository provides a thin Python SDK plus reference demo applications that show how to build voice agents on top of it.

The SDK (`fun_realtime/`) handles the low-level WebSocket connection, event serialization, session configuration, and audio codec utilities. It intentionally stays minimal — no turn state machine, no built-in router — so you can integrate it into your own architecture.

The demo apps (`demo_app/`) illustrate three common patterns:

- **Companion Chat** (`companion_chat.py`): a persona-driven voice companion using only prompt engineering.
- **Tool Agent** (`tool_agent.py`): a voice agent with function calling.
- **Reasoning Agent** (`reasoning_agent.py`): dual-mode routing that delegates complex questions to an external reasoning pipeline.

## Quick Start

### Install SDK

```bash
pip install -e .
```

The SDK depends only on `websockets` — no audio hardware libraries required.

### Configuration

Model and endpoint are centralized in [`demo_app/config.py`](demo_app/config.py), and scenario instructions are centralized in [`demo_app/prompts.py`](demo_app/prompts.py). Edit the files or override via environment variables:

> ⚠️ **Required**: both `DASHSCOPE_API_KEY` and `FUN_REALTIME_SPACE_ID` must be set; together they determine authentication and the request endpoint.

```bash
# Required: API key
export DASHSCOPE_API_KEY=your-key

# Required: Bailian space_id; endpoint is built as wss://{space_id}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime
export FUN_REALTIME_SPACE_ID=your-bailian-space-id

# Optional: model
export FUN_REALTIME_MODEL=qwen-audio-3.0-realtime-plus

# Optional: override the full endpoint directly (takes precedence over space_id)
export FUN_REALTIME_BASE_URL=wss://your-bailian-space-id.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime
```

The web demo loads instructions dynamically from `prompts.py` via the `/api/prompts` endpoint, so changes to `prompts.py` take effect after refreshing the page.

### Run a Demo

```bash
# Extra dependency for demos (microphone/speaker)
pip install pyaudio

# Scenario A: companion chat (simplest)
python3 -m demo_app.companion_chat

# Scenario B: tool-augmented agent
python3 -m demo_app.tool_agent

# Scenario C: chat + reasoning routing
python3 -m demo_app.reasoning_agent

# Web demo (browser-based, all three scenarios)
python3 -m demo_app.web.server
# Open http://localhost:8080
```

## Project Structure

```
├── fun_realtime/              # SDK (pip install fun-realtime)
│   ├── client.py              # RealtimeClient: WebSocket connection + event I/O
│   ├── types.py               # Event types, SessionConfig, TurnDetection
│   └── audio.py               # PCM ↔ Base64 codec, WAV read/write
├── demo_app/                  # Application examples
│   ├── companion_chat.py      # Scenario A: persona-driven companion
│   ├── tool_agent.py          # Scenario B: agent with function calling
│   ├── reasoning_agent.py     # Scenario C: chat + reasoning dual-mode
│   ├── prompts.py             # Shared system prompt constraints and scenario instructions
│   ├── config.py              # Centralized model and endpoint configuration
│   ├── web/                   # Browser-based demo
│   │   ├── server.py          # HTTP + WebSocket proxy, serves /api/prompts
│   │   └── index.html         # Single-page app (3 scenarios)
│   └── utils/
│       ├── mic_speaker.py     # Microphone & speaker (pyaudio)
│       └── audio_file.py      # WAV file as audio source (no hardware needed)
├── pyproject.toml             # Package config
└── requirements-demo.txt      # Extra deps for demos
```

## SDK Usage

The SDK is intentionally thin — it provides protocol primitives, not an opinionated framework.

### Minimal Example

```python
import asyncio
from fun_realtime import RealtimeClient, SessionConfig, TurnDetection, EventType

async def main():
    async with RealtimeClient(api_key="your-key", model="qwen-audio-3.0-realtime-plus") as client:
        await client.update_session(SessionConfig(
            instructions="You are a helpful assistant.",
            turn_detection=TurnDetection(type="smart_turn"),
        ))

        # Send audio (raw PCM bytes from any source)
        await client.send_audio(pcm_bytes)

        # Receive events
        async for event in client:
            if event.type == EventType.RESPONSE_AUDIO_DELTA:
                audio_pcm = base64_to_pcm(event.audio_delta_b64)
                # ... play audio
            elif event.type == EventType.RESPONSE_FUNCTION_CALL_ARGS_DONE:
                fc = event.function_call
                result = my_function(fc.name, fc.parse_arguments())
                await client.send_function_output(fc.call_id, result)

asyncio.run(main())
```

### Key API

| Method | Description |
|--------|-------------|
| `RealtimeClient(api_key, model, base_url)` | Create client |
| `client.connect()` / `async with client` | Open WebSocket |
| `client.update_session(SessionConfig)` | Configure session (voice, instructions, tools, VAD) |
| `client.send_audio(pcm_bytes)` | Stream raw PCM audio |
| `client.send_audio_base64(b64_str)` | Stream base64-encoded PCM |
| `client.create_response()` | Manually trigger a response |
| `client.cancel_response()` | Cancel current response |
| `client.send_function_output(call_id, output)` | Return function call result |
| `client.send_event(dict)` | Send arbitrary event (escape hatch) |
| `async for event in client` | Iterate over server events |
| `client.recv()` | Receive single event |

### Audio Utilities

```python
from fun_realtime import pcm_to_base64, base64_to_pcm, read_wav_as_pcm, write_pcm_as_wav, pcm_chunks

# Read WAV file as PCM (auto-resample to 16kHz)
pcm = read_wav_as_pcm("input.wav", target_sample_rate=16000)

# Split into chunks for real-time sending
for chunk in pcm_chunks(pcm, chunk_duration_s=0.1):
    await client.send_audio(chunk)

# Save received audio
write_pcm_as_wav("output.wav", received_pcm, sample_rate=24000)
```

### Web Demo

```bash
export DASHSCOPE_API_KEY=your-key
python3 -m demo_app.web.server
# Open http://localhost:8080
```

Browser-based demo with all three scenarios as switchable tabs, schedule-based audio playback, interruption handling, client-side VAD latency measurement, and tool call visualization.

## Three Scenarios

### A. Companion Chat (`companion_chat.py`)

Pure prompt engineering — configure a persona and start talking. Demonstrates the minimal SDK surface: connect, configure, send audio, handle audio responses and interruptions. **~50 lines of application code.**

### B. Tool Agent (`tool_agent.py`)

Adds function calling — register tool schemas in SessionConfig, handle `RESPONSE_FUNCTION_CALL_ARGS_DONE` events, call local functions, return results via `send_function_output()`. **~80 lines of application code.**

### C. Reasoning Agent (`reasoning_agent.py`)

Dual-mode routing — simple questions get fast direct replies from the realtime API; complex questions are intercepted, cancelled, routed to an external reasoning pipeline, and the result is injected back into the session. Demonstrates `cancel_response()`, `send_event()` for arbitrary protocol operations, and the pattern for integrating multi-agent backends. **~100 lines of application code.**

## Design Philosophy

- **SDK = primitives**: connection, events, audio codec. No turn state machine, no built-in router.
- **demo_app = patterns**: application-level logic lives here, showing best practices without baking them into the SDK.
- **Escape hatch**: `send_event()` lets you send any WebSocket message. `ServerEvent.raw` gives you the full JSON. The SDK never blocks advanced use cases.
