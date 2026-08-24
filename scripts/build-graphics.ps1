$Root = Split-Path -Parent $PSScriptRoot
& "$Root\scripts\build.ps1" -Source "src\graphics_test.py" -Output "dist\GraphicsTest.tns"
