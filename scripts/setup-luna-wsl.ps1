param(
    [switch]$SkipAptUpdate
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Tools = Join-Path $Root "tools"
$LunaLinux = Join-Path $Tools "luna-linux"

if (-not (Get-Command wsl.exe -ErrorAction SilentlyContinue)) {
    throw "WSL is not installed or wsl.exe is not on PATH."
}

function To-WslPath([string]$Path) {
    $resolved = [System.IO.Path]::GetFullPath($Path)
    $drive = $resolved.Substring(0,1).ToLower()
    $rest = $resolved.Substring(2).Replace("\","/")
    return "/mnt/$drive$rest"
}

$ToolsWsl = To-WslPath $Tools
$RepoWsl = "$ToolsWsl/Luna"
$OutWsl = "$ToolsWsl/luna-linux"

Write-Host "=== Luna WSL setup ==="
Write-Host "Repository: $RepoWsl"
Write-Host ""

if (-not $SkipAptUpdate) {
    wsl bash -lc "sudo apt-get update"
    if ($LASTEXITCODE -ne 0) { throw "apt-get update failed." }
}

wsl bash -lc "sudo apt-get install -y build-essential zlib1g-dev git"
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed." }

wsl bash -lc "if [ ! -d '$RepoWsl/.git' ]; then git clone https://github.com/ndless-nspire/Luna.git '$RepoWsl'; else git -C '$RepoWsl' pull --ff-only; fi"
if ($LASTEXITCODE -ne 0) { throw "Cloning/updating Luna failed." }

wsl bash -lc "make -C '$RepoWsl' clean && make -C '$RepoWsl'"
if ($LASTEXITCODE -ne 0) { throw "Luna build failed." }

wsl bash -lc "cp '$RepoWsl/luna' '$OutWsl' && chmod +x '$OutWsl'"
if ($LASTEXITCODE -ne 0) { throw "Could not copy Luna binary." }

if (!(Test-Path $LunaLinux)) {
    throw "Expected Luna binary was not created at $LunaLinux"
}

Write-Host ""
Write-Host "Luna built successfully:"
Write-Host "  $LunaLinux"
Write-Host ""
Write-Host "Next:"
Write-Host "  Ctrl+Shift+B in VS Code"
Write-Host "or:"
Write-Host "  .\scripts\build.ps1"
