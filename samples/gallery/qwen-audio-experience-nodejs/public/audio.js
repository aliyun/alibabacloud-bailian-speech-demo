/**
 * 浏览器端音频工具：麦克风采集（-> 16kHz/16bit/mono PCM）与 PCM 播放器（24kHz）。
 * 纯 vanilla JS，无外部依赖（离线可用）。
 */

/** 线性插值重采样。 */
function resample(input, inRate, outRate) {
  if (inRate === outRate) return input
  const ratio = inRate / outRate
  const outLen = Math.round(input.length / ratio)
  const out = new Float32Array(outLen)
  for (let i = 0; i < outLen; i++) {
    const idx = i * ratio
    const i0 = Math.floor(idx)
    const i1 = Math.min(i0 + 1, input.length - 1)
    const frac = idx - i0
    out[i] = input[i0] * (1 - frac) + input[i1] * frac
  }
  return out
}

/** Float32 [-1,1] -> Int16 PCM。 */
function floatTo16BitPCM(f32) {
  const i16 = new Int16Array(f32.length)
  for (let i = 0; i < f32.length; i++) {
    let s = Math.max(-1, Math.min(1, f32[i]))
    i16[i] = s < 0 ? s * 0x8000 : s * 0x7fff
  }
  return i16
}

/**
 * 麦克风采集器：持续输出目标采样率的 Int16 PCM（ArrayBuffer）。
 * 用法：const rec = new MicRecorder((buf) => ws.send(buf)); await rec.start(16000); ... rec.stop()
 */
class MicRecorder {
  constructor(onChunk) {
    this.onChunk = onChunk
    this.stream = null
    this.ctx = null
    this.processor = null
    this.source = null
    this.running = false
  }

  async start(targetSampleRate = 16000) {
    if (this.running) return
    this.stream = await navigator.mediaDevices.getUserMedia({
      audio: { channelCount: 1, echoCancellation: true, noiseSuppression: true, autoGainControl: true },
    })
    this.ctx = new (window.AudioContext || window.webkitAudioContext)()
    await this.ctx.resume()
    this.inputRate = this.ctx.sampleRate
    this.targetRate = targetSampleRate

    this.source = this.ctx.createMediaStreamSource(this.stream)
    // ScriptProcessor 兼容性最好；4096 帧约 85ms@48k
    this.processor = this.ctx.createScriptProcessor(4096, 1, 1)
    this.processor.onaudioprocess = (e) => {
      if (!this.running) return
      const input = e.inputBuffer.getChannelData(0)
      const resampled = resample(input, this.inputRate, this.targetRate)
      const pcm16 = floatTo16BitPCM(resampled)
      this.onChunk(pcm16.buffer)
    }

    this.source.connect(this.processor)
    // 接到静音增益再到 destination，确保回调触发且不回放麦克风（避免啸叫）
    const mute = this.ctx.createGain()
    mute.gain.value = 0
    this.processor.connect(mute)
    mute.connect(this.ctx.destination)

    this.running = true
  }

  stop() {
    this.running = false
    try { this.processor && (this.processor.onaudioprocess = null) } catch (e) {}
    try { this.source && this.source.disconnect() } catch (e) {}
    try { this.processor && this.processor.disconnect() } catch (e) {}
    try { this.stream && this.stream.getTracks().forEach((t) => t.stop()) } catch (e) {}
    try { this.ctx && this.ctx.close() } catch (e) {}
    this.stream = this.ctx = this.processor = this.source = null
  }
}

/**
 * PCM 播放器：按序调度播放 Int16 PCM（默认 24kHz/mono）。支持 barge-in 清空。
 * AudioBuffer 以 24000 采样率创建，浏览器会自动重采样到输出设备，无需强制 AudioContext 采样率。
 */
class PcmPlayer {
  constructor(sampleRate = 24000) {
    this.sampleRate = sampleRate
    this.ctx = null
    this.nextTime = 0
    this.sources = new Set()
  }

  _ensureCtx() {
    if (!this.ctx) {
      this.ctx = new (window.AudioContext || window.webkitAudioContext)()
      this.nextTime = 0
    }
    if (this.ctx.state === 'suspended') this.ctx.resume()
    return this.ctx
  }

  /** 喂入一段 Int16 PCM（ArrayBuffer / Int16Array）。 */
  feed(data) {
    const ctx = this._ensureCtx()
    const i16 = data instanceof Int16Array ? data : new Int16Array(data)
    if (i16.length === 0) return
    const f32 = new Float32Array(i16.length)
    for (let i = 0; i < i16.length; i++) f32[i] = i16[i] / 0x8000

    const buf = ctx.createBuffer(1, f32.length, this.sampleRate)
    buf.copyToChannel(f32, 0)

    const src = ctx.createBufferSource()
    src.buffer = buf
    src.connect(ctx.destination)

    const now = ctx.currentTime
    if (this.nextTime < now) this.nextTime = now + 0.02
    src.start(this.nextTime)
    this.nextTime += buf.duration

    this.sources.add(src)
    src.onended = () => this.sources.delete(src)
  }

  /** 打断：停止所有已排队音频（VAD 检测到用户说话时调用）。 */
  clear() {
    for (const s of this.sources) {
      try { s.stop() } catch (e) {}
    }
    this.sources.clear()
    this.nextTime = 0
  }

  destroy() {
    this.clear()
    try { this.ctx && this.ctx.close() } catch (e) {}
    this.ctx = null
  }
}
