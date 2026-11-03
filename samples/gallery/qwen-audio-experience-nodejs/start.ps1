$ErrorActionPreference = 'Stop'

function Test-NodeVersion {
    param([string]$NodePath)

    if (-not (Test-Path -LiteralPath $NodePath -PathType Leaf)) {
        return $false
    }
    try {
        $versionOutput = @(& $NodePath -p 'process.versions.node' 2>$null)
        $nodeExitCode = $LASTEXITCODE
        if ($nodeExitCode -ne 0 -or $versionOutput.Count -ne 1) {
            return $false
        }
        $version = ([string]$versionOutput[0]).Trim()
        return ($version -match '^(\d+)\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$' -and [int]$Matches[1] -ge 18)
    }
    catch {
        return $false
    }
}

function Find-PathNode {
    $commands = @(Get-Command -Name 'node.exe' -CommandType Application -All -ErrorAction SilentlyContinue)
    foreach ($command in $commands) {
        if (Test-NodeVersion -NodePath $command.Source) {
            return $command.Source
        }
    }
    return $null
}

function Get-NpmPath {
    param([string]$NodePath, [string]$BootstrapPath)

    try {
        $output = @(& $NodePath $BootstrapPath '--npm-path' 2>$null)
        $npmExitCode = $LASTEXITCODE
        if ($npmExitCode -ne 0 -or $output.Count -ne 1) {
            return $null
        }
        $npmPath = ([string]$output[0]).Trim()
        if ([System.IO.Path]::IsPathRooted($npmPath) -and
            (Test-Path -LiteralPath $npmPath -PathType Leaf)) {
            return $npmPath
        }
    }
    catch {
        return $null
    }
    return $null
}

function Get-NativeArchitecture {
    # WOW64 exposes the native architecture here, even in 32-bit PowerShell.
    $architecture = $env:PROCESSOR_ARCHITEW6432
    if ([string]::IsNullOrWhiteSpace($architecture)) {
        try {
            # Prefer the OS architecture over an emulated process architecture.
            $architecture = [System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString()
        }
        catch {
            # Older Windows PowerShell/.NET versions do not provide RuntimeInformation.
            $architecture = $env:PROCESSOR_ARCHITECTURE
        }
    }
    if ([string]::IsNullOrWhiteSpace($architecture)) {
        throw 'Cannot determine the native Windows architecture. Only x64 and arm64 are supported.'
    }
    switch ($architecture.ToUpperInvariant()) {
        'AMD64' { return 'x64' }
        'X64' { return 'x64' }
        'ARM64' { return 'arm64' }
        default { throw "Unsupported native Windows architecture: $architecture. Only x64 and arm64 are supported." }
    }
}

function Install-LocalNode {
    param([string]$PackageDirectory)

    foreach ($name in @('Invoke-WebRequest', 'Get-FileHash', 'Expand-Archive')) {
        if (-not (Get-Command -Name $name -CommandType Cmdlet, Function -ErrorAction SilentlyContinue)) {
            throw "Required Windows PowerShell tool '$name' is missing. Stop without installing Node."
        }
    }

    $version = '24.22.2'
    if ($version -notmatch '^\d+\.\d+\.\d+$') {
        throw 'The Node version placeholder was not replaced when this demo was packaged.'
    }
    $architecture = Get-NativeArchitecture
    $archiveName = "node-v$version-win-$architecture.zip"
    $baseUrl = "https://nodejs.org/dist/v$version/"
    $runtimeDirectory = Join-Path $PackageDirectory '.runtime'
    $nodeDirectory = Join-Path $runtimeDirectory 'node'
    if (Test-Path -LiteralPath $runtimeDirectory) {
        $runtimeItem = Get-Item -LiteralPath $runtimeDirectory -Force
        if (-not $runtimeItem.PSIsContainer -or
            ($runtimeItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
            throw 'The demo .runtime path must be a regular directory, not a file or a link.'
        }
    }
    else {
        New-Item -ItemType Directory -Path $runtimeDirectory -ErrorAction Stop | Out-Null
    }

    $downloadDirectory = Join-Path $runtimeDirectory ('download-' + [guid]::NewGuid().ToString('N'))
    $ownsDownloadDirectory = $false
    $previousSecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol
    try {
        New-Item -ItemType Directory -Path $downloadDirectory -ErrorAction Stop | Out-Null
        $ownsDownloadDirectory = $true
        # TLS settings are process-local and restored below; certificate validation stays enabled.
        [System.Net.ServicePointManager]::SecurityProtocol = $previousSecurityProtocol -bor [System.Net.SecurityProtocolType]::Tls12
        $hashesPath = Join-Path $downloadDirectory 'SHASUMS256.txt'
        $archivePath = Join-Path $downloadDirectory $archiveName
        Write-Host "Downloading official Node.js v$version ($architecture) into this demo..."
        Invoke-WebRequest -Uri ($baseUrl + 'SHASUMS256.txt') -OutFile $hashesPath -UseBasicParsing -TimeoutSec 120 -ErrorAction Stop
        Invoke-WebRequest -Uri ($baseUrl + $archiveName) -OutFile $archivePath -UseBasicParsing -TimeoutSec 600 -ErrorAction Stop

        $expectedHashes = @(
            foreach ($line in (Get-Content -LiteralPath $hashesPath -ErrorAction Stop)) {
                if ($line -match '^(?<hash>[0-9a-fA-F]{64})[ \t]+\*?(?<name>[^\r\n]+)$') {
                    if ($Matches['name'] -ceq $archiveName) {
                        $Matches['hash']
                    }
                }
            }
        )
        if ($expectedHashes.Count -ne 1) {
            throw "SHASUMS256.txt must contain exactly one SHA256 entry for $archiveName."
        }
        $actualHash = (Get-FileHash -LiteralPath $archivePath -Algorithm SHA256 -ErrorAction Stop).Hash
        if ($actualHash -ine $expectedHashes[0]) {
            throw 'Node archive SHA256 verification failed. Nothing will be extracted or started.'
        }

        $extractDirectory = Join-Path $downloadDirectory 'extracted'
        Expand-Archive -LiteralPath $archivePath -DestinationPath $extractDirectory -ErrorAction Stop
        $stagedDirectory = Join-Path $extractDirectory "node-v$version-win-$architecture"
        $stagedNode = Join-Path $stagedDirectory 'node.exe'
        $stagedNpm = Join-Path $stagedDirectory 'node_modules/npm/bin/npm-cli.js'
        if (-not (Test-NodeVersion -NodePath $stagedNode) -or
            -not (Test-Path -LiteralPath $stagedNpm -PathType Leaf)) {
            throw 'The verified Node distribution cannot run or is missing npm. The demo will not start.'
        }

        $existingNode = Get-Item -LiteralPath $nodeDirectory -Force -ErrorAction SilentlyContinue
        if ($null -ne $existingNode) {
            $backupDirectory = Join-Path $runtimeDirectory ('node.backup-' + [guid]::NewGuid().ToString('N'))
            Move-Item -LiteralPath $nodeDirectory -Destination $backupDirectory -ErrorAction Stop
            Write-Host "Previous local runtime preserved at: $backupDirectory"
        }
        Move-Item -LiteralPath $stagedDirectory -Destination $nodeDirectory -ErrorAction Stop
        $installedNode = Join-Path $nodeDirectory 'node.exe'
        if (-not (Test-NodeVersion -NodePath $installedNode)) {
            throw 'The installed local Node cannot run. The demo will not start.'
        }
        return $installedNode
    }
    finally {
        [System.Net.ServicePointManager]::SecurityProtocol = $previousSecurityProtocol
        # Never remove previous runtimes or any download directory owned by another run.
        if ($ownsDownloadDirectory) {
            try {
                Remove-Item -LiteralPath $downloadDirectory -Recurse -Force -ErrorAction Stop
            }
            catch {
                Write-Warning "Could not clean this run's temporary download directory: $downloadDirectory"
            }
        }
    }
}

$exitCode = 1
$originalPath = $env:PATH
$locationPushed = $false
try {
    $packageDirectory = $PSScriptRoot
    if ([string]::IsNullOrWhiteSpace($packageDirectory)) {
        $packageDirectory = $env:QWEN_AUDIO_DIR
    }
    if ([string]::IsNullOrWhiteSpace($packageDirectory)) {
        throw 'Cannot locate the demo directory. Run start.bat or the adjacent start.ps1.'
    }
    $packageDirectory = (Resolve-Path -LiteralPath $packageDirectory -ErrorAction Stop).ProviderPath
    $bootstrapPath = Join-Path $packageDirectory 'bootstrap.mjs'
    if (-not (Test-Path -LiteralPath $bootstrapPath -PathType Leaf)) {
        throw "Missing demo bootstrap: $bootstrapPath"
    }
    Push-Location -LiteralPath $packageDirectory -ErrorAction Stop
    $locationPushed = $true

    $nodePath = Find-PathNode
    if (-not $nodePath) {
        $localNode = Join-Path $packageDirectory '.runtime/node/node.exe'
        if (Test-NodeVersion -NodePath $localNode) {
            $nodePath = $localNode
        }
        else {
            $nodePath = Install-LocalNode -PackageDirectory $packageDirectory
        }
    }

    & $nodePath $bootstrapPath '--check'
    $checkExitCode = $LASTEXITCODE
    if ($checkExitCode -eq 1) {
        # Complete dependencies require no npm lookup or Node download.
        if (-not (Get-NpmPath -NodePath $nodePath -BootstrapPath $bootstrapPath)) {
            $localNode = Join-Path $packageDirectory '.runtime/node/node.exe'
            if ((Test-NodeVersion -NodePath $localNode) -and
                (Get-NpmPath -NodePath $localNode -BootstrapPath $bootstrapPath)) {
                $nodePath = $localNode
            }
            else {
                $nodePath = Install-LocalNode -PackageDirectory $packageDirectory
                if (-not (Get-NpmPath -NodePath $nodePath -BootstrapPath $bootstrapPath)) {
                    throw 'The local Node distribution has no usable npm CLI. The demo will not start.'
                }
            }
        }
    }
    elseif ($checkExitCode -ne 0) {
        throw "Dependency check failed with exit code $checkExitCode. The demo will not start."
    }

    # Only this PowerShell process and its children receive the selected Node directory.
    $env:PATH = (Split-Path -Parent $nodePath) + [System.IO.Path]::PathSeparator + $originalPath
    & $nodePath $bootstrapPath
    $exitCode = $LASTEXITCODE
}
catch {
    [Console]::Error.WriteLine('Demo startup failed: ' + $_.Exception.Message)
    $exitCode = 1
}
finally {
    $env:PATH = $originalPath
    if ($locationPushed) {
        Pop-Location
    }
}
exit $exitCode
