import asyncio
import importlib.util
import queue
import sys
import threading
import types
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_websocket_proxy_finishes_when_upstream_closes(monkeypatch):
    sample_root = REPO_ROOT / "samples/conversation/fun-audiochat-realtime"
    monkeypatch.syspath_prepend(str(sample_root))
    server = load_module(
        "fun_audiochat_web_server_test",
        sample_root / "demo_app/web/server.py",
    )
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")

    class Browser:
        def __init__(self):
            self.request = types.SimpleNamespace(path="/ws?model=qwen-audio-3.1-realtime-plus")
            self.closed = False

        def __aiter__(self):
            return self

        async def __anext__(self):
            await asyncio.Future()

        async def send(self, message):
            pass

        async def close(self):
            self.closed = True

    class Upstream:
        def __init__(self):
            self.closed = False

        def __aiter__(self):
            return self

        async def __anext__(self):
            raise StopAsyncIteration

        async def send(self, message):
            pass

        async def close(self):
            self.closed = True

    class Connection:
        def __init__(self, upstream):
            self.upstream = upstream

        async def __aenter__(self):
            return self.upstream

        async def __aexit__(self, exc_type, exc, tb):
            await self.upstream.close()

    browser = Browser()
    upstream = Upstream()
    monkeypatch.setattr(
        server.websockets,
        "connect",
        lambda *args, **kwargs: Connection(upstream),
    )

    asyncio.run(asyncio.wait_for(server.ws_proxy(browser), timeout=1.0))

    assert browser.closed
    assert upstream.closed


def test_asyncio_tts_propagates_worker_failure(monkeypatch, tmp_path):
    dashscope = types.ModuleType("dashscope")
    dashscope.Client = object
    monkeypatch.setitem(sys.modules, "dashscope", dashscope)
    module = load_module(
        "asyncio_tts_test",
        REPO_ROOT
        / "samples/speech-synthesizer/synthesize_speech_from_text_using_asyncio/python/run.py",
    )
    monkeypatch.chdir(tmp_path)

    class FailingClient:
        def __init__(self, **kwargs):
            pass

        def __enter__(self):
            raise RuntimeError("worker failed")

        def __exit__(self, exc_type, exc, tb):
            pass

    monkeypatch.setattr(module, "Client", FailingClient)

    async def run():
        await asyncio.wait_for(
            module.synthesis_text_to_speech_using_asyncio(["hello"]),
            timeout=1.0,
        )

    with pytest.raises(RuntimeError, match="worker failed"):
        asyncio.run(run())


def test_subtitle_player_drains_text_after_audio_ends(monkeypatch):
    wx = types.ModuleType("wx")
    wx.Frame = object
    wx_richtext = types.ModuleType("wx.richtext")
    wx.richtext = wx_richtext
    dashscope = types.ModuleType("dashscope")
    dashscope.Client = object
    player_module = types.ModuleType("RealtimeMp3Player")
    player_module.RealtimeMp3Player = object
    monkeypatch.setitem(sys.modules, "wx", wx)
    monkeypatch.setitem(sys.modules, "wx.richtext", wx_richtext)
    monkeypatch.setitem(sys.modules, "dashscope", dashscope)
    monkeypatch.setitem(sys.modules, "RealtimeMp3Player", player_module)

    module = load_module(
        "subtitle_player_test",
        REPO_ROOT / "samples/gallery/read-and-display-subtitles/python/run.py",
    )
    subtitle_player = module.SubtitlePlayer.__new__(module.SubtitlePlayer)
    subtitle_player.task_lock = threading.Lock()
    subtitle_player.queue_lock = threading.Lock()
    subtitle_player.stop_task = True
    subtitle_player.audio_queue = [[True, None]]
    subtitle_player.text_queue = [[False, "tail"], [True, None]]
    subtitle_player.player = types.SimpleNamespace(write=lambda audio: None)
    rendered = []
    refreshed = []
    subtitle_player.add_text_to_label = rendered.append
    subtitle_player.wait_and_refresh_player = lambda: refreshed.append(True)

    worker = threading.Thread(target=subtitle_player.run, daemon=True)
    worker.start()
    worker.join(timeout=1.0)

    assert not worker.is_alive()
    assert rendered == ["tail", "\n"]
    assert refreshed == [True]


def test_subtitle_player_stops_with_unmatched_tail(monkeypatch):
    wx = types.ModuleType("wx")
    wx.Frame = object
    wx_richtext = types.ModuleType("wx.richtext")
    wx.richtext = wx_richtext
    dashscope = types.ModuleType("dashscope")
    dashscope.Client = object
    player_module = types.ModuleType("RealtimeMp3Player")
    player_module.RealtimeMp3Player = object
    monkeypatch.setitem(sys.modules, "wx", wx)
    monkeypatch.setitem(sys.modules, "wx.richtext", wx_richtext)
    monkeypatch.setitem(sys.modules, "dashscope", dashscope)
    monkeypatch.setitem(sys.modules, "RealtimeMp3Player", player_module)

    module = load_module(
        "subtitle_player_unmatched_tail_test",
        REPO_ROOT / "samples/gallery/read-and-display-subtitles/python/run.py",
    )
    subtitle_player = module.SubtitlePlayer.__new__(module.SubtitlePlayer)
    subtitle_player.task_lock = threading.Lock()
    subtitle_player.queue_lock = threading.Lock()
    subtitle_player.stop_task = True
    subtitle_player.audio_queue = [[False, b"tail"]]
    subtitle_player.text_queue = []

    worker = threading.Thread(target=subtitle_player.run, daemon=True)
    worker.start()
    worker.join(timeout=1.0)

    assert not worker.is_alive()


def test_tts_worker_times_out_when_receiver_does_not_stop(monkeypatch, tmp_path):
    dashscope = types.ModuleType("dashscope")
    dashscope.Client = object
    monkeypatch.setitem(sys.modules, "dashscope", dashscope)
    module = load_module(
        "asyncio_tts_stuck_receiver_test",
        REPO_ROOT
        / "samples/speech-synthesizer/synthesize_speech_from_text_using_asyncio/python/run.py",
    )
    monkeypatch.setattr(module, "RECEIVER_JOIN_TIMEOUT_SECONDS", 0.01, raising=False)
    release = threading.Event()

    class Session:
        def __init__(self):
            self.session = types.SimpleNamespace(request_id="request-id")
            self.first_package_delay = 0
            self.closed = False

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

        def audio_chunks(self):
            release.wait(timeout=0.5)
            if False:
                yield b""

        def close(self):
            self.closed = True

    session = Session()

    class Tts:
        def connect(self, **kwargs):
            return session

    class Client:
        def __init__(self, **kwargs):
            self.audio = types.SimpleNamespace(tts=Tts())

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

    monkeypatch.setattr(module, "Client", Client)
    cancelled = threading.Event()
    cancelled.set()

    try:
        with pytest.raises(TimeoutError, match="receiver thread"):
            module.synthesize_worker(queue.Queue(), cancelled, tmp_path / "result.mp3")
    finally:
        release.set()

    assert session.closed


def test_tts_worker_preserves_primary_error_during_context_cleanup(
        monkeypatch, tmp_path):
    dashscope = types.ModuleType("dashscope")
    dashscope.Client = object
    monkeypatch.setitem(sys.modules, "dashscope", dashscope)
    module = load_module(
        "asyncio_tts_cleanup_error_test",
        REPO_ROOT
        / "samples/speech-synthesizer/synthesize_speech_from_text_using_asyncio/python/run.py",
    )

    class Session:
        def __init__(self):
            self.session = types.SimpleNamespace(request_id="request-id")
            self.first_package_delay = 0

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            raise RuntimeError("context cleanup failed")

        def audio_chunks(self):
            if False:
                yield b""

        def send_text(self, text):
            raise ValueError("send failed")

        def close(self):
            raise RuntimeError("close failed")

    class Tts:
        def connect(self, **kwargs):
            return Session()

    class Client:
        def __init__(self, **kwargs):
            self.audio = types.SimpleNamespace(tts=Tts())

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

    monkeypatch.setattr(module, "Client", Client)
    text_queue = queue.Queue()
    text_queue.put("hello")

    with pytest.raises(ValueError, match="send failed"):
        module.synthesize_worker(
            text_queue,
            threading.Event(),
            tmp_path / "result.mp3",
        )
