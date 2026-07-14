#!/usr/bin/env python3
"""Lightweight HTTP + WebSocket proxy for the web demo.

Serves static files from this directory and proxies WebSocket
connections to DashScope Realtime API.

Usage:
    export DASHSCOPE_API_KEY=your-key
    python -m demo_app.web.server          # http://localhost:8080
    python -m demo_app.web.server --port 9000
"""

import argparse
import asyncio
import http.server
import json
import os
import threading

import websockets

from demo_app.config import DEFAULT_BASE_URL, DEFAULT_MODEL
from demo_app.prompts import (
    BASE_CONSTRAINTS,
    COMPANION_INSTRUCTIONS,
    REASONING_INSTRUCTIONS,
    TOOL_INSTRUCTIONS,
)

DASHSCOPE_UPSTREAM = DEFAULT_BASE_URL
DEFAULT_PORT = 8080
WEB_DIR = os.path.dirname(os.path.abspath(__file__))


class WebDemoRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/prompts":
            self._serve_prompts()
        elif self.path == "/api/config":
            self._serve_config()
        else:
            super().do_GET()

    def _serve_prompts(self):
        prompts = {
            "base_constraints": BASE_CONSTRAINTS,
            "companion": COMPANION_INSTRUCTIONS,
            "tool": TOOL_INSTRUCTIONS,
            "reasoning": REASONING_INSTRUCTIONS,
        }
        self._send_json(prompts)

    def _serve_config(self):
        self._send_json({"model": DEFAULT_MODEL})

    def _send_json(self, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


async def ws_proxy(browser_ws):
    api_key = os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("REALTIME_API_KEY", "")
    if not api_key:
        await browser_ws.send(json.dumps({
            "type": "error",
            "error": {"message": "Server env DASHSCOPE_API_KEY not set"},
        }))
        return

    raw_path = browser_ws.request.path
    query = raw_path.split("?", 1)[-1] if "?" in raw_path else ""
    params = dict(p.split("=", 1) for p in query.split("&") if "=" in p)
    model = params.get("model", "")

    upstream_url = f"{DEFAULT_BASE_URL}?model={model}"
    headers = {"Authorization": f"Bearer {api_key}"}

    print(f"[ws] new connection, model={model}")

    try:
        async with websockets.connect(upstream_url, additional_headers=headers) as upstream_ws:
            async def browser_to_upstream():
                try:
                    async for msg in browser_ws:
                        await upstream_ws.send(msg)
                finally:
                    await upstream_ws.close()

            async def upstream_to_browser():
                async for msg in upstream_ws:
                    await browser_ws.send(msg)

            await asyncio.gather(browser_to_upstream(), upstream_to_browser())
    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        print(f"[ws] error: {e}")


def start_http_server(port):
    os.chdir(WEB_DIR)
    httpd = http.server.HTTPServer(("0.0.0.0", port), WebDemoRequestHandler)
    print(f"[http] serving at http://localhost:{port}/")
    httpd.serve_forever()


async def main(http_port, ws_port):
    threading.Thread(target=start_http_server, args=(http_port,), daemon=True).start()
    async with websockets.serve(ws_proxy, "0.0.0.0", ws_port):
        print(f"[ws]   proxy listening on ws://localhost:{ws_port}/ws?model=xxx")
        await asyncio.Future()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web demo proxy server")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="HTTP port")
    parser.add_argument("--ws-port", type=int, default=DEFAULT_PORT + 1, help="WebSocket port")
    args = parser.parse_args()

    if not (os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("REALTIME_API_KEY")):
        raise SystemExit("Error: set DASHSCOPE_API_KEY or REALTIME_API_KEY")

    asyncio.run(main(args.port, args.ws_port))
