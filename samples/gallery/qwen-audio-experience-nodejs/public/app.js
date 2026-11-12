/**
 * 体验台前端逻辑：设置持久化 + Tab 切换 + 实时对话 / TTS / 实时识别接线。
 * 纯 vanilla JS，无外部依赖。
 */

const $ = (id) => document.getElementById(id)
const wsBase = () => `${location.protocol === 'https:' ? 'wss' : 'ws'}://${location.host}`

/** 需要持久化到 localStorage 的输入项。 */
const PERSIST = [
  'rt-model', 'rt-voice', 'rt-turn', 'rt-modalities', 'rt-instructions',
  'tts-model', 'tts-voice', 'tts-format', 'tts-samplerate', 'tts-volume', 'tts-rate', 'tts-pitch', 'tts-text',
  'rasr-model', 'rasr-samplerate', 'rasr-langs', 'rasr-vad', 'rasr-silence', 'rasr-noise',
  'rasr-multi-threshold', 'rasr-heartbeat', 'rasr-keep-dialect', 'rasr-vocabulary-id', 'rasr-vocabulary',
]
/** 清空后应回到页面默认值而非保存空值的输入项。 */
const RESTORE_DEFAULT_WHEN_EMPTY = new Set(['rt-model', 'tts-model', 'rasr-model', 'rasr-silence'])

// ---------- 设置持久化 ----------
function loadSettings() {
  for (const id of PERSIST) {
    const el = $(id)
    if (!el) continue
    const v = localStorage.getItem('ds_' + id)
    if (v === '' && RESTORE_DEFAULT_WHEN_EMPTY.has(id)) continue
    if (v !== null) {
      if (el.tagName === 'SELECT') {
        // 仅当存储值仍是合法选项时恢复，否则保留默认选中项
        if (Array.from(el.options).some((o) => o.value === v)) el.value = v
      } else {
        el.value = v
      }
    }
  }
  syncRangeLabels()
}
function bindPersist() {
  for (const id of PERSIST) {
    const el = $(id)
    if (!el) continue
    el.addEventListener('input', () => {
      localStorage.setItem('ds_' + id, el.value)
      syncRangeLabels()
    })
    el.addEventListener('change', () => localStorage.setItem('ds_' + id, el.value))
  }
}
function syncRangeLabels() {
  $('tts-volume-val').textContent = $('tts-volume').value
  $('tts-rate-val').textContent = Number($('tts-rate').value).toFixed(1)
  $('tts-pitch-val').textContent = Number($('tts-pitch').value).toFixed(1)
}

// Connection settings live only in this browser (shared with the studio pages); the local server never stores them.
const CONNECTION_KEY = 'qwenAudio.connection'
const CONNECTION_FIELDS = ['apiKey', 'workspaceId', 'baseUrl']
let serverConfigured = false

function storedConnection() {
  let saved = {}
  try { saved = JSON.parse(localStorage.getItem(CONNECTION_KEY) || '{}') || {} } catch (e) {}
  return Object.fromEntries(CONNECTION_FIELDS.map((key) => [key, typeof saved[key] === 'string' ? saved[key] : '']))
}

/** 读取当前浏览器保存的连接设置；API Key 为空时由本地服务使用 .env 配置。 */
function getSettings() {
  const saved = storedConnection()
  return {
    apiKey: saved.apiKey,
    workspaceId: saved.workspaceId || undefined,
    baseUrl: saved.baseUrl || undefined,
  }
}

function showSharedSettings() {
  const saved = storedConnection()
  for (const key of CONNECTION_FIELDS) $(key).value = saved[key]
  $('apiKey').placeholder = serverConfigured ? '留空则使用服务端 .env 配置' : '请输入 DashScope API Key'
  const ready = Boolean(saved.apiKey || serverConfigured)
  $('shared-api-status').textContent = saved.apiKey ? '已保存在本浏览器' : serverConfigured ? '使用服务端 .env 配置' : 'API Key 未配置'
  $('shared-api-status').dataset.state = ready ? 'ready' : 'missing'
  updateCodeExample()
  return ready
}

function openSharedSettings() {
  showSharedSettings()
  const dialog = $('settings')
  if (!dialog.open) dialog.showModal()
}

function closeSharedSettings() {
  const dialog = $('settings')
  if (dialog.open) dialog.close()
}

async function loadSharedSettings() {
  try {
    const response = await fetch('/api/settings', { cache: 'no-store' })
    const status = await response.json()
    if (!response.ok) throw new Error(status.error || `HTTP ${response.status}`)
    serverConfigured = status.serverConfigured === true
  } catch (error) {
    serverConfigured = false
  }
  if (!showSharedSettings() && !$('settings').open) $('settings').showModal()
}

function saveSharedSettings() {
  const next = Object.fromEntries(CONNECTION_FIELDS.map((key) => [key, $(key).value.trim()]))
  try {
    if (!next.apiKey && (next.workspaceId || next.baseUrl)) throw new Error('填写 Workspace ID 或服务域名时，请同时填写 API Key')
    if (!next.apiKey && !serverConfigured) throw new Error('请填写 API Key，或在服务端 .env 中配置 DASHSCOPE_API_KEY')
    if (next.apiKey) localStorage.setItem(CONNECTION_KEY, JSON.stringify(next))
    else localStorage.removeItem(CONNECTION_KEY)
  } catch (error) {
    alert(error.message || error)
    $('apiKey').focus()
    return
  }
  showSharedSettings()
  closeSharedSettings()
}

// ---------- Tab 切换 ----------
let activeCodeTab = 'realtime'

function bindTabs() {
  document.querySelectorAll('.tab').forEach((tab) => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach((t) => t.classList.remove('active'))
      document.querySelectorAll('.panel').forEach((p) => p.classList.remove('active'))
      tab.classList.add('active')
      activeCodeTab = tab.dataset.tab
      $('panel-' + activeCodeTab).classList.add('active')
      updateCodeExample()
    })
  })
  $('toggle-settings').addEventListener('click', openSharedSettings)
  $('close-settings').addEventListener('click', closeSharedSettings)
  // Discard unsaved edits so the inputs always match what requests will use.
  $('settings').addEventListener('close', () => { showSharedSettings() })
}

// ---------- Node.js 调用代码 ----------
const CODE_TITLES = {
  realtime: '实时对话调用代码',
  tts: '语音合成调用代码',
  'asr-rt': '实时识别调用代码',
}

function codeConnectionLines() {
  const baseUrl = $('baseUrl').value.trim()
  return `  apiKey: process.env.DASHSCOPE_API_KEY,
  workspaceId: process.env.DASHSCOPE_WORKSPACE_ID,${baseUrl ? `\n  baseUrl: ${JSON.stringify(baseUrl)},` : ''}`
}

function realtimeCode() {
  const turn = $('rt-turn').value
  const turnDetection = turn === 'push' ? 'null' : `{ type: ${JSON.stringify(turn)} }`
  const modalities = JSON.stringify($('rt-modalities').value.split(','))
  return `import { readFile, writeFile } from 'node:fs/promises'
import { setTimeout as sleep } from 'node:timers/promises'
import { RealtimeClient } from 'dashscope-sdk-nodejs'

// 输入须为无文件头的 16kHz / 16bit / 单声道 PCM，不是 WAV 或 MP3。
if (!process.argv[2]) throw new Error('用法：node realtime.mjs input.pcm [output.pcm]')
const pcmBuffer = await readFile(process.argv[2])
if (!pcmBuffer.length || pcmBuffer.length % 2) throw new Error('PCM 必须非空且包含完整的 16bit 采样')

const client = new RealtimeClient({
${codeConnectionLines()}
  model: ${JSON.stringify($('rt-model').value.trim())},${$('rt-voice').value.trim() ? `\n  voice: ${JSON.stringify($('rt-voice').value.trim())},` : ''}
  // 文件按一轮手动提交；实时麦克风可使用页面所选配置：${turnDetection}。
  turnDetection: null,
  modalities: ${modalities},
  instructions: ${JSON.stringify($('rt-instructions').value.trim())},
})

const audioChunks = []
client.on('audio', (audio) => audioChunks.push(audio))
client.on('outputTranscript', ({ transcript }) => console.log(transcript))
const ready = new Promise((resolve) => client.once('sessionUpdated', resolve))
let timer
const done = new Promise((resolve, reject) => {
  timer = setTimeout(() => reject(new Error('等待模型响应超时（60 秒）')), 60000)
  client.on('error', reject)
  client.once('close', () => reject(new Error('响应完成前连接已关闭')))
  client.once('responseDone', (event) => {
    if (event.response?.status === 'completed') resolve()
    else reject(new Error('模型响应未完成'))
  })
})

try {
  await Promise.all([
    done,
    (async () => {
      await client.connect()
      await ready
      for (let offset = 0; offset < pcmBuffer.length; offset += 3200) {
        client.appendAudio(pcmBuffer.subarray(offset, offset + 3200))
        await sleep(100)
      }
      client.commit()
      client.createResponse()
    })(),
  ])
  if (audioChunks.length) await writeFile(process.argv[3] || 'output.pcm', Buffer.concat(audioChunks))
} finally {
  clearTimeout(timer)
  client.close()
}`
}

function ttsCode() {
  const format = $('tts-format').value
  return `import { writeFile } from 'node:fs/promises'
import { SpeechSynthesizer } from 'dashscope-sdk-nodejs'

const synthesizer = new SpeechSynthesizer({
${codeConnectionLines()}
  model: ${JSON.stringify($('tts-model').value.trim())},
  voice: ${JSON.stringify($('tts-voice').value.trim())},
  format: ${JSON.stringify(format)},
  sampleRate: ${Number($('tts-samplerate').value)},
  volume: ${Number($('tts-volume').value)},
  rate: ${Number($('tts-rate').value)},
  pitch: ${Number($('tts-pitch').value)},
})

synthesizer.on('audio', (chunk) => console.log('收到音频分片', chunk.length, 'bytes'))

await synthesizer.begin()
synthesizer.sendText(${$('tts-text').value ? JSON.stringify($('tts-text').value) : "'请输入要合成的文本'"})
const audio = await synthesizer.end()
await writeFile(${JSON.stringify(`tts-output.${format}`)}, audio)`
}

/** 官方文档给出的服务端默认值；与之相同时不写入 run-task。 */
const RASR_DEFAULTS = {
  vadModel: 'far_field_meeting_16k',
  maxSentenceSilence: 800,
  multiThresholdModeEnabled: false,
  heartbeat: false,
  keepDialect: false,
}

/** 读取实时识别调试参数；留空或等于默认值即不下发。 */
function rasrConfig() {
  const config = {
    model: $('rasr-model').value.trim(),
    sampleRate: Number($('rasr-samplerate').value),
    languageHints: $('rasr-langs').value.split(',').map((x) => x.trim()).filter(Boolean),
  }
  const isFunAsr = config.model === 'fun-asr-realtime'
  const vadModel = $('rasr-vad').value
  if (vadModel && !isFunAsr) config.vadModel = vadModel
  const silence = $('rasr-silence').value.trim()
  if (silence) config.maxSentenceSilence = Number(silence)
  const noise = $('rasr-noise').value.trim()
  if (noise) config.speechNoiseThreshold = Number(noise)
  for (const [id, field] of [
    ['rasr-multi-threshold', 'multiThresholdModeEnabled'],
    ['rasr-heartbeat', 'heartbeat'],
    ['rasr-keep-dialect', 'keepDialect'],
  ]) {
    const value = $(id).value
    if (value) config[field] = value === 'true'
  }
  for (const [field, value] of Object.entries(RASR_DEFAULTS)) {
    if (config[field] === value) delete config[field]
  }
  const vocabularyId = $('rasr-vocabulary-id').value.trim()
  if (vocabularyId) config.vocabularyId = vocabularyId
  const vocabulary = $('rasr-vocabulary').value.trim()
  if (vocabulary) {
    try { config.vocabulary = JSON.parse(vocabulary) }
    catch (e) { throw new Error('vocabulary 必须是 {"词": 权重} 形式的 JSON') }
  }
  return config
}

function asrRealtimeCode() {
  let config
  try { config = rasrConfig() }
  catch (e) { return `// 参数无效：${e.message}` }
  const sampleRate = config.sampleRate
  const options = [
    `  model: ${JSON.stringify(config.model)},`,
    `  format: 'pcm',`,
    `  sampleRate: ${sampleRate},`,
    `  languageHints: ${JSON.stringify(config.languageHints)},`,
  ]
  for (const field of ['maxSentenceSilence', 'multiThresholdModeEnabled', 'heartbeat', 'vocabularyId']) {
    if (config[field] !== undefined) options.push(`  ${field}: ${JSON.stringify(config[field])},`)
  }
  const parameters = {}
  if (config.vadModel !== undefined) parameters.vad_model = config.vadModel
  if (config.speechNoiseThreshold !== undefined) parameters.speech_noise_threshold = config.speechNoiseThreshold
  if (config.keepDialect !== undefined) parameters.keep_dialect = config.keepDialect
  if (config.vocabulary !== undefined) parameters.vocabulary = config.vocabulary
  if (Object.keys(parameters).length) {
    options.push(`  parameters: ${JSON.stringify(parameters, null, 2).replace(/\n/g, '\n  ')},`)
  }
  return `import { readFile } from 'node:fs/promises'
import { setTimeout as sleep } from 'node:timers/promises'
import { RecognitionClient } from 'dashscope-sdk-nodejs'

// 输入须为无文件头的 ${sampleRate}Hz / 16bit / 单声道 PCM，不是 WAV 或 MP3。
if (!process.argv[2]) throw new Error('用法：node asr.mjs input.pcm')
const pcmBuffer = await readFile(process.argv[2])
if (!pcmBuffer.length || pcmBuffer.length % 2) throw new Error('PCM 必须非空且包含完整的 16bit 采样')

const client = new RecognitionClient({
${codeConnectionLines()}
${options.join('\n')}
})

client.on('sentenceEnd', ({ text }) => console.log(text))
client.on('error', (error) => console.error(error.message))

try {
  await client.start()
  const chunkBytes = ${sampleRate / 5}
  for (let offset = 0; offset < pcmBuffer.length; offset += chunkBytes) {
    client.sendAudio(pcmBuffer.subarray(offset, offset + chunkBytes))
    await sleep(100)
  }
  await client.finish()
} finally {
  client.close()
}`
}

function currentCodeExample() {
  if (activeCodeTab === 'tts') return ttsCode()
  if (activeCodeTab === 'asr-rt') return asrRealtimeCode()
  return realtimeCode()
}

function updateCodeExample() {
  $('code-title').textContent = CODE_TITLES[activeCodeTab]
  $('node-code').textContent = currentCodeExample()
}

let copyStateTimer = null
function showCopyState(text, state) {
  const button = $('copy-code')
  clearTimeout(copyStateTimer)
  button.textContent = text
  button.dataset.state = state || ''
  copyStateTimer = setTimeout(() => {
    button.textContent = '复制代码'
    button.dataset.state = ''
  }, 1600)
}

function fallbackCopy(text) {
  const textarea = document.createElement('textarea')
  textarea.value = text
  textarea.setAttribute('readonly', '')
  textarea.style.position = 'fixed'
  textarea.style.opacity = '0'
  document.body.appendChild(textarea)
  textarea.select()
  const copied = document.execCommand('copy')
  textarea.remove()
  if (!copied) throw new Error('copy failed')
}

async function copyCodeExample() {
  const code = $('node-code').textContent
  try {
    let copied = false
    if (typeof navigator !== 'undefined' && navigator.clipboard?.writeText) {
      try {
        await navigator.clipboard.writeText(code)
        copied = true
      } catch (error) {
        // 浏览器可能因权限策略拒绝 Clipboard API，继续使用本地选区复制。
      }
    }
    if (!copied) fallbackCopy(code)
    showCopyState('已复制', 'success')
  } catch (error) {
    showCopyState('复制失败', 'error')
  }
}

function bindCodeExample() {
  const ids = [
    'baseUrl', 'rt-model', 'rt-voice', 'rt-turn', 'rt-modalities', 'rt-instructions',
    'tts-model', 'tts-voice', 'tts-format', 'tts-samplerate', 'tts-volume', 'tts-rate', 'tts-pitch', 'tts-text',
    'rasr-model', 'rasr-samplerate', 'rasr-langs', 'rasr-vad', 'rasr-silence', 'rasr-noise',
    'rasr-multi-threshold', 'rasr-heartbeat', 'rasr-keep-dialect', 'rasr-vocabulary-id', 'rasr-vocabulary',
  ]
  for (const id of ids) {
    $(id).addEventListener('input', updateCodeExample)
    $(id).addEventListener('change', updateCodeExample)
  }
  $('copy-code').addEventListener('click', () => { void copyCodeExample() })
  updateCodeExample()
}

function setStatus(el, text, kind) {
  el.textContent = text
  el.className = 'status' + (kind ? ' ' + kind : '')
}

function logData(value, key = '', messageType = '') {
  const name = key.replace(/[-_]/g, '')
  const tokenCount = typeof value === 'number' && /^(maxresponseoutput|input|output|total|cached|text|audio|max|reasoning|completion|prompt)(input|output|completion)?tokens$/i.test(name)
  const tokenDetails = value && typeof value === 'object' && !Array.isArray(value) && /^(input|output)tokendetails$/i.test(name)
  if (!tokenCount && !tokenDetails && /api.?key|authorization|token|password|signature|secret|headers/i.test(key)) return '[REDACTED]'
  if (typeof value === 'string') {
    if (/^(audio|audio_data)$/i.test(key) || (key === 'delta' && /audio\.delta$/.test(messageType))) {
      return { bytes: Math.max(0, Math.floor(value.length * 3 / 4) - (value.match(/=+$/)?.[0].length || 0)), encoding: 'base64 omitted' }
    }
    const secret = getSettings().apiKey
    let text = secret ? value.split(secret).join('[REDACTED]') : value
    text = text.replace(/\b(?:https?|wss?):\/\/[^\s"<>]+/gi, url => url.replace(/\/\/[^/@]+@/, '//').replace(/[?#].*$/, '?[REDACTED]'))
    return text.length > 8192 ? text.slice(0, 8192) + `… (${text.length} chars)` : text
  }
  if (Array.isArray(value)) return value.map(item => logData(item, key, messageType))
  if (value && typeof value === 'object') {
    const type = value.type || messageType
    return Object.fromEntries(Object.entries(value).map(([name, item]) => [name, logData(item, name, type)]))
  }
  return value
}

function debugLog(id, source, event) {
  const data = logData(event)
  const row = document.createElement('div')
  row.className = 'log-entry' + (data.event === 'error' || data.data?.type === 'error' ? ' log-error' : '')
  const timestamp = data.timestamp ?? Date.now()
  row.dataset.timestamp = String(timestamp)
  const time = new Date(timestamp).toISOString().slice(11, 23)
  const [from, to] = source === 'sdk' ? ['Node.js', '百炼'] : ['浏览器', 'Node.js']
  const direction = data.event === 'send' ? `上行 ${from} → ${to}` : data.event === 'receive' ? `下行 ${to} → ${from}` : `${from} ↔ ${to}`
  row.textContent = `[${time}] ${direction} ${data.transport} ${data.event}`
    + (data.method ? ` ${data.method}` : '') + (data.status !== undefined ? ` HTTP ${data.status}` : '')
    + (data.url ? ` ${data.url}` : '') + (data.bytes !== undefined ? ` ${data.bytes} bytes` : '')
    + (data.data !== undefined ? '\n' + JSON.stringify(data.data, null, 2) : '')
  const log = $(source === 'sdk' ? id : `${id}-bridge`)
  const next = Array.from(log.children).find(entry => Number(entry.dataset.timestamp) > timestamp)
  if (next) log.insertBefore(row, next)
  else log.appendChild(row)
  while (log.children.length > 500) log.firstElementChild.remove()
  log.scrollTop = log.scrollHeight
}

function browserLog(id, transport, event, data, extra = {}) {
  debugLog(id, 'browser', { timestamp: Date.now(), transport, event, data, ...extra })
}

function logMessage(id, message) {
  if (message.type === 'trace') debugLog(id, 'sdk', message.event)
  else browserLog(id, 'websocket', 'receive', message)
}

function sendDebug(ws, id, message) {
  const binary = typeof message.byteLength === 'number'
  ws.send(binary ? message : JSON.stringify(message))
  browserLog(id, 'websocket', 'send', binary ? undefined : message, binary ? { bytes: message.byteLength } : {})
}

let rtWs = null
let rtMic = null

function turnDetectionValue() {
  const v = $('rt-turn').value
  if (v === 'push') return null
  if (v === 'smart_turn') return { type: 'smart_turn' }
  return { type: 'server_vad' }
}

function rtStart() {
  if (rtWs) return
  const s = getSettings()
  $('rt-log').innerHTML = ''
  $('rt-log-bridge').innerHTML = ''
  setStatus($('rt-status'), '连接中…', 'busy')
  $('rt-start').disabled = true
  $('rt-stop').disabled = false

  const url = `${wsBase()}/ws/realtime?trace=1`
  browserLog('rt-log', 'websocket', 'connect', undefined, { url })
  const ws = rtWs = new WebSocket(url)
  ws.binaryType = 'arraybuffer'
  const fail = (e) => {
    if (rtWs !== ws) return
    browserLog('rt-log', 'websocket', 'error', { message: e.message })
    setStatus($('rt-status'), '错误', 'err')
    rtTeardown(ws)
  }

  ws.onopen = () => {
    if (rtWs !== ws) return
    browserLog('rt-log', 'websocket', 'open', undefined, { url })
    try {
      sendDebug(ws, 'rt-log', {
        type: 'config',
        ...s,
        model: $('rt-model').value.trim(),
        ...($('rt-voice').value.trim() ? { voice: $('rt-voice').value.trim() } : {}),
        instructions: $('rt-instructions').value.trim(),
        modalities: $('rt-modalities').value.split(','),
        turnDetection: turnDetectionValue(),
      })
    } catch (e) { fail(e) }
  }

  const handleMessage = async (ev) => {
    if (typeof ev.data !== 'string') {
      browserLog('rt-log', 'websocket', 'receive', undefined, { bytes: ev.data.byteLength })
      return
    }
    const m = JSON.parse(ev.data)
    logMessage('rt-log', m)
    if (m.type === 'status') {
      if (m.status === 'open') {
        setStatus($('rt-status'), '已连接', 'ok')
        $('rt-stop').disabled = false
        $('rt-commit').style.display = $('rt-turn').value === 'push' ? '' : 'none'
        await rtStartMic(ws)
      } else if (m.status === 'closed') rtTeardown(ws)
    } else if (m.type === 'error') setStatus($('rt-status'), '错误', 'err')
  }
  ws.onmessage = (ev) => {
    if (rtWs === ws) void handleMessage(ev).catch(fail)
  }

  ws.onerror = () => fail(new Error('WebSocket 错误'))
  ws.onclose = (event) => {
    if (rtWs !== ws) return
    browserLog('rt-log', 'websocket', 'close', { code: event?.code, reason: event?.reason })
    rtTeardown(ws)
  }
}

async function rtStartMic(ws) {
  if (rtWs !== ws || rtMic) return
  const mic = rtMic = new MicRecorder((buf) => {
    if (rtWs !== ws || rtMic !== mic || ws.readyState !== WebSocket.OPEN) return
    try { sendDebug(ws, 'rt-log', buf) }
    catch (e) {
      browserLog('rt-log', 'websocket', 'error', { message: '音频发送失败：' + e.message })
      setStatus($('rt-status'), '错误', 'err')
      rtTeardown(ws)
    }
  })
  try {
    await mic.start(16000)
    if (rtWs !== ws || rtMic !== mic) { mic.stop(); return }
    browserLog('rt-log', 'websocket', 'open', { resource: 'microphone', sampleRate: 16000 })
  } catch (e) {
    mic.stop()
    if (rtWs !== ws || rtMic !== mic) return
    rtMic = null
    browserLog('rt-log', 'websocket', 'error', { resource: 'microphone', message: e.message })
  }
}

function rtTeardown(ws = rtWs) {
  if (rtWs !== ws) return
  rtWs = null // 先失效身份，避免 close 回调影响下一次连接
  try { rtMic && rtMic.stop() } catch (e) {}
  rtMic = null
  if (ws && ws.readyState !== 3) browserLog('rt-log', 'websocket', 'close', { reason: 'local teardown' })
  try { ws && ws.close() } catch (e) {}
  $('rt-start').disabled = false
  $('rt-stop').disabled = true
  $('rt-commit').style.display = 'none'
  if ($('rt-status').textContent !== '错误') setStatus($('rt-status'), '未连接')
}

function rtStop() {
  rtTeardown()
}

function rtSendControl(message) {
  const ws = rtWs
  if (!ws || ws.readyState !== WebSocket.OPEN) return false
  try { sendDebug(ws, 'rt-log', message); return true }
  catch (e) {
    browserLog('rt-log', 'websocket', 'error', { message: '发送失败：' + e.message })
    setStatus($('rt-status'), '错误', 'err')
    rtTeardown(ws)
    return false
  }
}

function rtSendText() {
  const text = $('rt-text').value.trim()
  if (!text) return
  if (!rtWs || rtWs.readyState !== WebSocket.OPEN) { alert('请先点击「连接并开始」'); return }
  if (!rtSendControl({ type: 'text', text })) return
  $('rt-text').value = ''
}

function bindRealtime() {
  const syncVoices = () => {
    const version = $('rt-model').value.trim().match(/^qwen-audio-3\.(0|1)-realtime-(?:plus|flash)$/)?.[1]
    const voice = $('rt-voice')
    for (const option of voice.options) {
      const incompatible = Boolean(option.value && version && option.value.endsWith('_v3.1') !== (version === '1'))
      option.disabled = incompatible
      option.hidden = incompatible
    }
    if (Array.from(voice.options).some((option) => option.value === voice.value && option.disabled)) {
      voice.value = ''
      localStorage.setItem('ds_rt-voice', '')
    }
    updateCodeExample()
  }
  $('rt-model').addEventListener('input', syncVoices)
  $('rt-model').addEventListener('change', syncVoices)
  syncVoices()
  $('rt-start').addEventListener('click', rtStart)
  $('rt-stop').addEventListener('click', rtStop)
  $('rt-commit').addEventListener('click', () => {
    if (rtSendControl({ type: 'commit' })) rtSendControl({ type: 'respond' })
  })
  $('rt-send-text').addEventListener('click', rtSendText)
  $('rt-text').addEventListener('keydown', (e) => { if (e.key === 'Enter') rtSendText() })
  $('rt-turn').addEventListener('change', () => {
    if (rtWs && rtWs.readyState === WebSocket.OPEN) $('rt-commit').style.display = $('rt-turn').value === 'push' ? '' : 'none'
  })
}

/* =========================================================
 * 模块二：TTS 语音合成（WebSocket 流式）
 * =======================================================*/
let ttsWs = null

function ttsRun() {
  if (ttsWs) return
  const s = getSettings()
  $('tts-log').innerHTML = ''
  $('tts-log-bridge').innerHTML = ''
  setStatus($('tts-status'), '连接中…', 'busy')
  $('tts-run').disabled = true

  let bytes = 0
  const url = `${wsBase()}/ws/tts?trace=1`
  browserLog('tts-log', 'websocket', 'connect', undefined, { url })
  const ws = ttsWs = new WebSocket(url)
  ws.binaryType = 'arraybuffer'
  const fail = (e) => {
    if (ttsWs !== ws) return
    browserLog('tts-log', 'websocket', 'error', { message: e.message })
    ttsTeardown(ws, '失败', 'err')
  }

  ws.onopen = () => {
    if (ttsWs !== ws) return
    browserLog('tts-log', 'websocket', 'open', undefined, { url })
    try {
      sendDebug(ws, 'tts-log', {
        type: 'config',
        ...s,
        model: $('tts-model').value.trim(),
        voice: $('tts-voice').value.trim(),
        format: $('tts-format').value,
        sampleRate: Number($('tts-samplerate').value),
        volume: Number($('tts-volume').value),
        rate: Number($('tts-rate').value),
        pitch: Number($('tts-pitch').value),
        text: $('tts-text').value,
      })
    } catch (e) { fail(e) }
  }

  ws.onmessage = (ev) => {
    if (ttsWs !== ws) return
    if (typeof ev.data !== 'string') {
      bytes += ev.data.byteLength
      browserLog('tts-log', 'websocket', 'receive', { totalBytes: bytes }, { bytes: ev.data.byteLength })
      return
    }
    try {
      const m = JSON.parse(ev.data)
      logMessage('tts-log', m)
      if (m.type === 'status') {
        if (m.status === 'started') setStatus($('tts-status'), '合成中…', 'busy')
        else if (m.status === 'finished') ttsTeardown(ws, `已完成 · ${bytes} bytes`, 'ok')
        else if (m.status === 'closed') fail(new Error('连接在合成完成前关闭'))
      } else if (m.type === 'error') fail(new Error(m.message))
    } catch (e) { fail(e) }
  }

  ws.onerror = () => fail(new Error('WebSocket 错误'))
  ws.onclose = (event) => {
    if (ttsWs !== ws) return
    browserLog('tts-log', 'websocket', 'close', { code: event?.code, reason: event?.reason })
    fail(new Error('连接在合成完成前关闭'))
  }
}

function ttsTeardown(ws, text, kind) {
  if (ttsWs !== ws) return
  ttsWs = null
  if (ws && ws.readyState !== 3) browserLog('tts-log', 'websocket', 'close', { reason: text })
  try { ws && ws.close() } catch (e) {}
  setStatus($('tts-status'), text, kind)
  $('tts-run').disabled = false
}

function bindTts() {
  $('tts-run').addEventListener('click', ttsRun)
  ;['tts-volume', 'tts-rate', 'tts-pitch'].forEach((id) => $(id).addEventListener('input', syncRangeLabels))
}

/* =========================================================
 * 模块三：实时识别 ASR（WebSocket 流式）
 * =======================================================*/
let rasrWs = null
let rasrMic = null
let rasrFinishing = false
let rasrFinishTimer = null

function rasrStart() {
  if (rasrWs) return
  let config
  try { config = rasrConfig() }
  catch (e) {
    browserLog('rasr-log', 'websocket', 'error', { message: e.message })
    setStatus($('rasr-status'), '参数无效', 'err')
    return
  }
  const s = getSettings()
  $('rasr-log').innerHTML = ''
  $('rasr-log-bridge').innerHTML = ''
  setStatus($('rasr-status'), '连接中…', 'busy')
  $('rasr-start').disabled = true
  $('rasr-stop').disabled = false // 握手或麦克风授权未完成时也允许取消
  rasrFinishing = false

  const url = `${wsBase()}/ws/asr?trace=1`
  browserLog('rasr-log', 'websocket', 'connect', undefined, { url })
  const ws = rasrWs = new WebSocket(url)
  ws.binaryType = 'arraybuffer'
  const fail = (e) => {
    if (rasrWs !== ws) return
    browserLog('rasr-log', 'websocket', 'error', { message: e.message })
    rasrTeardown(ws, '错误', 'err')
  }
  ws.onopen = () => {
    if (rasrWs !== ws) return
    browserLog('rasr-log', 'websocket', 'open', undefined, { url })
    try {
      sendDebug(ws, 'rasr-log', { type: 'config', ...s, ...config })
    } catch (e) { fail(e) }
  }
  ws.onmessage = (ev) => {
    if (rasrWs !== ws || typeof ev.data !== 'string') return
    void (async () => {
      const m = JSON.parse(ev.data)
      logMessage('rasr-log', m)
      switch (m.type) {
        case 'status':
          if (m.status === 'started') {
            if (rasrFinishing || rasrMic) return
            setStatus($('rasr-status'), '识别中', 'ok')
            const mic = rasrMic = new MicRecorder((buf) => {
              if (rasrWs !== ws || rasrMic !== mic || rasrFinishing || ws.readyState !== WebSocket.OPEN) return
              try { sendDebug(ws, 'rasr-log', buf) } catch (e) { fail(e) }
            })
            try {
              await mic.start(Number($('rasr-samplerate').value))
              if (rasrWs !== ws || rasrMic !== mic || rasrFinishing) mic.stop()
            } catch (e) {
              mic.stop()
              if (rasrWs === ws && rasrMic === mic) fail(new Error('麦克风不可用：' + e.message))
            }
          } else if (m.status === 'finished') {
            rasrTeardown(ws, '已完成', 'ok')
          } else if (m.status === 'closed') {
            fail(new Error('连接在识别完成前关闭'))
          }
          break
        case 'error': fail(new Error(m.message)); break
        default: break
      }
    })().catch(fail)
  }
  ws.onerror = () => fail(new Error('WebSocket 错误'))
  ws.onclose = (event) => {
    if (rasrWs !== ws) return
    browserLog('rasr-log', 'websocket', 'close', { code: event?.code, reason: event?.reason })
    fail(new Error('连接在识别完成前关闭'))
  }
}

function rasrTeardown(ws, text, kind) {
  if (rasrWs !== ws) return
  rasrWs = null
  clearTimeout(rasrFinishTimer)
  rasrFinishTimer = null
  rasrFinishing = false
  try { rasrMic && rasrMic.stop() } catch (e) {}
  rasrMic = null
  if (ws && ws.readyState !== 3) browserLog('rasr-log', 'websocket', 'close', { reason: text })
  try { ws && ws.close() } catch (e) {}
  $('rasr-start').disabled = false
  $('rasr-stop').disabled = true
  $('rasr-stop').textContent = '结束'
  setStatus($('rasr-status'), text, kind)
}

function rasrStop() {
  const ws = rasrWs
  if (!ws) return
  if (rasrFinishing || ws.readyState !== WebSocket.OPEN || !rasrMic) {
    rasrTeardown(ws, '已取消')
    return
  }
  rasrFinishing = true
  try { rasrMic.stop() } catch (e) {}
  rasrMic = null
  $('rasr-stop').textContent = '取消等待'
  setStatus($('rasr-status'), '等待最终识别结果…', 'busy')
  // 超时只能报告失败并取消，绝不能以本地计时推断 task-finished。
  rasrFinishTimer = setTimeout(() => {
    rasrTeardown(ws, '等待识别完成超时，已取消', 'err')
  }, 30_000)
  try { sendDebug(ws, 'rasr-log', { type: 'finish' }) }
  catch (e) {
    browserLog('rasr-log', 'websocket', 'error', { message: e.message })
    rasrTeardown(ws, '结束失败', 'err')
  }
}

function bindAsrRealtime() {
  const syncVad = () => {
    const hide = $('rasr-model').value.trim() === 'fun-asr-realtime'
    $('rasr-vad').disabled = hide
  }
  $('rasr-model').addEventListener('input', syncVad)
  $('rasr-model').addEventListener('change', syncVad)
  syncVad()
  $('rasr-start').addEventListener('click', rasrStart)
  $('rasr-stop').addEventListener('click', rasrStop)
}

// ---------- 启动 ----------
document.addEventListener('DOMContentLoaded', () => {
  loadSettings()
  bindPersist()
  bindTabs()
  bindCodeExample()
  bindRealtime()
  bindTts()
  bindAsrRealtime()
  $('save-shared-settings').addEventListener('click', saveSharedSettings)
  void loadSharedSettings()
})
