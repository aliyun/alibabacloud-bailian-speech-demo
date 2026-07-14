from __future__ import annotations

import base64
import struct
from typing import Iterator

BYTES_PER_SAMPLE = 2  # 16-bit PCM


def pcm_to_base64(pcm_bytes: bytes) -> str:
    return base64.b64encode(pcm_bytes).decode()


def base64_to_pcm(b64_str: str) -> bytes:
    return base64.b64decode(b64_str)


def pcm_chunks(
    pcm_bytes: bytes,
    chunk_duration_s: float = 0.1,
    sample_rate: int = 16000,
) -> Iterator[bytes]:
    chunk_bytes = int(chunk_duration_s * sample_rate * BYTES_PER_SAMPLE)
    for i in range(0, len(pcm_bytes), chunk_bytes):
        yield pcm_bytes[i : i + chunk_bytes]


def read_wav_as_pcm(path: str, target_sample_rate: int = 16000) -> bytes:
    with open(path, "rb") as f:
        riff = f.read(4)
        if riff != b"RIFF":
            raise ValueError(f"Not a WAV file: {path}")
        f.read(4)  # file size
        wave = f.read(4)
        if wave != b"WAVE":
            raise ValueError(f"Not a WAV file: {path}")

        fmt_found = False
        channels = 1
        sample_rate = target_sample_rate
        bits_per_sample = 16
        data_bytes = b""

        while True:
            chunk_id = f.read(4)
            if len(chunk_id) < 4:
                break
            chunk_size = struct.unpack("<I", f.read(4))[0]

            if chunk_id == b"fmt ":
                fmt_data = f.read(chunk_size)
                audio_format = struct.unpack("<H", fmt_data[0:2])[0]
                if audio_format != 1:
                    raise ValueError(f"Unsupported audio format: {audio_format} (only PCM supported)")
                channels = struct.unpack("<H", fmt_data[2:4])[0]
                sample_rate = struct.unpack("<I", fmt_data[4:8])[0]
                bits_per_sample = struct.unpack("<H", fmt_data[14:16])[0]
                fmt_found = True
            elif chunk_id == b"data":
                data_bytes = f.read(chunk_size)
            else:
                f.read(chunk_size)

        if not fmt_found:
            raise ValueError(f"No fmt chunk found in: {path}")

        samples = []
        step = bits_per_sample // 8 * channels
        for i in range(0, len(data_bytes), step):
            sample_bytes = data_bytes[i : i + bits_per_sample // 8]
            if len(sample_bytes) < bits_per_sample // 8:
                break
            if bits_per_sample == 16:
                sample = struct.unpack("<h", sample_bytes)[0]
            elif bits_per_sample == 8:
                sample = (sample_bytes[0] - 128) * 256
            else:
                raise ValueError(f"Unsupported bits_per_sample: {bits_per_sample}")
            samples.append(sample)

        if sample_rate != target_sample_rate:
            ratio = target_sample_rate / sample_rate
            n_out = int(len(samples) * ratio)
            resampled = []
            for j in range(n_out):
                src_idx = j / ratio
                idx = int(src_idx)
                frac = src_idx - idx
                if idx + 1 < len(samples):
                    val = samples[idx] + (samples[idx + 1] - samples[idx]) * frac
                else:
                    val = samples[idx] if idx < len(samples) else 0
                val = max(-32768, min(32767, int(val)))
                resampled.append(val)
            samples = resampled

        return struct.pack(f"<{len(samples)}h", *samples)


def write_pcm_as_wav(path: str, pcm_bytes: bytes, sample_rate: int = 24000) -> None:
    data_size = len(pcm_bytes)
    byte_rate = sample_rate * BYTES_PER_SAMPLE
    with open(path, "wb") as f:
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + data_size))
        f.write(b"WAVE")
        f.write(b"fmt ")
        f.write(struct.pack("<I", 16))
        f.write(struct.pack("<H", 1))       # PCM
        f.write(struct.pack("<H", 1))       # mono
        f.write(struct.pack("<I", sample_rate))
        f.write(struct.pack("<I", byte_rate))
        f.write(struct.pack("<H", BYTES_PER_SAMPLE))
        f.write(struct.pack("<H", 16))      # bits per sample
        f.write(b"data")
        f.write(struct.pack("<I", data_size))
        f.write(pcm_bytes)
