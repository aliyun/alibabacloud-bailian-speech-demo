from __future__ import annotations

import json
import time
from typing import AsyncIterator, Optional

import websockets

from .audio import pcm_to_base64
from .types import EventType, ServerEvent, SessionConfig

DEFAULT_BASE_URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime"


class RealtimeClient:
    """qwen-audio-realtime WebSocket client.

    Handles: connection lifecycle, event serialization, session configuration.
    Does NOT handle: audio I/O, turn state machine, application logic.
    """

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        model: str = "",
        extra_headers: Optional[dict] = None,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.extra_headers = extra_headers or {}
        self._ws: Optional[websockets.WebSocketClientProtocol] = None

    async def connect(self) -> None:
        url = f"{self.base_url}?model={self.model}" if self.model else self.base_url
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            **self.extra_headers,
        }
        # websockets >= 14 names the header argument 'additional_headers',
        # earlier versions (>= 12) name it 'extra_headers'.
        try:
            self._ws = await websockets.connect(url, additional_headers=headers)
        except TypeError:
            self._ws = await websockets.connect(url, extra_headers=headers)

    async def close(self) -> None:
        if self._ws:
            await self._ws.close()
            self._ws = None

    async def __aenter__(self) -> RealtimeClient:
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    @property
    def closed(self) -> bool:
        return self._ws is None or self._ws.close_code is not None

    def _ensure_connected(self) -> websockets.WebSocketClientProtocol:
        if self._ws is None:
            raise RuntimeError("Not connected. Call connect() or use 'async with'.")
        return self._ws

    # ---- Send: low-level ----

    async def send_event(self, event: dict) -> None:
        ws = self._ensure_connected()
        if "event_id" not in event:
            event["event_id"] = f"evt_{int(time.time() * 1000)}"
        await ws.send(json.dumps(event))

    # ---- Send: session ----

    async def update_session(self, config: SessionConfig) -> None:
        await self.send_event({
            "type": "session.update",
            "session": config.to_dict(),
        })

    # ---- Send: audio input ----

    async def send_audio(self, pcm_bytes: bytes) -> None:
        await self.send_event({
            "type": "input_audio_buffer.append",
            "audio": pcm_to_base64(pcm_bytes),
        })

    async def send_audio_base64(self, audio_b64: str) -> None:
        await self.send_event({
            "type": "input_audio_buffer.append",
            "audio": audio_b64,
        })

    async def commit_audio_buffer(self) -> None:
        await self.send_event({"type": "input_audio_buffer.commit"})

    async def clear_audio_buffer(self) -> None:
        await self.send_event({"type": "input_audio_buffer.clear"})

    # ---- Send: response control ----

    async def create_response(self) -> None:
        await self.send_event({"type": "response.create"})

    async def cancel_response(self) -> None:
        await self.send_event({"type": "response.cancel"})

    # ---- Send: function call output ----

    async def send_function_output(
        self, call_id: str, output: str, *, trigger_response: bool = True
    ) -> None:
        await self.send_event({
            "type": "conversation.item.create",
            "item": {
                "type": "function_call_output",
                "call_id": call_id,
                "output": output,
            },
        })
        if trigger_response:
            await self.create_response()

    # ---- Receive ----

    async def recv(self) -> ServerEvent:
        ws = self._ensure_connected()
        raw_msg = await ws.recv()
        data = json.loads(raw_msg)
        return ServerEvent.from_dict(data)

    async def __aiter__(self) -> AsyncIterator[ServerEvent]:
        ws = self._ensure_connected()
        try:
            async for raw_msg in ws:
                data = json.loads(raw_msg)
                yield ServerEvent.from_dict(data)
        except websockets.exceptions.ConnectionClosed:
            return
