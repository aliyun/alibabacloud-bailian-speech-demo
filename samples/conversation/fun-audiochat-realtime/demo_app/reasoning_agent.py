"""Scenario C: Chat + Reasoning dual-mode Voice Agent.

The model itself decides routing via function calling:
- Simple questions → direct voice reply (low latency)
- Complex questions → model calls `deep_thinking` tool, speaks a filler phrase
  ("好的，让我仔细想想") while the reasoning pipeline runs in the background,
  then replies with the result.

Usage:
    export DASHSCOPE_API_KEY=your-key
    python -m demo_app.reasoning_agent
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fun_realtime import EventType, RealtimeClient, SessionConfig, TurnDetection
from demo_app.config import DEFAULT_BASE_URL, DEFAULT_MODEL
from demo_app.prompts import REASONING_INSTRUCTIONS
from demo_app.utils.mic_speaker import MicrophoneStream, Speaker

# ---- Tool: deep_thinking ----

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "deep_thinking",
            "description": (
                "当用户的问题需要深度分析、多步推理、对比权衡、或综合规划时，"
                "调用此工具进行深度思考。简单的闲聊、问候、事实性问答不需要调用。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用户提出的需要深度分析的完整问题",
                    },
                },
                "required": ["query"],
            },
        },
    },
]

async def reasoning_pipeline(query: str) -> str:
    """Simulated external multi-agent reasoning pipeline.

    In production, replace with your reasoning backend:
    planning agent → search/retrieval agents → synthesis agent.
    """
    await asyncio.sleep(2)
    return (
        f"经过深度分析，关于「{query}」："
        f"这个问题需要从多个维度综合考虑。"
        f"核心建议是从实际需求出发，权衡短期成本与长期收益，"
        f"优先选择可验证、可迭代的方案。"
    )


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
            instructions=REASONING_INSTRUCTIONS,
            turn_detection=TurnDetection(type="smart_turn"),
            tools=TOOLS,
        ))
        print("Connected! Simple → direct reply, complex → deep_thinking tool.")

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
                    resp_id = event.response_id or ""
                    print(f"\n[turn {turn_count}] response_id={resp_id}")

                elif event.type == EventType.RESPONSE_AUDIO_DELTA:
                    speaker.play(event.audio_delta_b64)

                elif event.type == EventType.INPUT_AUDIO_BUFFER_SPEECH_STARTED:
                    speaker.cancel()

                elif event.type == EventType.RESPONSE_FUNCTION_CALL_ARGS_DONE:
                    fc = event.function_call
                    if fc.name == "deep_thinking":
                        query = fc.parse_arguments().get("query", "")
                        print(f"[deep_thinking] query: {query}")
                        print("[deep_thinking] reasoning pipeline running...")

                        result = await reasoning_pipeline(query)
                        print(f"[deep_thinking] result: {result}")

                        await client.send_function_output(fc.call_id, result)
                    else:
                        await client.send_function_output(
                            fc.call_id, f"Unknown tool: {fc.name}"
                        )

                elif event.type == EventType.RESPONSE_AUDIO_TRANSCRIPT_DELTA:
                    print(event.transcript_delta, end="", flush=True)

                elif event.type == EventType.RESPONSE_DONE:
                    print()

                elif event.type == EventType.INPUT_AUDIO_TRANSCRIPTION_COMPLETED:
                    print(f"[You]: {event.transcript}")

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
        print(f"\nBye!")
