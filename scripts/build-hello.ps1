$Root = Split-Path -Parent $PSScriptRoot
& "$Root\scripts\build.ps1" -Source "src\hello.py" -Output "dist\Hello.tns"
