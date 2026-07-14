from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


class EventType(str, Enum):
    SESSION_CREATED = "session.created"
    SESSION_UPDATED = "session.updated"

    RESPONSE_CREATED = "response.created"
    RESPONSE_DONE = "response.done"
    RESPONSE_AUDIO_DELTA = "response.audio.delta"
    RESPONSE_AUDIO_DONE = "response.audio.done"
    RESPONSE_AUDIO_TRANSCRIPT_DELTA = "response.audio_transcript.delta"
    RESPONSE_AUDIO_TRANSCRIPT_DONE = "response.audio_transcript.done"
    RESPONSE_TEXT_DELTA = "response.text.delta"
    RESPONSE_TEXT_DONE = "response.text.done"
    RESPONSE_FUNCTION_CALL_ARGS_DELTA = "response.function_call_arguments.delta"
    RESPONSE_FUNCTION_CALL_ARGS_DONE = "response.function_call_arguments.done"
    RESPONSE_OUTPUT_ITEM_ADDED = "response.output_item.added"
    RESPONSE_OUTPUT_ITEM_DONE = "response.output_item.done"

    INPUT_AUDIO_BUFFER_COMMITTED = "input_audio_buffer.committed"
    INPUT_AUDIO_BUFFER_CLEARED = "input_audio_buffer.cleared"
    INPUT_AUDIO_BUFFER_SPEECH_STARTED = "input_audio_buffer.speech_started"
    INPUT_AUDIO_BUFFER_SPEECH_STOPPED = "input_audio_buffer.speech_stopped"

    CONVERSATION_ITEM_CREATED = "conversation.item.created"
    CONVERSATION_ITEM_DELETED = "conversation.item.deleted"
    CONVERSATION_ITEM_TRUNCATED = "conversation.item.truncated"
    INPUT_AUDIO_TRANSCRIPTION_COMPLETED = "conversation.item.input_audio_transcription.completed"
    INPUT_AUDIO_TRANSCRIPTION_DELTA = "conversation.item.input_audio_transcription.delta"

    RESPONSE_CONTENT_PART_ADDED = "response.content_part.added"
    RESPONSE_CONTENT_PART_DONE = "response.content_part.done"

    ERROR = "error"
    UNKNOWN = "_unknown"


@dataclass
class TurnDetection:
    type: str = "smart_turn"
    threshold: float = 0.1
    silence_duration_ms: int = 1500

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class SessionConfig:
    modalities: List[str] = field(default_factory=lambda: ["text", "audio"])
    voice: str = "longanqian"
    instructions: str = ""
    input_audio_format: str = "pcm"
    output_audio_format: str = "pcm"
    turn_detection: Optional[TurnDetection] = None
    tools: List[dict] = field(default_factory=list)
    input_audio_transcription: Optional[dict] = None

    def to_dict(self) -> dict:
        d: Dict[str, Any] = {}
        d["modalities"] = self.modalities
        d["voice"] = self.voice
        d["instructions"] = self.instructions
        d["input_audio_format"] = self.input_audio_format
        d["output_audio_format"] = self.output_audio_format
        if self.turn_detection is not None:
            d["turn_detection"] = self.turn_detection.to_dict()
        else:
            d["turn_detection"] = None
        if self.tools:
            d["tools"] = self.tools
        if self.input_audio_transcription is not None:
            d["input_audio_transcription"] = self.input_audio_transcription
        return d


@dataclass
class FunctionCall:
    call_id: str
    name: str
    arguments: str

    def parse_arguments(self) -> dict:
        try:
            return json.loads(self.arguments) if self.arguments else {}
        except json.JSONDecodeError:
            return {}


@dataclass
class ServerEvent:
    type: EventType
    raw: Dict[str, Any]

    @staticmethod
    def from_dict(data: dict) -> ServerEvent:
        event_type_str = data.get("type", "")
        try:
            event_type = EventType(event_type_str)
        except ValueError:
            event_type = EventType.UNKNOWN
        return ServerEvent(type=event_type, raw=data)

    @property
    def audio_delta_b64(self) -> Optional[str]:
        if self.type == EventType.RESPONSE_AUDIO_DELTA:
            return self.raw.get("delta")
        return None

    @property
    def text_delta(self) -> Optional[str]:
        if self.type == EventType.RESPONSE_TEXT_DELTA:
            return self.raw.get("delta")
        return None

    @property
    def transcript_delta(self) -> Optional[str]:
        if self.type == EventType.RESPONSE_AUDIO_TRANSCRIPT_DELTA:
            return self.raw.get("delta")
        return None

    @property
    def function_call(self) -> Optional[FunctionCall]:
        if self.type == EventType.RESPONSE_FUNCTION_CALL_ARGS_DONE:
            return FunctionCall(
                call_id=self.raw.get("call_id", ""),
                name=self.raw.get("name", ""),
                arguments=self.raw.get("arguments", "{}"),
            )
        return None

    @property
    def response_id(self) -> Optional[str]:
        return self.raw.get("response_id") or self.raw.get("response", {}).get("id")

    @property
    def error(self) -> Optional[dict]:
        if self.type == EventType.ERROR:
            return self.raw.get("error", self.raw)
        return None

    @property
    def transcript(self) -> Optional[str]:
        if self.type == EventType.INPUT_AUDIO_TRANSCRIPTION_COMPLETED:
            return self.raw.get("transcript")
        return None
