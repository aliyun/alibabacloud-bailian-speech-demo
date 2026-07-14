from __future__ import annotations

import asyncio
from typing import AsyncIterator

from fun_realtime import read_wav_as_pcm, pcm_chunks


class AudioFileStream:
    """Async iterator that yields PCM chunks from a WAV file at real-time pace.

    Simulates microphone input for testing without audio hardware.

    Usage:
        stream = AudioFileStream("test.wav")
        async for chunk in stream:
            await client.send_audio(chunk)
    """

    def __init__(
        self,
        wav_path: str,
        sample_rate: int = 16000,
        chunk_duration_s: float = 0.1,
    ):
        self._pcm = read_wav_as_pcm(wav_path, target_sample_rate=sample_rate)
        self._chunk_duration = chunk_duration_s
        self._sample_rate = sample_rate

    async def __aiter__(self) -> AsyncIterator[bytes]:
        for chunk in pcm_chunks(self._pcm, self._chunk_duration, self._sample_rate):
            yield chunk
            await asyncio.sleep(self._chunk_duration)
