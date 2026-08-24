param(
    [string]$Output = "dist\SingleSkylineTest.tns"
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Compiler = Join-Path $Root "scripts\asset_processing\compile_single_asset_test.py"
$Generated = Join-Path $Root "build\generated\single_skyline_test.py"
$BuildScript = Join-Path $Root "scripts\build.ps1"

Write-Host ""
Write-Host "=== TI-Nspire single skyline test ==="
Write-Host ""

python $Compiler --output $Generated
if ($LASTEXITCODE -ne 0) {
    throw "Single-image compiler failed with exit code $LASTEXITCODE"
}

$rootFull = [System.IO.Path]::GetFullPath($Root).TrimEnd('\')
$generatedFull = [System.IO.Path]::GetFullPath($Generated)
$prefix = $rootFull + "\"
if (-not $generatedFull.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Generated source is outside repository root: $generatedFull"
}
$GeneratedRelative = $generatedFull.Substring($prefix.Length)

Write-Host ""
Write-Host "Building minimal test through existing Luna pipeline..."
Write-Host "  Source: $GeneratedRelative"
Write-Host "  Output: $Output"

& $BuildScript -Source $GeneratedRelative -Output $Output
if ($LASTEXITCODE -ne 0) {
    throw "Luna build failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Single-image test build complete."
Write-Host "Upload dist\SingleSkylineTest.tns and open it on the calculator."
