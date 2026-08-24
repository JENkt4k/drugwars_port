param(
    [string]$Output = "dist\DrugWarsGraphicalEmbedded.tns"
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Compiler = Join-Path $Root "scripts\asset_processing\compile_bmp_assets.py"
$Template = Join-Path $Root "src\drugwars_ti_nspire_cx2_graphical_v2.py"
$Generated = Join-Path $Root "build\generated\drugwars_ti_nspire_cx2_graphical_embedded.py"
$BuildScript = Join-Path $Root "scripts\build.ps1"

Write-Host ""
Write-Host "=== Drug Wars graphical embedded-asset build ==="
Write-Host ""

if (-not (Test-Path $Compiler)) {
    throw "Asset compiler not found: $Compiler"
}
if (-not (Test-Path $Template)) {
    throw "Graphical v2 template not found: $Template"
}

Write-Host "Compiling PNG assets into TI-Nspire Python source..."
python $Compiler `
    --template $Template `
    --assets (Join-Path $Root "images\assets") `
    --output $Generated

if ($LASTEXITCODE -ne 0) {
    throw "Asset compiler failed with exit code $LASTEXITCODE"
}

$GeneratedRelative = [System.IO.Path]::GetRelativePath($Root, $Generated)

Write-Host ""
Write-Host "Building generated Python through existing Luna pipeline..."
& $BuildScript `
    -Source $GeneratedRelative `
    -Output $Output

if ($LASTEXITCODE -ne 0) {
    throw "Luna build failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Embedded-art build complete."
Write-Host "No ti_image/Notes image lookup is required at runtime."
