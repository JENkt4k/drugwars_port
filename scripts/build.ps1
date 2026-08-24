param(
    [string[]]$Source = @("src\drugwars.py"),
    [string]$Output = "dist\DrugWars.tns"
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$WindowsLuna = Join-Path $Root "tools\luna.exe"
$WslLuna = Join-Path $Root "tools\luna-linux"

function Full-ProjectPath([string]$Path) {
    if ([System.IO.Path]::IsPathRooted($Path)) {
        return [System.IO.Path]::GetFullPath($Path)
    }
    return [System.IO.Path]::GetFullPath((Join-Path $Root $Path))
}

function To-WslPath([string]$Path) {
    $resolved = [System.IO.Path]::GetFullPath($Path)
    $drive = $resolved.Substring(0,1).ToLower()
    $rest = $resolved.Substring(2).Replace("\","/")
    return "/mnt/$drive$rest"
}

$SourcePaths = @()
foreach ($s in $Source) {
    $p = Full-ProjectPath $s
    if (!(Test-Path $p)) {
        throw "Source file not found: $p"
    }
    $SourcePaths += $p
}

$OutputPath = Full-ProjectPath $Output
$OutputDir = Split-Path -Parent $OutputPath
if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

Write-Host ""
Write-Host "=== TI-Nspire TNS Build ==="
Write-Host "Source:"
foreach ($p in $SourcePaths) {
    Write-Host "  $p"
}
Write-Host "Output:"
Write-Host "  $OutputPath"
Write-Host ""

if (Test-Path $WindowsLuna) {
    Write-Host "Using Windows Luna:"
    Write-Host "  $WindowsLuna"
    & $WindowsLuna @SourcePaths $OutputPath
}
elseif (Test-Path $WslLuna) {
    if (-not (Get-Command wsl.exe -ErrorAction SilentlyContinue)) {
        throw "tools\luna-linux exists, but wsl.exe is unavailable."
    }

    $LunaWslPath = To-WslPath $WslLuna
    $SourceWsl = @($SourcePaths | ForEach-Object { To-WslPath $_ })
    $OutputWsl = To-WslPath $OutputPath

    $quotedArgs = @()
    $quotedArgs += "'$LunaWslPath'"
    foreach ($p in $SourceWsl) { $quotedArgs += "'$p'" }
    $quotedArgs += "'$OutputWsl'"
    $cmd = $quotedArgs -join " "

    Write-Host "Using Luna through WSL:"
    Write-Host "  $WslLuna"
    wsl bash -lc $cmd
}
else {
    Write-Host "Luna is not installed." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Option A: place a Windows luna.exe here:"
    Write-Host "  $WindowsLuna"
    Write-Host ""
    Write-Host "Option B: build Luna automatically in WSL:"
    Write-Host "  .\scripts\setup-luna-wsl.ps1"
    exit 2
}

if ($LASTEXITCODE -ne 0) {
    throw "Luna failed with exit code $LASTEXITCODE"
}

if (!(Test-Path $OutputPath)) {
    throw "Luna returned success but the TNS file was not created."
}

$Size = (Get-Item $OutputPath).Length

Write-Host ""
Write-Host "BUILD SUCCESS"
Write-Host "  $OutputPath"
Write-Host "  $Size bytes"
Write-Host ""
Write-Host "Upload this .tns with TI-Nspire CX II Connect."
