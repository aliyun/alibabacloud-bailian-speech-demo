#!/usr/bin/env node
import "dotenv/config";
import { spawn } from "node:child_process";
import http from "node:http";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { WebSocketServer } from "ws";
import {
  RealtimeClient,
  SpeechSynthesizer,
  TranscriptionClient,
  RecognitionClient,
  DashScopeError
} from "dashscope-sdk-nodejs";
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PUBLIC_DIR = path.join(__dirname, "public");
const PORT = Number(process.env.PORT ?? 5173);
const HOST = process.env.HOST ?? "0.0.0.0";
const MIME = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".svg": "image/svg+xml",
  ".json": "application/json; charset=utf-8",
  ".ico": "image/x-icon"
};
function errMsg(e) {
  if (e instanceof DashScopeError) return e.message;
  if (e instanceof Error) return e.message;
  return String(e);
}
function toBuffer(data) {
  if (Buffer.isBuffer(data)) return data;
  if (Array.isArray(data)) return Buffer.concat(data);
  return Buffer.from(data);
}
class RequestError extends Error {
  constructor(message, status = 400) {
    super(message);
    this.status = status;
  }
  status;
}
function parseObject(raw) {
  let value;
  try {
    value = JSON.parse(raw);
  } catch {
    throw new RequestError("\u65E0\u6548 JSON");
  }
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new RequestError("\u8BF7\u6C42\u5FC5\u987B\u662F JSON \u5BF9\u8C61");
  }
  return value;
}
async function readJson(req) {
  const chunks = [];
  for await (const c of req) chunks.push(c);
  return parseObject(Buffer.concat(chunks).toString("utf-8"));
}
function sendJson(res, status, obj) {
  if (res.destroyed || res.writableEnded) return;
  if (res.headersSent) {
    res.destroy();
    return;
  }
  const body = JSON.stringify(obj);
  res.writeHead(status, { "Content-Type": "application/json; charset=utf-8" });
  res.end(body);
}
const REDACTED = "[REDACTED]";
const secretField = (key, value) => {
  const name = key.replace(/[-_]/g, "");
  if (typeof value === "number" && /^(maxresponseoutput|input|output|total|cached|text|audio|max|reasoning|completion|prompt)(input|output|completion)?tokens$/i.test(name)) return false;
  if (value && typeof value === "object" && !Array.isArray(value) && /^(input|output)tokendetails$/i.test(name)) return false;
  return /apikey|authorization|token|password|signature|secret/i.test(name);
};
const headersField = (key, value) => {
  const name = key.replace(/[-_]/g, "");
  if (/headers$|^(?:request|response|http)header$/i.test(name)) return true;
  if (!/^header$/i.test(name)) return false;
  return !value || typeof value !== "object" || !Object.keys(value).some((field) => /^(?:action|type|task_id|task_status|request_id)$/i.test(field));
};
function protocolSanitizer() {
  const secrets = /* @__PURE__ */ new Set();
  const addSecret = (value) => {
    if (typeof value !== "string" || !value.trim()) return;
    for (const key of [value, value.trim(), value.replace(/^Bearer\s+/i, "").trim()]) {
      if (!key) continue;
      secrets.add(key);
      secrets.add(encodeURIComponent(key));
    }
  };
  const remember = (input) => {
    addSecret(input?.apiKey);
    addSecret(process.env.DASHSCOPE_API_KEY);
  };
  const structured = (value) => {
    if (typeof value === "string" && /^[\s]*[\[{]/.test(value)) {
      try {
        return JSON.parse(value);
      } catch {
      }
    }
    return value;
  };
  const text = (value) => {
    let clean = value.replace(/\bdata:audio\/[^;,\s]+(?:;[^;,\s]+)*;base64,([a-z0-9+/_-]*={0,2})/gi, (_uri, data) => `[audio: ${Buffer.byteLength(data, "base64")} bytes]`).replace(/\b(?:https?|wss?):\/\/[^\s<>"'`]+/gi, (raw) => {
      try {
        const url = new URL(raw);
        url.username = "";
        url.password = "";
        for (const key of new Set(url.searchParams.keys())) url.searchParams.set(key, REDACTED);
        if (url.hash) url.hash = REDACTED;
        return url.toString();
      } catch {
        return "[REDACTED URL]";
      }
    });
    for (const key of [...secrets].sort((a, b) => b.length - a.length)) clean = clean.split(key).join(REDACTED);
    clean = clean.replace(/\bauthorization\s*[:=]\s*(?:[a-z][\w-]*\s+)?(?:"[^"]*"|'[^']*'|[^\s,;&]+)/gi, "Authorization=[REDACTED]");
    return clean.replace(/\b(api[-_]?key|authorization|[\w-]*token|password|[\w-]*signature|[\w-]*secret)\s*[:=]\s*(?:Bearer\s+)?(?:"[^"]*"|'[^']*'|[^\s,;&]+)/gi, "$1=[REDACTED]");
  };
  const sanitize = (input) => {
    remember();
    const scanned = /* @__PURE__ */ new WeakSet();
    const collect = (raw) => {
      const value = structured(raw);
      if (!value || typeof value !== "object" || Buffer.isBuffer(value) || scanned.has(value)) return;
      scanned.add(value);
      for (const [key, child] of Object.entries(value)) {
        if (secretField(key, child)) addSecret(child);
        collect(child);
      }
    };
    collect(input);
    const seen = /* @__PURE__ */ new WeakSet();
    const copy = (raw, audio = false, key = "") => {
      if (Buffer.isBuffer(raw)) return { bytes: raw.length };
      if (ArrayBuffer.isView(raw)) return { bytes: raw.byteLength };
      if (raw instanceof ArrayBuffer) return { bytes: raw.byteLength };
      const value = structured(raw);
      if (typeof value === "string") {
        const dataAudio = value.match(/^data:audio\/[^;,]+;base64,([\s\S]*)$/i);
        if (dataAudio) return { bytes: Buffer.byteLength(dataAudio[1], "base64") };
        if (/^(?:(?:input|output)?audio(?:data|base64|chunk)?|base64audio)$/i.test(key.replace(/[-_]/g, "")) || audio && /^(?:delta|data|chunk|base64)$/i.test(key)) {
          return { bytes: Buffer.byteLength(value, "base64") };
        }
        return text(value);
      }
      if (typeof value === "bigint") return value.toString();
      if (!value || typeof value !== "object") return typeof value === "function" || typeof value === "symbol" ? void 0 : value;
      if (seen.has(value)) return "[Circular]";
      seen.add(value);
      if (Array.isArray(value)) {
        const result2 = value.map((child) => copy(child, audio, key));
        seen.delete(value);
        return result2;
      }
      const obj = value;
      if (obj.type === "Buffer" && Array.isArray(obj.data)) return { bytes: obj.data.length };
      const audioMessage = audio || typeof obj.type === "string" && /(?:^|[._-])audio(?:[._-]|$)/i.test(obj.type) && !/transcript|text/i.test(obj.type);
      const result = /* @__PURE__ */ Object.create(null);
      for (const [field, child] of Object.entries(obj)) {
        if (headersField(field, child)) continue;
        result[text(field)] = secretField(field, child) ? REDACTED : copy(child, audioMessage || /audio/i.test(field), field);
      }
      seen.delete(value);
      return result;
    };
    return copy(input);
  };
  remember();
  return { remember, sanitize };
}
function errorFrame(e, trace = false) {
  const metadata = e && typeof e === "object" ? e : {};
  return {
    type: "error",
    message: errMsg(e),
    ...trace && metadata.code !== void 0 ? { code: metadata.code } : {},
    ...trace && metadata.requestId !== void 0 ? { requestId: metadata.requestId } : {}
  };
}
function httpProtocolLog(res) {
  const { remember, sanitize } = protocolSanitizer();
  const write = (value, status = 200, end = false) => {
    if (res.destroyed || res.writableEnded) return;
    const line = JSON.stringify(sanitize(value)) + "\n";
    if (!res.headersSent) res.writeHead(status, { "Content-Type": "application/x-ndjson; charset=utf-8" });
    if (end) res.end(line);
    else res.write(line, "utf8");
  };
  return {
    remember,
    onTrace: (event) => write({ type: "trace", event }),
    result: (value) => write({ type: "result", ...value }, 200, true),
    error: (e, status) => write(errorFrame(e, true), status, true)
  };
}
function baseOpts(b) {
  for (const field of ["apiKey", "workspaceId", "baseUrl"]) {
    if (b[field] !== void 0 && typeof b[field] !== "string") {
      throw new RequestError(`${field} \u5FC5\u987B\u662F\u5B57\u7B26\u4E32`);
    }
  }
  const apiKey = b.apiKey?.trim();
  const workspaceId = b.workspaceId?.trim() ?? "";
  const baseUrl = b.baseUrl?.trim();
  // Browser settings travel with each request and are never stored here. They are used as one set,
  // so the server's own key is never sent to a host or workspace chosen by a browser.
  if (apiKey) return { apiKey, workspaceId, baseUrl: baseUrl || void 0 };
  if (workspaceId || baseUrl) throw new RequestError("\u586B\u5199 Workspace ID \u6216\u670D\u52A1\u57DF\u540D\u65F6\uFF0C\u8BF7\u540C\u65F6\u586B\u5199 API Key");
  const envKey = process.env.DASHSCOPE_API_KEY?.trim();
  if (!envKey) throw new RequestError("\u8BF7\u5728\u8FDE\u63A5\u8BBE\u7F6E\u4E2D\u586B\u5199 API Key\uFF0C\u6216\u5728\u670D\u52A1\u7AEF .env \u4E2D\u914D\u7F6E DASHSCOPE_API_KEY");
  return {
    apiKey: envKey,
    workspaceId: process.env.DASHSCOPE_WORKSPACE_ID?.trim() ?? "",
    baseUrl: process.env.DASHSCOPE_BASE_URL?.trim() || void 0
  };
}
function connectionStatus() {
  return { serverConfigured: Boolean(process.env.DASHSCOPE_API_KEY?.trim()) };
}
function checkSameOriginRequest(req, requireOrigin) {
  const host = req.headers.host;
  const countHeader = (name) => req.rawHeaders.filter((h, i) => i % 2 === 0 && h.toLowerCase() === name).length;
  if (countHeader("host") !== 1 || !host || /[^A-Za-z0-9.!$&'()*+,;=_~%:\[\]-]/.test(host)) {
    throw new RequestError("Forbidden Host", 403);
  }
  try {
    new URL(`http://${host}`);
  } catch {
    throw new RequestError("Forbidden Host", 403);
  }
  const origin = req.headers.origin;
  if (countHeader("origin") > 1 || origin !== void 0 && origin !== `http://${host}` && origin !== `https://${host}` || requireOrigin && !origin) {
    throw new RequestError("\u540C\u6E90 Origin \u5FC5\u987B\u4E0E Host \u7CBE\u786E\u5339\u914D", 403);
  }
  if (!req.url?.startsWith("/") || req.url.startsWith("//")) throw new RequestError("\u65E0\u6548\u8BF7\u6C42\u8DEF\u5F84");
}
const server = http.createServer((req, res) => {
  res.on("error", () => res.destroy());
  let log;
  void (async () => {
    checkSameOriginRequest(req, req.method !== "GET" && req.method !== "HEAD");
    const url = new URL(req.url, "http://localhost");
    if (req.method === "POST") {
      if (url.searchParams.get("trace") === "1" && (url.pathname === "/api/tts" || url.pathname === "/api/asr-file")) {
        log = httpProtocolLog(res);
      }
      if (req.headers["content-type"]?.split(";")[0]?.trim().toLowerCase() !== "application/json") {
        throw new RequestError("POST \u4EC5\u652F\u6301 application/json", 415);
      }
      if (url.pathname === "/api/tts") return await handleTts(req, res, log);
      if (url.pathname === "/api/asr-file") return await handleAsrFile(req, res, log);
      return sendJson(res, 404, { error: "Not Found" });
    }
    if (req.method !== "GET" && req.method !== "HEAD") return sendJson(res, 405, { error: "Method Not Allowed" });
    if (url.pathname === "/api/health") return sendJson(res, 200, { ok: true });
    if (url.pathname === "/api/settings") return sendJson(res, 200, connectionStatus());
    return await serveStatic(url.pathname, res);
  })().catch((e) => {
    try {
      const status = e instanceof RequestError ? e.status : 500;
      if (log) log.error(e, status);
      else sendJson(res, status, { error: errMsg(e) });
    } catch {
      res.destroy();
    }
  });
});
async function serveStatic(pathname, res) {
  const rel = pathname === "/" ? "/asr.html" : pathname === "/develop" || pathname === "/develop/" ? "/index.html" : pathname;
  const filePath = path.join(PUBLIC_DIR, path.normalize(rel));
  if (!filePath.startsWith(PUBLIC_DIR)) {
    res.writeHead(403);
    res.end("Forbidden");
    return;
  }
  try {
    const data = await readFile(filePath);
    res.writeHead(200, { "Content-Type": MIME[path.extname(filePath)] ?? "application/octet-stream" });
    res.end(data);
  } catch {
    res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("Not Found");
  }
}
async function handleTts(req, res, log) {
  const b = await readJson(req);
  log?.remember(b);
  const options = baseOpts(b);
  if (!b.text) {
    if (log) return log.error(new RequestError("\u7F3A\u5C11 text"), 400);
    return sendJson(res, 400, { error: "\u7F3A\u5C11 text" });
  }
  const sampleRate = [8e3, 16e3, 22050, 24e3, 44100, 48e3].find((rate) => rate === Number(b.sampleRate));
  if (b.sampleRate !== void 0 && sampleRate === void 0) throw new RequestError("\u4E0D\u652F\u6301\u7684 TTS \u91C7\u6837\u7387");
  const synth = new SpeechSynthesizer({
    ...options,
    ...log ? { onTrace: log.onTrace } : {},
    model: b.model || void 0,
    voice: b.voice || "longanhuan_v3.1",
    format: b.format || "mp3",
    sampleRate,
    volume: b.volume !== void 0 ? Number(b.volume) : void 0,
    rate: b.rate !== void 0 ? Number(b.rate) : void 0,
    pitch: b.pitch !== void 0 ? Number(b.pitch) : void 0
  });
  try {
    const audio = await synth.synthesize(String(b.text));
    const fmt = b.format || "mp3";
    if (log) return log.result({ bytes: audio.length, format: fmt, sampleRate: sampleRate ?? null });
    const ct = fmt === "pcm" ? "application/octet-stream" : fmt === "wav" ? "audio/wav" : `audio/${fmt}`;
    res.writeHead(200, { "Content-Type": ct, "Content-Length": String(audio.length) });
    res.end(audio);
  } catch (e) {
    if (log) log.error(e, 502);
    else sendJson(res, 502, { error: errMsg(e) });
  }
}
async function handleAsrFile(req, res, log) {
  const b = await readJson(req);
  log?.remember(b);
  const options = baseOpts(b);
  if (!b.fileUrl) {
    if (log) return log.error(new RequestError("\u7F3A\u5C11 fileUrl"), 400);
    return sendJson(res, 400, { error: "\u7F3A\u5C11 fileUrl" });
  }
  const client = new TranscriptionClient({
    ...options,
    ...log ? { onTrace: log.onTrace } : {},
    model: b.model || void 0,
    pollIntervalMs: 2e3
  });
  try {
    const params = {};
    if (Array.isArray(b.languageHints) && b.languageHints.length) params.language_hints = b.languageHints;
    if (b.diarizationEnabled) params.diarization_enabled = true;
    const job = await client.transcribe(String(b.fileUrl), params);
    const result = {
      taskId: job.taskId,
      taskStatus: job.taskStatus,
      usage: job.usage,
      results: job.results.map((r) => ({
        fileUrl: r.fileUrl,
        subtaskStatus: r.subtaskStatus,
        text: r.text,
        code: r.code,
        message: r.message
      }))
    };
    if (log) log.result(result);
    else sendJson(res, 200, result);
  } catch (e) {
    if (log) log.error(e, 502);
    else sendJson(res, 502, { error: errMsg(e) });
  }
}
const wss = new WebSocketServer({ noServer: true });
server.on("upgrade", (req, socket, head) => {
  socket.on("error", () => socket.destroy());
  try {
    checkSameOriginRequest(req, true);
    const { pathname, searchParams } = new URL(req.url, "http://localhost");
    if (pathname !== "/ws/realtime" && pathname !== "/ws/asr" && pathname !== "/ws/tts") {
      socket.destroy();
      return;
    }
    const trace = searchParams.get("trace") === "1";
    wss.handleUpgrade(req, socket, head, (ws) => {
      if (pathname === "/ws/realtime") handleRealtime(ws, trace);
      else if (pathname === "/ws/tts") handleTtsStreaming(ws, trace);
      else handleAsrRealtime(ws, trace);
    });
  } catch {
    socket.end("HTTP/1.1 403 Forbidden\r\nConnection: close\r\nContent-Length: 0\r\n\r\n");
  }
});
function safeSend(ws, obj, binary = false, reportError = true) {
  const failed = () => {
    if (reportError) safeSend(ws, { type: "error", message: "WebSocket \u53D1\u9001\u5931\u8D25" }, false, false);
  };
  try {
    if (ws.readyState === ws.OPEN) {
      ws.send(binary ? obj : JSON.stringify(obj), (error) => {
        if (error) failed();
      });
    }
  } catch {
    failed();
  }
}
function bridgeSession(ws, trace = false) {
  let client;
  let revision = 0;
  const sanitizer = trace ? protocolSanitizer() : void 0;
  const send = (obj) => safeSend(ws, sanitizer ? sanitizer.sanitize(obj) : obj);
  const failure = (e) => errorFrame(e, trace);
  const clear = () => {
    revision++;
    const old = client;
    client = void 0;
    try {
      old?.close();
    } catch (e) {
      send(failure(e));
    }
  };
  ws.on("close", clear);
  ws.on("error", () => {
    send({ type: "error", message: "WebSocket \u8FDE\u63A5\u9519\u8BEF" });
    clear();
  });
  return {
    send,
    clear,
    failure,
    traceOptions(current) {
      return trace ? { onTrace: (event) => {
        if (current()) send({ type: "trace", event });
      } } : {};
    },
    get client() {
      return client;
    },
    replace(next) {
      clear();
      client = next;
      const version = revision;
      return () => client === next && version === revision && ws.readyState === ws.OPEN;
    },
    listen(types, handle) {
      ws.on("message", (data, isBinary) => {
        const pending = (async () => {
          if (isBinary) return await handle({}, toBuffer(data));
          const msg = parseObject(data.toString());
          sanitizer?.remember(msg);
          if (typeof msg.type !== "string" || !types.includes(msg.type)) throw new RequestError("\u65E0\u6548\u6D88\u606F\u7C7B\u578B");
          await handle(msg);
        })();
        const version = revision;
        void pending.catch((e) => {
          if (version === revision) send(failure(e));
        });
      });
    }
  };
}
function handleTtsStreaming(ws, trace = false) {
  const session = bridgeSession(ws, trace);
  session.listen(["config", "stop"], async (msg, binary) => {
    if (binary) throw new RequestError("TTS \u4EC5\u63A5\u53D7 JSON \u6587\u672C\u6D88\u606F");
    if (msg.type === "stop") {
      session.clear();
      session.send({ type: "status", status: "closed" });
      return;
    }
    const options = baseOpts(msg);
    if (typeof msg.text !== "string" || !msg.text.trim()) throw new RequestError("text \u5FC5\u987B\u662F\u975E\u7A7A\u5B57\u7B26\u4E32");
    if (msg.text.length > 2e4) throw new RequestError("text \u4E0D\u80FD\u8D85\u8FC7 20000 \u5B57\u7B26");
    for (const field of ["model", "voice"]) {
      if (msg[field] !== void 0 && (typeof msg[field] !== "string" || !msg[field].trim())) {
        throw new RequestError(`${field} \u5FC5\u987B\u662F\u975E\u7A7A\u5B57\u7B26\u4E32`);
      }
    }
    const range = (field, fallback, min, max) => {
      const value = msg[field] === void 0 ? fallback : msg[field];
      if (typeof value !== "number" || !Number.isFinite(value) || value < min || value > max) {
        throw new RequestError(`${field} \u5FC5\u987B\u662F ${min} \u5230 ${max} \u4E4B\u95F4\u7684\u6709\u9650\u6570\u503C`);
      }
      return value;
    };
    const rate = range("rate", 1, 0.5, 2);
    const volume = range("volume", 50, 0, 100);
    const pitch = msg.pitch === void 0 ? void 0 : range("pitch", 1, 0.5, 2);
    const format = ["pcm", "mp3", "wav"].find((value) => value === (msg.format === void 0 ? "pcm" : msg.format));
    if (!format) throw new RequestError("format \u5FC5\u987B\u662F pcm\u3001mp3 \u6216 wav");
    const sampleRate = [8e3, 16e3, 22050, 24e3, 44100, 48e3].find((value) => value === (msg.sampleRate === void 0 ? 24e3 : msg.sampleRate));
    if (!sampleRate) throw new RequestError("\u4E0D\u652F\u6301\u7684 TTS \u91C7\u6837\u7387");
    let current = () => false;
    const next = new SpeechSynthesizer({
      ...options,
      ...session.traceOptions(() => current()),
      model: msg.model?.trim(),
      voice: msg.voice?.trim() ?? "longanhuan_v3.1",
      rate,
      pitch,
      format,
      sampleRate,
      volume
    });
    current = session.replace(next);
    const fail = (e) => {
      if (!current()) return;
      session.send(session.failure(e));
      session.clear();
    };
    next.on("started", () => {
      if (current()) session.send({ type: "status", status: "started", sampleRate });
    });
    next.on("audio", (pcm) => {
      if (current()) safeSend(ws, pcm, true);
    });
    next.on("finished", () => {
      if (!current()) return;
      session.send({ type: "status", status: "finished" });
      session.clear();
    });
    next.on("failed", fail);
    next.on("error", fail);
    next.on("close", () => {
      if (!current()) return;
      session.clear();
      session.send({ type: "status", status: "closed" });
    });
    try {
      await next.synthesize(msg.text);
    } catch (e) {
      fail(e);
    }
  });
}
function handleRealtime(ws, trace = false) {
  const session = bridgeSession(ws, trace);
  const { send } = session;
  session.listen(["config", "commit", "respond", "text", "stop"], async (msg, binary) => {
    if (binary) {
      if (!session.client?.isConnected) throw new RequestError("\u5C1A\u672A\u8FDE\u63A5");
      session.client.appendAudio(binary);
      return;
    }
    if (msg.type === "config") {
      let current = () => false;
      const next = new RealtimeClient({
        ...baseOpts(msg),
        ...session.traceOptions(() => current()),
        model: msg.model || "qwen-audio-3.1-realtime-plus",
        voice: msg.voice || void 0,
        instructions: msg.instructions || void 0,
        modalities: msg.modalities ?? ["text", "audio"],
        turnDetection: parseTurnDetection(msg.turnDetection),
        inputTranscription: parseInputTranscription(msg.inputTranscription)
      });
      current = session.replace(next);
      wireRealtimeEvents(next, ws, current, send, trace);
      next.on("close", (info) => {
        if (!current()) return;
        session.clear();
        send({ type: "status", status: "closed", code: info.code, reason: info.reason });
      });
      try {
        await next.connect();
        if (current()) send({ type: "status", status: "open" });
      } catch (e) {
        if (!current()) return;
        send(session.failure(e));
        session.clear();
        send({ type: "status", status: "closed" });
      }
      return;
    }
    if (msg.type === "stop") {
      session.clear();
      send({ type: "status", status: "closed" });
      return;
    }
    const client = session.client;
    if (!client?.isConnected) throw new RequestError("\u5C1A\u672A\u8FDE\u63A5");
    switch (msg.type) {
      case "commit":
        client.commit();
        break;
      case "respond":
        client.createResponse();
        break;
      case "text": {
        if (typeof msg.text !== "string") throw new RequestError("text \u5FC5\u987B\u662F\u5B57\u7B26\u4E32");
        const item = {
          type: "message",
          role: "user",
          content: [{ type: "input_text", text: msg.text }]
        };
        client.createConversationItem(item);
        client.createResponse();
        break;
      }
    }
  });
}
function parseTurnDetection(v) {
  if (v === null) return null;
  if (v && typeof v === "object" && !Array.isArray(v)) return v;
  return void 0;
}
function parseInputTranscription(value) {
  if (value === void 0 || value === null) return value;
  if (typeof value !== "object" || Array.isArray(value)) {
    throw new RequestError("inputTranscription \u5FC5\u987B\u662F\u5BF9\u8C61\u6216 null");
  }
  for (const key of ["model", "language"]) {
    const option = value[key];
    if (option !== void 0 && (typeof option !== "string" || !option.trim())) {
      throw new RequestError(`inputTranscription.${key} \u5FC5\u987B\u662F\u975E\u7A7A\u5B57\u7B26\u4E32`);
    }
  }
  return value;
}
function wireRealtimeEvents(client, ws, current, sendMessage, trace) {
  const send = (o) => {
    if (current()) sendMessage(o);
  };
  client.on("sessionCreated", () => send({ type: "log", text: "session.created" }));
  client.on("sessionUpdated", () => send({ type: "log", text: "session.updated\uFF08\u9274\u6743+\u914D\u7F6E\u6210\u529F\uFF09" }));
  client.on("audio", (pcm) => {
    if (current()) safeSend(ws, pcm, true);
  });
  client.on("audioTranscriptDelta", ({ delta }) => send({ type: "aiDelta", delta }));
  client.on("outputTranscript", ({ transcript }) => send({ type: "aiText", transcript }));
  client.on("inputTranscriptDelta", ({ text, stash }) => send({ type: "userDelta", text, stash }));
  client.on("inputTranscript", ({ transcript }) => send({ type: "userText", transcript }));
  client.on("speechStarted", () => send({ type: "speechStarted" }));
  client.on("speechStopped", () => send({ type: "speechStopped" }));
  client.on("responseCreated", () => send({ type: "responseCreated" }));
  client.on("responseDone", () => send({ type: "responseDone" }));
  client.on("event", (e) => {
    if (e.type === "response.text.delta" && typeof e.delta === "string") send({ type: "aiDelta", delta: e.delta });
    else if (e.type === "response.text.done" && typeof e.text === "string") send({ type: "aiText", transcript: e.text });
  });
  client.on("error", (e) => send(trace ? errorFrame(e, true) : { type: "error", message: e.message }));
}
function handleAsrRealtime(ws, trace = false) {
  const session = bridgeSession(ws, trace);
  let finishing = false;
  session.listen(["config", "finish", "stop"], async (msg, binary) => {
    if (binary) {
      if (!session.client?.isRunning || finishing) throw new RequestError("\u6CA1\u6709\u53EF\u63A5\u6536\u97F3\u9891\u7684\u4EFB\u52A1");
      session.client.sendAudio(binary);
      return;
    }
    if (msg.type === "config") {
      if (msg.vadModel !== void 0 && msg.vadModel !== "near_meeting_16k" && msg.vadModel !== "far_field_meeting_16k") {
        throw new RequestError("vadModel \u5FC5\u987B\u4E3A near_meeting_16k \u6216 far_field_meeting_16k");
      }
      const bool = (field) => {
        if (msg[field] === void 0) return void 0;
        if (typeof msg[field] !== "boolean") throw new RequestError(`${field} \u5FC5\u987B\u662F\u5E03\u5C14\u503C`);
        return msg[field];
      };
      const integer = (field, min, max) => {
        if (msg[field] === void 0) return void 0;
        const value = msg[field];
        if (!Number.isInteger(value) || value < min || value > max) {
          throw new RequestError(`${field} \u5FC5\u987B\u662F ${min} \u5230 ${max} \u4E4B\u95F4\u7684\u6574\u6570`);
        }
        return value;
      };
      const decimal = (field, min, max) => {
        if (msg[field] === void 0) return void 0;
        const value = msg[field];
        if (typeof value !== "number" || !Number.isFinite(value) || value < min || value > max) {
          throw new RequestError(`${field} \u5FC5\u987B\u662F ${min} \u5230 ${max} \u4E4B\u95F4\u7684\u6570\u503C`);
        }
        return value;
      };
      const vocabularyId = msg.vocabularyId === void 0 ? void 0 : (() => {
        if (typeof msg.vocabularyId !== "string" || !msg.vocabularyId.trim()) {
          throw new RequestError("vocabularyId \u5FC5\u987B\u662F\u975E\u7A7A\u5B57\u7B26\u4E32");
        }
        return msg.vocabularyId.trim();
      })();
      const vocabulary = msg.vocabulary === void 0 ? void 0 : (() => {
        const invalid = new RequestError("vocabulary \u5FC5\u987B\u662F 1 \u5230 50 \u4E2A\u70ED\u8BCD\uFF0C\u6743\u91CD\u53D6 1 \u5230 5 \u4E4B\u95F4\u7684\u6570\u503C\u6216 50");
        const value = msg.vocabulary;
        if (typeof value !== "object" || value === null || Array.isArray(value)) throw invalid;
        const entries = Object.entries(value);
        if (!entries.length || entries.length > 50) throw invalid;
        for (const [word, weight] of entries) {
          if (!word.trim()) throw invalid;
          if (typeof weight !== "number" || !Number.isFinite(weight)) throw invalid;
          if (weight !== 50 && (weight < 1 || weight > 5)) throw invalid;
        }
        return value;
      })();
      const parameters = {};
      if (msg.vadModel !== void 0) parameters.vad_model = msg.vadModel;
      const speechNoiseThreshold = decimal("speechNoiseThreshold", -1, 1);
      if (speechNoiseThreshold !== void 0) parameters.speech_noise_threshold = speechNoiseThreshold;
      const keepDialect = bool("keepDialect");
      if (keepDialect !== void 0) parameters.keep_dialect = keepDialect;
      if (vocabulary !== void 0) parameters.vocabulary = vocabulary;
      const maxSentenceSilence = integer("maxSentenceSilence", 200, 6e3);
      const multiThresholdModeEnabled = bool("multiThresholdModeEnabled");
      const heartbeat = bool("heartbeat");
      let current = () => false;
      const next = new RecognitionClient({
        ...baseOpts(msg),
        ...session.traceOptions(() => current()),
        model: msg.model || void 0,
        format: "pcm",
        sampleRate: msg.sampleRate ? Number(msg.sampleRate) : 16e3,
        parameters: Object.keys(parameters).length ? parameters : void 0,
        languageHints: Array.isArray(msg.languageHints) && msg.languageHints.length ? msg.languageHints : void 0,
        maxSentenceSilence,
        multiThresholdModeEnabled,
        heartbeat,
        vocabularyId,
        disfluencyRemovalEnabled: msg.disfluencyRemovalEnabled || void 0,
        punctuationPredictionEnabled: msg.punctuationPredictionEnabled,
        inverseTextNormalizationEnabled: msg.inverseTextNormalizationEnabled
      });
      current = session.replace(next);
      const send = (obj) => {
        if (current()) session.send(obj);
      };
      finishing = false;
      let finished = false;
      next.on("started", ({ taskId }) => send({ type: "status", status: "started", taskId }));
      next.on("result", (s) => send({ type: "result", text: s.text, end: !!s.sentence_end }));
      next.on("sentenceEnd", (s) => send({ type: "sentenceEnd", text: s.text }));
      next.on("finished", () => {
        if (!current() || finished) return;
        finished = true;
        send({ type: "status", status: "finished" });
      });
      next.on("error", (e) => send(trace ? session.failure(e) : { type: "error", message: e.message }));
      next.on("close", () => {
        if (!current()) return;
        session.clear();
        if (!finished) session.send({ type: "status", status: "closed" });
      });
      try {
        await next.start();
      } catch (e) {
        if (!current()) return;
        send(session.failure(e));
        session.clear();
        session.send({ type: "status", status: "closed" });
      }
      return;
    }
    if (msg.type === "stop") {
      session.clear();
      session.send({ type: "status", status: "closed" });
      return;
    }
    if (!session.client?.isRunning || finishing) throw new RequestError("\u6CA1\u6709\u53EF\u7ED3\u675F\u7684\u4EFB\u52A1");
    finishing = true;
    await session.client.finish();
  });
}
function openBrowser(url) {
  if (PORT === 0 || process.env.NO_OPEN === "1") return;
  const command = process.platform === "darwin" ? { file: "open", args: [url] } : process.platform === "win32" ? { file: "cmd", args: ["/c", "start", "", url] } : { file: "xdg-open", args: [url] };
  try {
    const child = spawn(command.file, command.args, { detached: true, stdio: "ignore" });
    child.on("error", () => {
    });
    child.unref();
  } catch {
  }
}
server.listen(PORT, HOST, () => {
  const address = server.address();
  const port = typeof address === "object" && address ? address.port : PORT;
  const browserHost = HOST === "0.0.0.0" || HOST === "::" ? "localhost" : HOST.includes(":") ? `[${HOST}]` : HOST;
  const home = `http://${browserHost}:${port}/`;
  console.log(`
  Qwen Audio SDK \u4F53\u9A8C\u9875\u5DF2\u542F\u52A8`);
  console.log(`    \u76D1\u542C\u5730\u5740\uFF1A ${HOST}:${port}`);
  console.log(`    \u9ED8\u8BA4\u4F53\u9A8C\uFF1A ${home}`);
  console.log(`    \u5F00\u53D1\u8005\u53F0\uFF1A ${home}develop`);
  console.log(`    \u7F51\u9875\u586B\u5199\u7684\u8FDE\u63A5\u914D\u7F6E\u53EA\u4FDD\u5B58\u5728\u5404\u81EA\u6D4F\u89C8\u5668\u4E2D\uFF0C\u670D\u52A1\u7AEF\u4E0D\u4FDD\u5B58\uFF1B\u670D\u52A1\u7AEF\u51ED\u636E\u8BF7\u5199\u5165 .env\u3002\u516C\u7F51\u90E8\u7F72\u9700 HTTPS \u4E0E\u8BBF\u95EE\u8BA4\u8BC1\u3002
`);
  openBrowser(home);
});
