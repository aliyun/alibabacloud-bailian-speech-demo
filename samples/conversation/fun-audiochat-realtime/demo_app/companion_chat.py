"""Scenario A: Companion Chat — simplest usage of the SDK.

A persona-driven voice companion using only prompt engineering.
No tools, no routing — just real-time voice conversation.

Usage:
    export DASHSCOPE_API_KEY=your-key
    python -m demo_app.companion_chat
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fun_realtime import EventType, RealtimeClient, SessionConfig, TurnDetection
from demo_app.config import DEFAULT_BASE_URL, DEFAULT_MODEL
from demo_app.prompts import COMPANION_INSTRUCTIONS
from demo_app.utils.mic_speaker import MicrophoneStream, Speaker


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
            voice="longanqian",
            instructions=COMPANION_INSTRUCTIONS,
            turn_detection=TurnDetection(type="smart_turn"),
        ))
        print("Connected! Start speaking...")

        async def send_mic():
            mic = MicrophoneStream()
            async for chunk in mic:
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
