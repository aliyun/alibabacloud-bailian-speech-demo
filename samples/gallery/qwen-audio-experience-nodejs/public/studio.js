/* Independent ASR / TTS / Realtime pages. Load audio.js before this script. */
(() => {
  'use strict'

  function boot() {
    const $ = (id) => document.getElementById(id)
    const page = document.body.dataset.page
    if (!['asr', 'tts', 'realtime'].includes(page)) return
    // Connection settings live only in this browser; the local server never stores them.
    const STORAGE_KEY = 'qwenAudio.connection'
    const FIELDS = { apiKey: 'api-key', workspaceId: 'workspace-id', baseUrl: 'base-url' }
    const storedCredentials = () => {
      let saved = {}
      try { saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}') || {} } catch (_) {}
      return Object.fromEntries(Object.keys(FIELDS).map((key) => [key, typeof saved[key] === 'string' ? saved[key] : '']))
    }

    let current = null
    let revision = 0
    let objectURL = null
    let serverConfigured = false
    const wave = makeWaveform($('waveform'))
    const labels = { asr: '开始听写', tts: '听见这段文字', realtime: '开始对话' }
    const layout = window.matchMedia('(min-width: 761px)')
    const syncDetails = () => document.querySelectorAll('.settings-details').forEach((details) => { details.open = layout.matches })
    syncDetails()
    layout.addEventListener('change', syncDetails)
    const credentials = storedCredentials
    const alive = (s) => current === s && !s.disposed
    const notice = (message) => {
      $('notice').textContent = String(message || '操作失败，请重试')
      $('notice').hidden = false
    }
    const showConnectionSettings = () => {
      const saved = storedCredentials()
      for (const [key, id] of Object.entries(FIELDS)) $(id).value = saved[key]
      $('api-key').placeholder = serverConfigured ? '留空则使用服务端 .env 配置' : '请输入 DashScope API Key'
      const label = $('api-key-status')
      if (label) label.textContent = saved.apiKey ? '已保存在本浏览器' : serverConfigured ? '使用服务端 .env 配置' : '需要设置'
      return Boolean(saved.apiKey || serverConfigured)
    }
    const loadConnectionSettings = async () => {
      try {
        const response = await fetch('/api/settings', { cache: 'no-store' })
        const status = await response.json()
        if (!response.ok) throw new Error(status.error || `HTTP ${response.status}`)
        serverConfigured = status.serverConfigured === true
      } catch (error) {
        notice(`读取服务端配置失败：${error.message || error}`)
      }
      if (!showConnectionSettings() && !$('settings-dialog').open) $('settings-dialog').showModal()
    }
    const saveConnectionSettings = () => {
      const next = Object.fromEntries(Object.entries(FIELDS).map(([key, id]) => [key, $(id).value.trim()]))
      try {
        if (!next.apiKey && (next.workspaceId || next.baseUrl)) throw new Error('填写 Workspace ID 或服务域名时，请同时填写 API Key')
        if (!next.apiKey && !serverConfigured) throw new Error('请填写 API Key，或在服务端 .env 中配置 DASHSCOPE_API_KEY')
        if (next.apiKey) localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
        else localStorage.removeItem(STORAGE_KEY)
      } catch (error) {
        notice(error.message || error)
        $('api-key').focus()
        return
      }
      showConnectionSettings()
      $('settings-dialog').close()
      $('notice').hidden = true
    }
    const state = (kind, text) => {
      document.body.dataset.state = kind
      $('status').dataset.state = kind
      $('status').textContent = text
    }
    const locks = (busy) => {
      $('controls').disabled = busy
      $('open-settings').disabled = busy
      $('start').disabled = busy
      $('start').hidden = busy
      $('start').textContent = busy ? '进行中' : labels[page]
      $('stop').hidden = !busy
      $('stop').disabled = !busy
      if (page === 'tts') {
        $('text').disabled = busy
        document.querySelectorAll('button[data-sample]').forEach((button) => { button.disabled = busy })
      }
    }
    const clearTimer = (s, name) => {
      clearTimeout(s.timers.get(name))
      s.timers.delete(name)
    }
    const later = (s, name, fn, delay) => {
      clearTimer(s, name)
      s.timers.set(name, setTimeout(() => {
        s.timers.delete(name)
        if (alive(s)) fn()
      }, delay))
    }
    const startClock = (s) => {
      if (s.clock) return
      s.began = Date.now()
      const update = () => {
        if (!alive(s)) return
        const seconds = Math.floor((Date.now() - s.began) / 1000)
        $('elapsed').textContent = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`
      }
      update()
      s.clock = setInterval(update, 1000)
    }
    const begin = () => {
      if (current) return null
      const s = { revision: ++revision, timers: new Map(), disposed: false, ready: false }
      current = s
      $('notice').hidden = true
      $('notice').textContent = ''
      $('elapsed').textContent = '00:00'
      locks(true)
      $('start').textContent = '连接中'
      $('stop').textContent = '取消连接'
      state('connecting', '正在连接')
      return s
    }
    const closeSocket = (s) => {
      const ws = s.ws
      s.ws = null
      if (!ws) return
      ws.onopen = ws.onmessage = ws.onclose = ws.onerror = null
      try { ws.close() } catch (_) {}
    }
    const stopMic = (s) => {
      const mic = s.mic
      s.mic = null
      s.micReady = false
      if (mic) mic.stop()
    }
    const end = (s, text, kind = 'idle') => {
      if (!alive(s)) return
      // Invalidate identity BEFORE closing anything: close/permission/onended may be late.
      current = null
      s.disposed = true
      for (const timer of s.timers.values()) clearTimeout(timer)
      s.timers.clear()
      clearInterval(s.clock)
      stopMic(s)
      if (s.player) { s.player.destroy(); s.player = null }
      s.chunks = null
      closeSocket(s)
      wave.reset()
      locks(false)
      state(kind, text)
      if (page === 'asr') updateTranscript()
      if (page === 'realtime') {
        $('mute').disabled = true
        $('mute').setAttribute('aria-pressed', 'false')
        $('mute').textContent = '静音'
        $('commit').hidden = true
        $('commit').disabled = true
        $('send').disabled = true
        $('orb-label').textContent = kind === 'error' ? '连接已中断' : '静候你的声音'
        $('session-hint').textContent = kind === 'error' ? '请查看提示，调整后重新连接' : '自然开口，随时打断'
      }
    }
    const fail = (s, error) => {
      if (!alive(s)) return
      notice(error instanceof Error ? error.message : String(error))
      end(s, '发生错误', 'error')
    }
    const send = (s, message) => {
      if (!alive(s)) return false
      try {
        if (!s.ws || s.ws.readyState !== WebSocket.OPEN) throw new Error('连接不可用，请重新开始')
        if (s.ws.bufferedAmount > 4 * 1024 * 1024) throw new Error('网络发送拥堵，已停止以避免音频积压')
        s.ws.send(message instanceof ArrayBuffer ? message : JSON.stringify(message))
        return true
      } catch (e) { fail(s, e); return false }
    }
    const connect = (s, path, config, onMessage, onBinary) => {
      try {
        const ws = new WebSocket(`${location.protocol === 'https:' ? 'wss' : 'ws'}://${location.host}${path}`)
        s.ws = ws
        ws.binaryType = 'arraybuffer'
        const valid = () => alive(s) && s.ws === ws
        ws.onopen = () => { if (valid()) send(s, { type: 'config', ...config }) }
        ws.onmessage = (event) => {
          if (!valid()) return
          try {
            if (typeof event.data !== 'string') {
              if (!onBinary || !(event.data instanceof ArrayBuffer)) throw new Error('收到无效音频数据')
              onBinary(event.data)
              return
            }
            const message = JSON.parse(event.data)
            if (!message || typeof message !== 'object') throw new Error('收到无效服务消息')
            if (message.type === 'error') { fail(s, new Error(String(message.message || '服务返回错误'))); return }
            onMessage(message)
          } catch (e) { fail(s, e) }
        }
        ws.onerror = () => { if (valid()) fail(s, new Error('连接失败，请确认本地服务已启动并检查网络')) }
        ws.onclose = () => { if (valid()) fail(s, new Error('连接意外关闭，任务未完成')) }
      } catch (e) { fail(s, e) }
    }
    const openPlayer = (s, onDrain) => {
      const player = s.player = new GesturePlayer(wave, () => {
        if (alive(s)) onDrain()
      }, (e) => fail(s, e))
      // This call MUST stay in the click stack, before getUserMedia or any await.
      player.unlock().catch((e) => fail(s, new Error(`无法播放音频：${e.message}。请检查浏览器音频权限后重新点击开始。`)))
      return player
    }
    const openMic = (s, sampleRate, onReady, onError) => {
      const mic = s.mic = new GestureMic((buffer) => {
        if (!alive(s) || s.mic !== mic || !s.ready || s.finishing || s.muted) return
        if (send(s, buffer)) {
          s.hasInput = true
          wave.feed(buffer)
          if (page === 'realtime') updateRealtime(s)
        }
      })
      const unavailable = (e) => {
        mic.stop()
        if (!alive(s) || s.mic !== mic) return
        s.mic = null
        s.micReady = false
        onError(new Error(`麦克风不可用：${e.message || '请检查录音权限及设备'}`))
      }
      mic.onFailure = unavailable
      // The recorder creates/resumes its context synchronously, even if permission is pending.
      mic.start(sampleRate).then(() => {
        if (!alive(s) || s.mic !== mic || s.finishing) { mic.stop(); return }
        s.micReady = true
        onReady()
      }).catch(unavailable)
    }

    $('open-settings').addEventListener('click', () => {
      showConnectionSettings()
      $('settings-dialog').showModal()
    })
    // Discard unsaved edits so the inputs always match what requests will use.
    $('settings-dialog').addEventListener('close', () => { showConnectionSettings() })
    $('close-settings').addEventListener('click', () => { $('settings-dialog').close() })
    $('save-settings').addEventListener('click', saveConnectionSettings)
    // Enter in a settings form must never navigate or put credentials in the URL.
    $('settings-dialog').addEventListener('submit', (event) => { event.preventDefault(); saveConnectionSettings() })
    void loadConnectionSettings()

    // ASR -------------------------------------------------------------------
    const transcriptText = () => [...$('transcript').children].map((line) => line.textContent).concat($('partial').textContent).filter(Boolean).join('\n')
    function updateTranscript() {
      const text = transcriptText()
      $('transcript-placeholder').hidden = !!text
      $('word-count').textContent = String(Array.from(text.replace(/\s/g, '')).length)
      $('copy').disabled = !text
      $('clear').disabled = !!current || !text
    }
    function resetTranscript() {
      $('transcript').textContent = ''
      $('partial').textContent = ''
      updateTranscript()
    }
    function appendSentence(text) {
      if (text) {
        const line = document.createElement('div')
        line.className = 'transcript-line'
        line.textContent = text
        $('transcript').appendChild(line)
      }
      $('partial').textContent = ''
      updateTranscript()
    }
    function startAsr() {
      const s = begin()
      if (!s) return
      resetTranscript()
      const sampleRate = 16000
      const ready = () => {
        if (!s.ready || !s.micReady || s.finishing) return
        clearTimer(s, 'connect')
        startClock(s)
        state('active', '正在识别')
        $('start').textContent = '识别中'
        $('stop').textContent = '结束识别'
      }
      later(s, 'connect', () => fail(s, new Error('连接或麦克风授权等待超过 30 秒，已取消')), 30000)
      openMic(s, sampleRate, ready, (e) => fail(s, e))
      connect(s, '/ws/asr', {
        ...credentials(), model: $('model').value, sampleRate,
        ...($('vad-model').disabled ? {} : { vadModel: $('vad-model').value }),
      }, (m) => {
        const viewport = $('transcript-scroll')
        const follow = viewport.scrollHeight - viewport.scrollTop - viewport.clientHeight < 80
        if (m.type === 'status') {
          if (m.status === 'started' && !s.finishing) { s.ready = true; ready() }
          else if (m.status === 'finished') end(s, '识别完成')
          else if (m.status === 'closed') fail(s, new Error('识别完成前连接已关闭，结果可能不完整'))
        } else if (m.type === 'result') {
          const text = typeof m.text === 'string' ? m.text : ''
          if (m.end) { appendSentence(text); s.pendingEnd = text }
          else { s.pendingEnd = null; $('partial').textContent = text; updateTranscript() }
        } else if (m.type === 'sentenceEnd') {
          const text = typeof m.text === 'string' ? m.text : ''
          // The bridge emits both result(end=true) and sentenceEnd for one sentence.
          if (s.pendingEnd !== text) appendSentence(text)
          s.pendingEnd = null
        }
        if (follow) viewport.scrollTop = viewport.scrollHeight
      })
    }
    function stopAsr() {
      const s = current
      if (!s) return
      if (s.finishing || !s.ready) { end(s, '已取消'); return }
      s.finishing = true
      stopMic(s)
      wave.reset()
      clearTimer(s, 'connect')
      clearInterval(s.clock)
      state('finishing', '正在等待最终识别结果')
      $('start').textContent = '收尾中'
      $('stop').textContent = '取消等待'
      later(s, 'finish', () => fail(s, new Error('等待最终识别结果超过 30 秒，已取消；已有结果可能不完整')), 30000)
      send(s, { type: 'finish' })
    }

    // TTS -------------------------------------------------------------------
    function releaseAudio() {
      $('audio').pause()
      $('audio').removeAttribute('src')
      $('audio').load()
      $('download').removeAttribute('href')
      $('audio-result').hidden = true
      if (objectURL) URL.revokeObjectURL(objectURL)
      objectURL = null
    }
    function ttsDrain(s) {
      if (s.generated) end(s, '生成完成，可回放或下载')
      else { wave.reset(); state('active', '正在合成'); $('stop').textContent = '停止生成' }
    }
    function finishTts(s) {
      if (s.generated) return
      if (!s.bytes || s.pendingByte !== null) throw new Error('服务未返回完整的 PCM 音频，无法生成回放文件')
      const header = new ArrayBuffer(44)
      const view = new DataView(header)
      const ascii = (at, text) => { for (let i = 0; i < text.length; i++) view.setUint8(at + i, text.charCodeAt(i)) }
      ascii(0, 'RIFF'); view.setUint32(4, 36 + s.bytes, true); ascii(8, 'WAVE')
      ascii(12, 'fmt '); view.setUint32(16, 16, true); view.setUint16(20, 1, true)
      view.setUint16(22, 1, true); view.setUint32(24, 24000, true); view.setUint32(28, 48000, true)
      view.setUint16(32, 2, true); view.setUint16(34, 16, true); ascii(36, 'data'); view.setUint32(40, s.bytes, true)
      const blob = new Blob([header, ...s.chunks], { type: 'audio/wav' })
      objectURL = URL.createObjectURL(blob)
      $('audio').src = objectURL
      $('download').href = objectURL
      $('download').download = 'qwen-audio.wav'
      $('audio-meta').textContent = `${blob.size.toLocaleString()} 字节 · ${(s.bytes / 48000).toFixed(1)} 秒 · WAV / 24 kHz`
      $('audio-result').hidden = false
      s.generated = true
      s.chunks = null
      clearTimer(s, 'progress')
      closeSocket(s)
      if (s.player.sources.size) {
        state('finishing', '已生成，正在播放')
        $('start').textContent = '播放中'
        $('stop').textContent = '停止播放'
      } else ttsDrain(s)
    }
    function startTts() {
      if (current) return
      const text = $('text').value.trim()
      if (!text) { notice('请先输入需要合成的文字'); $('text').focus(); return }
      if (text.length > 20000) { notice('文字不能超过 20,000 个字符'); return }
      const voice = document.querySelector('input[name="voice"]:checked')
      const rate = Number($('rate').value)
      if (!voice || !Number.isFinite(rate) || rate < 0.5 || rate > 2) { notice('请选择音色及有效语速'); return }
      const s = begin()
      if (!s) return
      releaseAudio()
      s.chunks = []
      s.bytes = 0
      s.pendingByte = null
      const progress = () => later(s, 'progress', () => fail(s, new Error('语音合成超过 60 秒没有进展，已取消，请重试')), 60000)
      try { openPlayer(s, () => ttsDrain(s)) } catch (e) { fail(s, e); return }
      progress()
      connect(s, '/ws/tts', { ...credentials(), model: $('model').value, voice: voice.value, rate, text }, (m) => {
        if (m.type !== 'status') return
        if (m.status === 'started' && !s.ready) {
          s.ready = true
          startClock(s)
          state('active', '正在合成')
          $('start').textContent = '生成中'
          $('stop').textContent = '停止生成'
          progress()
        } else if (m.status === 'finished') finishTts(s)
        else if (m.status === 'closed' && !s.generated) fail(s, new Error('语音生成完成前连接已关闭'))
      }, (buffer) => {
        if (s.generated || !buffer.byteLength) return
        progress()
        startClock(s)
        s.bytes += buffer.byteLength
        // Avoid unbounded memory on a malformed/endless stream (about 45 minutes of PCM).
        if (s.bytes > 128 * 1024 * 1024) throw new Error('音频过长，已停止生成，请缩短文本')
        s.chunks.push(buffer)
        let bytes = new Uint8Array(buffer)
        if (s.pendingByte !== null) {
          const joined = new Uint8Array(bytes.length + 1)
          joined[0] = s.pendingByte
          joined.set(bytes, 1)
          bytes = joined
          s.pendingByte = null
        }
        if (bytes.length % 2) { s.pendingByte = bytes[bytes.length - 1]; bytes = bytes.slice(0, -1) }
        if (bytes.length) s.player.feed(bytes.buffer)
        state('active', '正在生成并播放')
        $('start').textContent = '生成中'
        $('stop').textContent = '停止生成与播放'
      })
    }
    function stopTts() {
      $('audio').pause()
      if (current) end(current, current.generated ? '已生成，播放已停止' : '已取消生成')
    }

    // Realtime --------------------------------------------------------------
    function updateRealtime(s) {
      if (!alive(s)) return
      $('send').disabled = !s.ready
      $('mute').disabled = !s.ready || !s.micReady
      $('mute').setAttribute('aria-pressed', String(!!s.muted))
      $('mute').textContent = s.muted ? '取消静音' : '静音'
      $('commit').hidden = s.turn !== 'push'
      $('commit').disabled = !s.ready || !s.micReady || s.muted || !s.hasInput
      if (!s.ready) return
      let label
      if (s.player && s.player.sources.size) label = '正在播放回复'
      else if (s.speaking) label = '正在听你说'
      else if (s.responding) label = '正在思考回复'
      else if (s.muted) label = '麦克风已静音'
      else if (s.micReady) label = s.turn === 'push' ? '说完后发送这一轮' : '正在聆听'
      else label = s.micDenied ? '文字对话已就绪' : '等待麦克风授权'
      state('active', label)
      $('start').textContent = '对话中'
      $('stop').textContent = '结束对话'
      $('orb-label').textContent = label
      $('session-hint').textContent = s.micDenied ? '麦克风不可用，仍可在下方输入文字' : s.muted ? '点击取消静音，或继续文字对话' : s.turn === 'push' ? '说完后点击「发送这一轮」，也可输入文字' : '自然开口，随时打断'
    }
    function bubble(role, text) {
      const element = document.createElement('div')
      element.className = `message ${role}`
      element.dataset.role = role
      element.textContent = text
      $('conversation').appendChild(element)
      $('conversation-empty').hidden = true
      return element
    }
    function updateBubble(s, role, text, done) {
      const key = `${role}Bubble`
      const list = $('conversation')
      const follow = list.scrollHeight - list.scrollTop - list.clientHeight < 100
      if (!s[key]) s[key] = bubble(role, '')
      if (done) s[key].textContent = text || s[key].textContent
      else if (role === 'user') s[key].textContent = text
      else s[key].textContent += text
      if (done) s[key] = null
      if (follow) list.scrollTop = list.scrollHeight
    }
    function startRealtime() {
      const s = begin()
      if (!s) return
      $('conversation').textContent = ''
      $('conversation-empty').hidden = false
      s.turn = $('turn').value
      s.muted = false
      s.hasInput = false
      $('orb-label').textContent = '正在建立连接'
      $('session-hint').textContent = '请允许麦克风权限，也可使用文字对话'
      updateRealtime(s)
      try { openPlayer(s, () => updateRealtime(s)) } catch (e) { fail(s, e); return }
      openMic(s, 16000, () => updateRealtime(s), (e) => {
        s.micDenied = true
        notice(`${e.message}。仍可使用下方文本框对话。`)
        updateRealtime(s)
      })
      later(s, 'connect', () => fail(s, new Error('对话连接超过 30 秒未就绪，已取消')), 30000)
      connect(s, '/ws/realtime', {
        ...credentials(), model: $('model').value,
        ...($('voice').value ? { voice: $('voice').value } : {}),
        modalities: $('modalities').value.split(','), instructions: $('instructions').value.trim(),
        inputTranscription: { language: 'zh' },
        turnDetection: s.turn === 'push' ? null : { type: s.turn === 'smart_turn' ? 'smart_turn' : 'server_vad' },
      }, (m) => {
        switch (m.type) {
          case 'status':
            if (m.status === 'open') { s.ready = true; clearTimer(s, 'connect'); startClock(s); updateRealtime(s) }
            else if (m.status === 'closed') fail(s, new Error('对话连接已关闭，请重新连接'))
            break
          case 'speechStarted':
            s.speaking = true
            s.responding = false
            s.aiBubble = null
            if (s.turn !== 'push') s.player.clear()
            updateRealtime(s)
            break
          case 'speechStopped': s.speaking = false; s.responding = true; updateRealtime(s); break
          case 'responseCreated': s.responding = true; updateRealtime(s); break
          case 'responseDone': s.responding = false; s.aiBubble = null; updateRealtime(s); break
          case 'userDelta': updateBubble(s, 'user', (typeof m.text === 'string' ? m.text : '') + (typeof m.stash === 'string' ? m.stash : ''), false); break
          case 'userText': updateBubble(s, 'user', typeof m.transcript === 'string' ? m.transcript : '', true); break
          case 'aiDelta': updateBubble(s, 'ai', typeof m.delta === 'string' ? m.delta : '', false); break
          case 'aiText': updateBubble(s, 'ai', typeof m.transcript === 'string' ? m.transcript : '', true); break
          default: break
        }
      }, (buffer) => {
        if (!buffer.byteLength) return
        if (buffer.byteLength % 2) throw new Error('收到不完整的实时 PCM 音频')
        s.player.feed(buffer)
        updateRealtime(s)
      })
    }
    function sendText() {
      const s = current
      const text = $('message').value.trim()
      if (!s || !s.ready || !text) return
      if (!send(s, { type: 'text', text })) return
      bubble('user', text)
      $('message').value = ''
      s.responding = true
      updateRealtime(s)
      $('conversation').scrollTop = $('conversation').scrollHeight
    }

    locks(false)
    state('idle', '准备就绪')
    $('elapsed').textContent = '00:00'
    if (page === 'asr') {
      const syncVad = () => {
        const hide = $('model').value === 'fun-asr-realtime'
        $('vad-model').disabled = hide
        $('vad-model').hidden = hide
      }
      $('model').addEventListener('change', syncVad)
      syncVad()
      updateTranscript()
      $('start').addEventListener('click', startAsr)
      $('stop').addEventListener('click', stopAsr)
      $('clear').addEventListener('click', () => { if (!current) resetTranscript() })
      $('copy').addEventListener('click', async () => {
        const version = revision
        const text = transcriptText()
        if (!text) return
        try {
          if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error('浏览器不支持剪贴板访问')
          await navigator.clipboard.writeText(text)
        } catch (_) { if (version === revision) notice('复制失败，请允许剪贴板权限，或手动选择识别文字复制') }
      })
    } else if (page === 'tts') {
      const updateText = () => { $('char-count').textContent = String($('text').value.length) }
      const updateRate = () => { $('rate-value').textContent = `${Number($('rate').value).toFixed(1)}×` }
      $('text').addEventListener('input', updateText)
      $('rate').addEventListener('input', updateRate)
      updateText(); updateRate()
      const samples = {
        daily: '早上好。给自己泡一杯茶，让今天从一个从容的微笑开始。',
        travel: '下一站，去看看海。沿着海边慢慢走，让风带走旅途的疲惫。',
        greeting: '你好，很高兴遇见你。愿这段温柔的声音，陪你度过美好的一天。',
      }
      document.querySelectorAll('button[data-sample]').forEach((button) => button.addEventListener('click', () => {
        if (!current && samples[button.dataset.sample]) { $('text').value = samples[button.dataset.sample]; updateText() }
      }))
      $('start').addEventListener('click', startTts)
      $('stop').addEventListener('click', stopTts)
      $('audio').addEventListener('play', () => {
        // Native replay is explicit; never overlap it with the streaming player.
        if (current) {
          if (current.generated) end(current, '已生成，正在回放')
          else $('audio').pause()
        }
      })
      $('audio').addEventListener('error', () => {
        if (objectURL) notice('音频无法解码或播放，请重新生成，或下载 WAV 文件后播放')
      })
    } else {
      const syncVoices = () => {
        const version = $('model').value.match(/^qwen-audio-3\.(0|1)-realtime-(?:plus|flash)$/)?.[1]
        const voice = $('voice')
        for (const option of voice.options) {
          const incompatible = Boolean(option.value && version && option.value.endsWith('_v3.1') !== (version === '1'))
          option.disabled = incompatible
          option.hidden = incompatible
        }
        if (Array.from(voice.options).some((option) => option.value === voice.value && option.disabled)) voice.value = ''
      }
      $('model').addEventListener('change', syncVoices)
      syncVoices()
      $('start').addEventListener('click', startRealtime)
      $('stop').addEventListener('click', () => { if (current) end(current, '对话已结束') })
      $('mute').addEventListener('click', () => {
        const s = current
        if (!s || !s.micReady || !s.ready) return
        s.muted = !s.muted
        if (s.muted) s.speaking = false
        s.mic.stream.getAudioTracks().forEach((track) => { track.enabled = !s.muted })
        if (s.muted && !s.player.sources.size) wave.reset()
        updateRealtime(s)
      })
      $('commit').addEventListener('click', () => {
        const s = current
        if (!s || !s.ready || s.turn !== 'push' || s.muted || !s.hasInput) return
        if (send(s, { type: 'commit' }) && send(s, { type: 'respond' })) {
          s.hasInput = false
          s.responding = true
          updateRealtime(s)
        }
      })
      let composing = false
      $('message').addEventListener('compositionstart', () => { composing = true })
      $('message').addEventListener('compositionend', () => { composing = false })
      $('message').addEventListener('keydown', (event) => {
        if (event.key !== 'Enter') return
        if (composing || event.isComposing || event.keyCode === 229) { event.preventDefault(); return }
        event.preventDefault()
        sendText()
      })
      $('text-form').addEventListener('submit', (event) => {
        event.preventDefault()
        if (!composing && !event.isComposing) sendText()
      })
    }
    window.addEventListener('pagehide', () => {
      ++revision
      if (current) end(current, '已停止')
      if (page === 'tts') releaseAudio()
      for (const id of Object.values(FIELDS)) $(id).value = ''
      layout.removeEventListener('change', syncDetails)
      wave.suspend()
    })
    window.addEventListener('pageshow', () => {
      showConnectionSettings()
      syncDetails()
      layout.addEventListener('change', syncDetails)
      wave.attach()
    })
  }

  function audioContext() {
    const Constructor = window.AudioContext || window.webkitAudioContext
    if (!Constructor) throw new Error('此浏览器不支持 Web Audio，请使用新版浏览器')
    return new Constructor()
  }
  function closeContext(ctx) {
    if (!ctx) return
    ctx.onstatechange = null
    try { Promise.resolve(ctx.close()).catch(() => {}) } catch (_) {}
  }

  // MicRecorder.start creates its context AFTER permission, losing iOS activation.
  // Keep its PCM conversion and stop machinery, but own the gesture-time context
  // and check a generation before retaining any late stream or creating nodes.
  class GestureMic extends MicRecorder {
    async start(sampleRate = 16000) {
      const generation = this.generation = (this.generation || 0) + 1
      let stream
      try {
        const ctx = this.ctx = audioContext()
        const resumed = Promise.resolve(ctx.resume())
        // Observe rejection now, even while the permission dialog remains open.
        resumed.catch(() => {})
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) throw new Error('请在 localhost 或安全浏览器环境中使用麦克风')
        const permission = navigator.mediaDevices.getUserMedia({
          audio: { channelCount: 1, echoCancellation: true, noiseSuppression: true, autoGainControl: true },
        })
        const acquired = permission.then((value) => {
          if (this.generation !== generation) value.getTracks().forEach((track) => track.stop())
          else this.stream = value // stop() must release tracks even while resume is pending.
          return value
        })
        ;[stream] = await Promise.all([acquired, resumed])
        if (this.generation !== generation) { stream.getTracks().forEach((track) => track.stop()); return }
        if (ctx.state !== 'running') throw new Error('录音音频环境未解锁，请重新点击开始')
        this.inputRate = ctx.sampleRate
        this.targetRate = sampleRate
        this.source = ctx.createMediaStreamSource(stream)
        this.processor = ctx.createScriptProcessor(4096, 1, 1)
        this.processor.onaudioprocess = (event) => {
          if (!this.running || this.generation !== generation) return
          try {
            this.onChunk(floatTo16BitPCM(resample(event.inputBuffer.getChannelData(0), this.inputRate, this.targetRate)).buffer)
          } catch (e) { if (this.onFailure) this.onFailure(e) }
        }
        this.gain = ctx.createGain()
        this.gain.gain.value = 0
        this.source.connect(this.processor)
        this.processor.connect(this.gain)
        this.gain.connect(ctx.destination)
        this.running = true
        const lost = () => {
          if (this.generation === generation && this.onFailure) this.onFailure(new Error('录音设备或音频环境已中断，请重新连接'))
        }
        stream.getTracks().forEach((track) => { track.onended = lost })
        ctx.onstatechange = () => { if (this.ctx === ctx && ctx.state !== 'running') lost() }
      } catch (e) {
        if (stream) stream.getTracks().forEach((track) => track.stop())
        this.stop()
        throw e
      }
    }
    stop() {
      this.generation = (this.generation || 0) + 1
      const ctx = this.ctx
      this.ctx = null // close() returns a promise; the legacy method does not catch it.
      try { if (this.gain) this.gain.disconnect() } catch (_) {}
      this.gain = null
      if (this.stream) this.stream.getTracks().forEach((track) => { track.onended = null })
      super.stop()
      closeContext(ctx)
    }
  }

  // PcmPlayer owns PCM scheduling; add safe unlock and actual source-ended events.
  class GesturePlayer extends PcmPlayer {
    constructor(wave, onDrain, onError) {
      super(24000)
      this.wave = wave
      this.onDrain = onDrain
      this.onError = onError
      this.generation = 0
    }
    async unlock() {
      const ctx = this.ctx = audioContext()
      this.unlocking = true
      this.analyser = ctx.createAnalyser()
      this.analyser.fftSize = 256
      this.analyser.connect(ctx.destination)
      // Both resume and a one-frame source start happen in the user gesture.
      const resumed = Promise.resolve(ctx.resume())
      resumed.catch(() => {})
      const silent = ctx.createBufferSource()
      silent.buffer = ctx.createBuffer(1, 1, ctx.sampleRate)
      silent.connect(ctx.destination)
      silent.onended = () => { try { silent.disconnect() } catch (_) {} }
      silent.start(0)
      await resumed
      if (this.ctx !== ctx) return
      this.unlocking = false
      if (ctx.state !== 'running') throw new Error('音频播放环境未解锁')
      ctx.onstatechange = () => {
        if (this.ctx === ctx && ctx.state !== 'running') this.onError(new Error('浏览器已暂停音频，请重新点击开始以恢复播放'))
      }
    }
    _ensureCtx() {
      if (!this.ctx || (!this.unlocking && this.ctx.state !== 'running')) throw new Error('音频播放未就绪，请重新点击开始')
      return this.ctx
    }
    feed(buffer) {
      super.feed(buffer)
      const source = [...this.sources].at(-1)
      if (!source) return
      source.disconnect()
      source.connect(this.analyser)
      const original = source.onended
      const generation = this.generation
      source.onended = () => {
        original()
        try { source.disconnect() } catch (_) {}
        if (generation !== this.generation) return
        if (!this.sources.size) { this.wave.stopPlayback(); this.onDrain() }
      }
      this.wave.play(this.analyser)
    }
    clear() {
      this.generation++
      super.clear()
      this.wave.stopPlayback()
    }
    destroy() {
      const ctx = this.ctx
      this.ctx = null
      super.destroy()
      try { if (this.analyser) this.analyser.disconnect() } catch (_) {}
      this.analyser = null
      closeContext(ctx)
    }
  }

  function makeWaveform(canvas) {
    const ctx = canvas.getContext('2d')
    const reduced = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false }
    let peaks = new Float32Array(80)
    let analyser = null
    let frame = null
    let quietTimer = null
    let reducedTimer = null
    let observer = null
    let attached = false
    let lastDraw = 0
    const draw = () => {
      if (!ctx) return
      const box = canvas.getBoundingClientRect()
      const width = Math.max(1, box.width)
      const height = Math.max(1, box.height)
      const dpr = Math.min(window.devicePixelRatio || 1, 3)
      if (canvas.width !== Math.round(width * dpr) || canvas.height !== Math.round(height * dpr)) {
        canvas.width = Math.round(width * dpr)
        canvas.height = Math.round(height * dpr)
      }
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
      ctx.clearRect(0, 0, width, height)
      ctx.strokeStyle = getComputedStyle(canvas).color || '#5d786a'
      ctx.lineWidth = 1.25
      ctx.lineCap = 'round'
      ctx.globalAlpha = 0.85
      ctx.beginPath()
      // Signed peak envelope of real samples, never a generated sine animation.
      for (let i = 0; i < peaks.length; i++) {
        const x = i * width / (peaks.length - 1)
        const y = height / 2 - peaks[i] * height * 0.42
        if (!i) ctx.moveTo(x, y)
        else ctx.lineTo(x, y)
      }
      ctx.stroke()
      lastDraw = Date.now()
    }
    const sample = (values, scale = 1) => {
      const count = reduced.matches ? 24 : 80
      peaks = new Float32Array(count)
      for (let i = 0; i < count; i++) {
        const begin = Math.floor(i * values.length / count)
        const end = Math.max(begin + 1, Math.floor((i + 1) * values.length / count))
        let peak = 0
        for (let j = begin; j < end && j < values.length; j++) if (Math.abs(values[j]) > Math.abs(peak)) peak = values[j]
        peaks[i] = Math.max(-1, Math.min(1, peak * scale))
      }
    }
    const cancel = () => {
      if (frame !== null) cancelAnimationFrame(frame)
      clearTimeout(quietTimer)
      clearTimeout(reducedTimer)
      frame = quietTimer = reducedTimer = null
    }
    const reset = () => { cancel(); analyser = null; peaks.fill(0); draw() }
    const tick = () => {
      frame = null
      reducedTimer = null
      if (!analyser) return
      const values = new Float32Array(analyser.fftSize)
      analyser.getFloatTimeDomainData(values)
      sample(values)
      draw()
      if (reduced.matches) reducedTimer = setTimeout(tick, 250)
      else frame = requestAnimationFrame(tick)
    }
    const resize = () => draw()
    const attach = () => {
      if (attached) return
      attached = true
      window.addEventListener('resize', resize)
      if (window.ResizeObserver) { observer = new window.ResizeObserver(resize); observer.observe(canvas) }
      if (reduced.addEventListener) reduced.addEventListener('change', resize)
      draw()
    }
    attach()
    return {
      feed(buffer) {
        if (analyser || !buffer.byteLength) return
        sample(new Int16Array(buffer), 1 / 32768)
        clearTimeout(quietTimer)
        if (!reduced.matches || Date.now() - lastDraw >= 250) {
          if (frame === null) frame = requestAnimationFrame(() => { frame = null; draw() })
        }
        quietTimer = setTimeout(() => { quietTimer = null; peaks.fill(0); draw() }, 220)
      },
      play(next) { if (analyser === next) return; cancel(); analyser = next; tick() },
      stopPlayback() { if (analyser) reset() },
      reset,
      attach,
      suspend() {
        reset()
        attached = false
        if (observer) observer.disconnect()
        observer = null
        window.removeEventListener('resize', resize)
        if (reduced.removeEventListener) reduced.removeEventListener('change', resize)
      },
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot, { once: true })
  else boot()
})()
