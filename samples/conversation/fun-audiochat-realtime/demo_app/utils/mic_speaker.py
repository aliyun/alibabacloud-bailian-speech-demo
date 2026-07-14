from __future__ import annotations

import asyncio
import base64
import contextlib
import queue
import threading
from typing import AsyncIterator

import pyaudio


class MicrophoneStream:
    """Async iterator that yields PCM bytes from the microphone.

    Usage:
        mic = MicrophoneStream()
        async for chunk in mic:
            await client.send_audio(chunk)
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        chunk_duration_s: float = 0.1,
        channels: int = 1,
    ):
        self._sample_rate = sample_rate
        self._chunk_samples = int(sample_rate * chunk_duration_s)
        self._channels = channels
        self._running = True
        self._pya = pyaudio.PyAudio()
        self._stream = self._pya.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=sample_rate,
            input=True,
        )

    def stop(self) -> None:
        self._running = False

    async def __aiter__(self) -> AsyncIterator[bytes]:
        try:
            while self._running:
                data = await asyncio.to_thread(
                    self._stream.read, self._chunk_samples, False
                )
                yield data
                await asyncio.sleep(0)
        finally:
            self._stream.stop_stream()
            self._stream.close()
            self._pya.terminate()


class Speaker:
    """Audio playback with base64 PCM input and interruption support.

    Usage:
        speaker = Speaker()
        speaker.play(audio_b64)   # feed base64 encoded PCM
        speaker.cancel()          # interrupt (clear buffer)
        speaker.shutdown()        # clean up
    """

    def __init__(self, sample_rate: int = 24000, chunk_size_ms: int = 100):
        self._pya = pyaudio.PyAudio()
        self._sample_rate = sample_rate
        self._chunk_bytes = chunk_size_ms * sample_rate * 2 // 1000
        self._stream = self._pya.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=sample_rate,
            output=True,
        )
        self._b64_queue: queue.Queue[str] = queue.Queue()
        self._pcm_queue: queue.Queue[bytes] = queue.Queue()
        self._running = True

        self._decoder_thread = threading.Thread(target=self._decode_loop, daemon=True)
        self._player_thread = threading.Thread(target=self._play_loop, daemon=True)
        self._decoder_thread.start()
        self._player_thread.start()

    def _decode_loop(self) -> None:
        while self._running:
            b64_data = None
            with contextlib.suppress(queue.Empty):
                b64_data = self._b64_queue.get(timeout=0.1)
            if b64_data is None:
                continue
            raw = base64.b64decode(b64_data)
            for i in range(0, len(raw), self._chunk_bytes):
                self._pcm_queue.put(raw[i : i + self._chunk_bytes])

    def _play_loop(self) -> None:
        while self._running:
            pcm_data = None
            with contextlib.suppress(queue.Empty):
                pcm_data = self._pcm_queue.get(timeout=0.1)
            if pcm_data is not None:
                self._stream.write(pcm_data)

    def play(self, audio_b64: str) -> None:
        self._b64_queue.put(audio_b64)

    def cancel(self) -> None:
        self._b64_queue.queue.clear()
        self._pcm_queue.queue.clear()

    def shutdown(self) -> None:
        self._running = False
        self._decoder_thread.join(timeout=2)
        self._player_thread.join(timeout=2)
        self._stream.close()
        self._pya.terminate()
