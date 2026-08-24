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

# Windows PowerShell 5.1 / older .NET Framework does not provide
# System.IO.Path.GetRelativePath().  The generated file is always beneath
# the repository root, so compute the repository-relative path directly.
$RootFull = [System.IO.Path]::GetFullPath($Root).TrimEnd([char[]]"\/")
$GeneratedFull = [System.IO.Path]::GetFullPath($Generated)
$RootPrefix = $RootFull + [System.IO.Path]::DirectorySeparatorChar

if (-not $GeneratedFull.StartsWith($RootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Generated source is outside repository root: $GeneratedFull"
}

$GeneratedRelative = $GeneratedFull.Substring($RootPrefix.Length)

Write-Host ""
Write-Host "Generated source:"
Write-Host "  $GeneratedRelative"
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
