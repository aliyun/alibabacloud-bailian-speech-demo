#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
PACKAGE_DIR="$PWD"
NODE_BIN=''
DOWNLOAD_DIR=''

fail() {
  printf '%s\n' "体验平台启动失败：$*" >&2
  exit 1
}

node_valid() {
  local major
  [[ -x "$1" ]] || return 1
  major="$("$1" -p 'process.versions.node.split(".")[0]' 2>/dev/null)" || return 1
  [[ "$major" =~ ^[0-9]+$ ]] && [[ "$major" -ge 18 ]]
}

cleanup() {
  if [[ -n "$DOWNLOAD_DIR" && -d "$DOWNLOAD_DIR" ]]; then
    rm -rf -- "$DOWNLOAD_DIR"
  fi
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

install_node() {
  local tool platform architecture archive base hash_tool expected actual line hash name count staged backup
  for tool in curl tar uname mkdir mktemp mv rm; do
    command -v "$tool" >/dev/null 2>&1 || fail "缺少系统工具 $tool，请安装后重试；脚本不会安装系统软件。"
  done
  if command -v shasum >/dev/null 2>&1; then hash_tool=shasum
  elif command -v sha256sum >/dev/null 2>&1; then hash_tool=sha256sum
  else fail '缺少 SHA256 工具 shasum 或 sha256sum，无法验证下载。'; fi
  case "$(uname -s)" in
    Darwin) platform=darwin ;;
    Linux) platform=linux ;;
    *) fail '自动安装仅支持 macOS 和 Linux。' ;;
  esac
  case "$(uname -m)" in
    x86_64|amd64) architecture=x64 ;;
    arm64|aarch64) architecture=arm64 ;;
    *) fail '自动安装仅支持 x64 和 arm64。' ;;
  esac
  [[ ! -L .runtime ]] || fail '.runtime 不能是符号链接。'
  [[ ! -e .runtime || -d .runtime ]] || fail '.runtime 必须是目录。'
  mkdir -p -- .runtime
  DOWNLOAD_DIR="$(mktemp -d "$PACKAGE_DIR/.runtime/download.XXXXXXXX")"
  archive="node-v24.22.2-$platform-$architecture.tar.gz"
  base='https://nodejs.org/dist/v24.22.2'
  printf '%s\n' "正在下载官方 Node.js v24.22.2（$platform/$architecture），安装到当前示例目录的 .runtime/ ..."
  curl --fail --location --proto '=https' --proto-redir '=https' --connect-timeout 20 --max-time 120 --output "$DOWNLOAD_DIR/SHASUMS256.txt" "$base/SHASUMS256.txt" || fail '下载 Node.js 校验清单失败，请检查网络。'
  curl --fail --location --proto '=https' --proto-redir '=https' --connect-timeout 20 --max-time 600 --output "$DOWNLOAD_DIR/$archive" "$base/$archive" || fail '下载 Node.js 失败，请检查网络。'
  expected=''
  count=0
  while IFS= read -r line || [[ -n "$line" ]]; do
    read -r hash name <<< "$line"
    if [[ "$name" == "$archive" && "$hash" =~ ^[0-9a-fA-F]{64}$ ]]; then
      expected="$hash"
      count=$((count + 1))
    fi
  done < "$DOWNLOAD_DIR/SHASUMS256.txt"
  [[ "$count" -eq 1 ]] || fail "SHA256 清单中没有唯一的 $archive 校验值。"
  if [[ "$hash_tool" == shasum ]]; then
    actual="$(shasum -a 256 "$DOWNLOAD_DIR/$archive")"
  else
    actual="$(sha256sum "$DOWNLOAD_DIR/$archive")"
  fi
  actual="${actual%% *}"
  [[ "$actual" == "$expected" ]] || fail 'Node.js SHA256 校验失败，不会解压或启动。'
  tar -xzf "$DOWNLOAD_DIR/$archive" -C "$DOWNLOAD_DIR" || fail 'Node.js 解压失败。'
  staged="$DOWNLOAD_DIR/node-v24.22.2-$platform-$architecture"
  node_valid "$staged/bin/node" || fail '下载的 Node.js 无法运行；请检查操作系统兼容性。'
  [[ -f "$staged/lib/node_modules/npm/bin/npm-cli.js" ]] || fail '下载的 Node.js 缺少 npm。'
  if [[ -e .runtime/node || -L .runtime/node ]]; then
    backup="$(mktemp -d "$PACKAGE_DIR/.runtime/node.backup.XXXXXXXX")"
    mv -- .runtime/node "$backup/node"
    printf '%s\n' "原本地运行时已保留在 $backup/node"
  fi
  mv -- "$staged" .runtime/node
  NODE_BIN="$PACKAGE_DIR/.runtime/node/bin/node"
  cleanup
  DOWNLOAD_DIR=''
}

[[ -f bootstrap.mjs ]] || fail '缺少 bootstrap.mjs，请从仓库重新获取完整的示例目录。'
SYSTEM_NODE="$(command -v node || true)"
if [[ -n "$SYSTEM_NODE" ]] && node_valid "$SYSTEM_NODE"; then
  NODE_BIN="$SYSTEM_NODE"
elif node_valid "$PACKAGE_DIR/.runtime/node/bin/node"; then
  NODE_BIN="$PACKAGE_DIR/.runtime/node/bin/node"
else
  install_node
fi

if "$NODE_BIN" bootstrap.mjs --check; then
  :
else
  status=$?
  [[ "$status" -eq 1 ]] || fail "依赖检测异常（退出码 $status）。"
  if ! "$NODE_BIN" bootstrap.mjs --npm-path >/dev/null; then
    if node_valid "$PACKAGE_DIR/.runtime/node/bin/node" && "$PACKAGE_DIR/.runtime/node/bin/node" bootstrap.mjs --npm-path >/dev/null; then
      NODE_BIN="$PACKAGE_DIR/.runtime/node/bin/node"
    else
      install_node
    fi
  fi
fi
export PATH="$(dirname "$NODE_BIN"):${PATH:-}"
export PORT="${PORT:-5173}"
exec "$NODE_BIN" bootstrap.mjs
