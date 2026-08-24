$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Dist = Join-Path $Root "dist"

if (!(Test-Path $Dist)) {
    New-Item -ItemType Directory -Path $Dist | Out-Null
}

Get-ChildItem $Dist -File | Where-Object { $_.Name -ne ".gitkeep" } | Remove-Item -Force
Write-Host "Cleaned $Dist"
