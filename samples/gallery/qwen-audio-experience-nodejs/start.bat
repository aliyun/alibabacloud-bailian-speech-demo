@echo off
setlocal DisableDelayedExpansion
set "QWEN_AUDIO_DIR=%~dp0"
if not exist "%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" (
    >&2 echo Windows PowerShell is missing. The demo cannot start.
    pause
    exit /b 1
)
rem Compile only the trusted adjacent script: Restricted blocks script files, not commands; no execution policy is changed.
"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -Command "try { $ErrorActionPreference = 'Stop'; $launcher = Join-Path $env:QWEN_AUDIO_DIR 'start.ps1'; $source = [System.IO.File]::ReadAllText($launcher); & ([ScriptBlock]::Create($source)) } catch { [Console]::Error.WriteLine($_.Exception.Message); exit 1 }"
set "QWEN_AUDIO_EXIT=%ERRORLEVEL%"
if not "%QWEN_AUDIO_EXIT%"=="0" pause
exit /b %QWEN_AUDIO_EXIT%
