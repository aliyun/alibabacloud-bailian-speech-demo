import { execFileSync, spawn } from 'node:child_process'
import { existsSync, realpathSync, readFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import { constants } from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const directory = path.dirname(fileURLToPath(import.meta.url))
const require = createRequire(import.meta.url)
const names = ['dashscope-sdk-nodejs', 'ws', 'dotenv']

function checkDependencies() {
  try {
    for (const name of names) {
      const manifest = JSON.parse(readFileSync(path.join(directory, 'node_modules', name, 'package.json'), 'utf8'))
      if (manifest.name !== name) return false
    }
    // Check the side-effect entry without executing it or reading credentials.
    execFileSync(process.execPath, ['--check', require.resolve('dotenv/config')], { cwd: directory, stdio: 'ignore' })
    // A fresh process avoids caching failed imports before npm repairs a package.
    execFileSync(process.execPath, ['--input-type=module', '-e', `
      import { SpeechSynthesizer, RecognitionClient, RealtimeClient, TranscriptionClient } from 'dashscope-sdk-nodejs';
      import WebSocket from 'ws';
      import dotenv from 'dotenv';
      if (![SpeechSynthesizer, RecognitionClient, RealtimeClient, TranscriptionClient, WebSocket, dotenv.config].every(value => typeof value === 'function')) process.exit(1);
    `], { cwd: directory, stdio: 'ignore' })
    return true
  } catch {
    return false
  }
}

function findNpm() {
  const nodeDirectory = path.dirname(realpathSync(process.execPath))
  const candidates = [
    path.join(nodeDirectory, 'node_modules/npm/bin/npm-cli.js'),
    path.join(nodeDirectory, '../lib/node_modules/npm/bin/npm-cli.js'),
  ]
  for (const entry of (process.env.PATH ?? '').split(path.delimiter).filter(Boolean)) {
    candidates.push(path.join(entry, 'node_modules/npm/bin/npm-cli.js'))
    try {
      const resolved = realpathSync(path.join(entry, process.platform === 'win32' ? 'npm.cmd' : 'npm'))
      if (path.basename(resolved) === 'npm-cli.js') candidates.push(resolved)
    } catch {}
  }
  for (const candidate of candidates) {
    if (!existsSync(candidate)) continue
    try {
      execFileSync(process.execPath, [candidate, '--version'], { cwd: directory, stdio: 'ignore' })
      return realpathSync(candidate)
    } catch {}
  }
  return undefined
}

async function installDependencies(npm) {
  const child = spawn(process.execPath, [npm, 'ci', '--omit=dev', '--ignore-scripts', '--no-audit', '--no-fund'], {
    cwd: directory,
    stdio: 'inherit',
    env: { ...process.env, PATH: `${path.dirname(process.execPath)}${path.delimiter}${process.env.PATH ?? ''}` },
  })
  let interrupted
  const stop = (signal) => {
    interrupted = signal
    child.kill(signal)
  }
  const interrupt = () => stop('SIGINT')
  const terminate = () => stop('SIGTERM')
  process.on('SIGINT', interrupt)
  process.on('SIGTERM', terminate)
  try {
    await new Promise((resolve, reject) => {
      child.once('error', reject)
      child.once('exit', (code, signal) => {
        if (interrupted || signal) {
          process.exitCode = 128 + constants.signals[interrupted || signal]
          reject(new Error('依赖安装已停止，体验服务未启动。'))
        } else if (code !== 0) {
          reject(new Error(`npm 安装失败（退出码 ${code}），体验服务未启动。`))
        } else {
          resolve()
        }
      })
    })
  } finally {
    process.off('SIGINT', interrupt)
    process.off('SIGTERM', terminate)
  }
}

if (process.argv[2] === '--check') {
  process.exit(checkDependencies() ? 0 : 1)
}
if (process.argv[2] === '--npm-path') {
  const npm = findNpm()
  if (!npm) process.exit(1)
  console.log(npm)
  process.exit(0)
}

try {
  if (!checkDependencies()) {
    const manifest = JSON.parse(readFileSync(path.join(directory, 'package.json'), 'utf8'))
    const sdk = manifest.dependencies['dashscope-sdk-nodejs']
    if (typeof sdk !== 'string' || !sdk.startsWith('file:./sdk/') || !existsSync(path.resolve(directory, sdk.slice(5)))) {
      throw new Error('缺少示例目录中的 SDK tgz（sdk/），请从仓库重新获取完整的示例目录。')
    }
    if (!existsSync(path.join(directory, 'package-lock.json'))) {
      throw new Error('缺少 package-lock.json，请从仓库重新获取完整的示例目录。')
    }
    const npm = findNpm()
    if (!npm) throw new Error('缺少可用 npm，请通过 start.sh 或 start.bat 启动以补齐本地运行时。')
    console.log('运行依赖缺失或损坏，正在根据锁文件恢复 SDK、ws 和 dotenv...')
    await installDependencies(npm)
    if (!checkDependencies()) throw new Error('安装后运行依赖仍不可加载，体验服务未启动。')
  }
  process.env.PORT ??= '5173'
  await import('./server.mjs')
} catch (error) {
  console.error(`体验平台启动失败：${error.message}`)
  process.exitCode ||= 1
}
