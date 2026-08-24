param(
    [string]$Source = "src\drugwars_ti_nspire_cx2_graphical_v1.py",
    [string]$Output = "dist\DrugWarsGraphical.tns",
    [switch]$SkipAssetPrep
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$WslLuna = Join-Path $Root "tools\luna-linux"
$AssetSourceDir = Join-Path $Root "images\assets"
$AssetBuildDir = Join-Path $Root "build\assets"

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

function Resize-Crop-ToBmp {
    param(
        [Parameter(Mandatory=$true)][string]$InputPath,
        [Parameter(Mandatory=$true)][string]$OutputPath,
        [Parameter(Mandatory=$true)][int]$TargetWidth,
        [Parameter(Mandatory=$true)][int]$TargetHeight
    )

    Add-Type -AssemblyName System.Drawing

    $src = [System.Drawing.Image]::FromFile($InputPath)
    try {
        $scaleX = $TargetWidth / [double]$src.Width
        $scaleY = $TargetHeight / [double]$src.Height
        $scale = [Math]::Max($scaleX, $scaleY)

        $scaledWidth = [int][Math]::Ceiling($src.Width * $scale)
        $scaledHeight = [int][Math]::Ceiling($src.Height * $scale)

        $x = [int][Math]::Floor(($TargetWidth - $scaledWidth) / 2.0)
        $y = [int][Math]::Floor(($TargetHeight - $scaledHeight) / 2.0)

        $bmp = New-Object System.Drawing.Bitmap($TargetWidth, $TargetHeight)
        try {
            $gfx = [System.Drawing.Graphics]::FromImage($bmp)
            try {
                $gfx.Clear([System.Drawing.Color]::Black)
                $gfx.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
                $gfx.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
                $gfx.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality

                $destRect = New-Object System.Drawing.Rectangle($x, $y, $scaledWidth, $scaledHeight)
                $gfx.DrawImage($src, $destRect)
            }
            finally {
                $gfx.Dispose()
            }

            $bmp.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Bmp)
        }
        finally {
            $bmp.Dispose()
        }
    }
    finally {
        $src.Dispose()
    }
}

Write-Host ""
Write-Host "=== Drug Wars graphical TNS build (WSL Luna + assets) ==="
Write-Host "Repository:"
Write-Host "  $Root"
Write-Host ""

if (-not (Test-Path $WslLuna)) {
    throw @"
WSL Luna binary not found:
  $WslLuna

Run the existing setup first:
  .\scripts\setup-luna-wsl.ps1
"@
}

if (-not (Get-Command wsl.exe -ErrorAction SilentlyContinue)) {
    throw "wsl.exe is unavailable. This build script uses the existing WSL Luna setup."
}

$SourcePath = Full-ProjectPath $Source
if (-not (Test-Path $SourcePath)) {
    throw "Python source not found: $SourcePath"
}

$OutputPath = Full-ProjectPath $Output
$OutputDir = Split-Path -Parent $OutputPath
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

if (-not (Test-Path $AssetBuildDir)) {
    New-Item -ItemType Directory -Path $AssetBuildDir -Force | Out-Null
}

$Assets = @(
    @{ Source="header_skyline.png"; Output="header_skyline.bmp"; Width=318; Height=60  },
    @{ Source="police_car.png";     Output="police_car.bmp";     Width=120; Height=90  },
    @{ Source="mugger.png";         Output="mugger.bmp";         Width=100; Height=90  },
    @{ Source="dead_body.png";      Output="dead_body.bmp";      Width=110; Height=75  },
    @{ Source="trenchcoat.png";     Output="trenchcoat.bmp";     Width=80;  Height=100 },
    @{ Source="doctor.png";         Output="doctor.bmp";         Width=90;  Height=100 },
    @{ Source="gun.png";            Output="gun.bmp";            Width=100; Height=50  },
    @{ Source="gun_snub.png";       Output="gun_snub.bmp";       Width=100; Height=50  },
    @{ Source="gun_44.png";         Output="gun_44.bmp";         Width=100; Height=50  },
    @{ Source="subwaybg.png";       Output="subwaybg.bmp";       Width=150; Height=90  }
)

$PreparedAssets = @()

if (-not $SkipAssetPrep) {
    Write-Host "Preparing calculator-sized BMP assets..."
    Write-Host ""

    foreach ($asset in $Assets) {
        $src = Join-Path $AssetSourceDir $asset.Source
        $dst = Join-Path $AssetBuildDir $asset.Output

        if (-not (Test-Path $src)) {
            throw "Required asset missing: $src"
        }

        Write-Host ("  {0,-22} -> {1,-22} {2}x{3}" -f `
            $asset.Source, $asset.Output, $asset.Width, $asset.Height)

        Resize-Crop-ToBmp `
            -InputPath $src `
            -OutputPath $dst `
            -TargetWidth $asset.Width `
            -TargetHeight $asset.Height

        $PreparedAssets += $dst
    }
}
else {
    Write-Host "Skipping asset preprocessing."
    foreach ($asset in $Assets) {
        $dst = Join-Path $AssetBuildDir $asset.Output
        if (-not (Test-Path $dst)) {
            throw "Prepared asset missing: $dst"
        }
        $PreparedAssets += $dst
    }
}

Write-Host ""
Write-Host "Prepared assets:"
foreach ($p in $PreparedAssets) {
    $size = (Get-Item $p).Length
    Write-Host ("  {0} ({1:N0} bytes)" -f $p, $size)
}

$LunaWsl = To-WslPath $WslLuna
$SourceWsl = To-WslPath $SourcePath
$OutputWsl = To-WslPath $OutputPath

$ArgsWsl = @()
$ArgsWsl += "'$LunaWsl'"
$ArgsWsl += "'$SourceWsl'"

foreach ($assetPath in $PreparedAssets) {
    $ArgsWsl += "'" + (To-WslPath $assetPath) + "'"
}

$ArgsWsl += "'$OutputWsl'"
$Command = $ArgsWsl -join " "

Write-Host ""
Write-Host "Running Luna through WSL:"
Write-Host "  $Command"
Write-Host ""

wsl bash -lc $Command

if ($LASTEXITCODE -ne 0) {
    throw "Luna failed with exit code $LASTEXITCODE"
}

if (-not (Test-Path $OutputPath)) {
    throw "Luna returned success but the TNS file was not created: $OutputPath"
}

$TnsSize = (Get-Item $OutputPath).Length

Write-Host ""
Write-Host "BUILD SUCCESS" -ForegroundColor Green
Write-Host "  $OutputPath"
Write-Host ("  {0:N0} bytes" -f $TnsSize)
Write-Host ""
Write-Host "Upload the .tns using TI-Nspire CX II Connect."
Write-Host ""
Write-Host "Luna supports packing arbitrary files including BMP resources."
Write-Host "The game code must load the embedded image resource names expected by TI Python."
