"""Scenario B: Tool-augmented Voice Agent.

Voice agent with function calling — demonstrates how to register tools,
handle function_call events, and return results to the model.

Usage:
    export DASHSCOPE_API_KEY=your-key
    python -m demo_app.tool_agent
"""

import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fun_realtime import EventType, RealtimeClient, SessionConfig, TurnDetection
from demo_app.config import DEFAULT_BASE_URL, DEFAULT_MODEL
from demo_app.prompts import BASE_CONSTRAINTS, TOOL_INSTRUCTIONS
from demo_app.utils.mic_speaker import MicrophoneStream, Speaker

# ---- Tool definitions (schema for session.update) ----

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Query weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name, e.g. 北京、上海",
                    },
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_train_price",
            "description": "Query train ticket price between two cities.",
            "parameters": {
                "type": "object",
                "properties": {
                    "src": {"type": "string", "description": "Departure city"},
                    "dst": {"type": "string", "description": "Arrival city"},
                },
                "required": ["src", "dst"],
            },
        },
    },
]

# ---- Tool implementations (local functions) ----


def get_weather(city: str) -> str:
    return f"{city}今天多云转晴，气温 18-26°C，微风。"


def get_train_price(src: str, dst: str) -> str:
    price = abs(hash(src + dst)) % 500 + 50
    return f"从{src}到{dst}的动车二等座票价约 ¥{price}，具体以 12306 为准。"


FUNCTIONS = {
    "get_weather": get_weather,
    "get_train_price": get_train_price,
}


async def main():
    api_key = os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("REALTIME_API_KEY", "")
    if not api_key:
        print("Error: set DASHSCOPE_API_KEY (or REALTIME_API_KEY)")
        return

    speaker = Speaker()
    session_id = ""
    turn_count = 0

    async with RealtimeClient(api_key=api_key, model=DEFAULT_MODEL, base_url=DEFAULT_BASE_URL) as client:
        await client.update_session(SessionConfig(
            instructions=TOOL_INSTRUCTIONS,
            turn_detection=TurnDetection(type="smart_turn"),
            tools=TOOLS,
        ))
        print("Connected! Ask about weather or train tickets...")

        async def send_mic():
            mic = MicrophoneStream()
            async for chunk in mic:
                if client.closed:
                    break
                await client.send_audio(chunk)

        async def handle_events():
            nonlocal session_id, turn_count

            async for event in client:
                if event.type == EventType.SESSION_CREATED:
                    session_id = event.raw.get("session", {}).get("id", "")
                    print(f"[session] id={session_id}")
                elif event.type == EventType.RESPONSE_CREATED:
                    turn_count += 1
                    print(f"\n[turn {turn_count}] response_id={event.response_id}")
                elif event.type == EventType.RESPONSE_AUDIO_DELTA:
                    speaker.play(event.audio_delta_b64)

                elif event.type == EventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED:
                    speaker.cancel()

                elif event.type == EventType.RESPONSE_FUNCTION_CALL_ARGS_DONE:
                    fc = event.function_call
                    print(f"[Tool Call] {fc.name}({fc.arguments})")
                    func = FUNCTIONS.get(fc.name)
                    if func:
                        result = func(**fc.parse_arguments())
                    else:
                        result = f"Unknown function: {fc.name}"
                    print(f"[Tool Result] {result}")
                    await client.send_function_output(fc.call_id, result)

                elif event.type == EventType.RESPONSE_AUDIO_TRANSCRIPT_DELTA:
                    print(event.transcript_delta, end="", flush=True)

                elif event.type == EventType.RESPONSE_DONE:
                    print()

                elif event.type == EventType.INPUT_AUDIO_TRANSCRIPTION_COMPLETED:
                    print(f"\n[You]: {event.transcript}")

                elif event.type == EventType.ERROR:
                    print(f"[Error]: {event.error}")

        try:
            await asyncio.gather(send_mic(), handle_events())
        finally:
            speaker.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBye!")
