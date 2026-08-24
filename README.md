# TI-Nspire CX II VS Code + Luna Starter

A Windows-first starter project for:

**VS Code `.py` -> Luna -> `.tns` -> TI-Nspire CX II Connect -> calculator**

## Requirements

- TI-Nspire CX II / CX II CAS
- Calculator OS **5.2 or later** for Luna Python conversion
- VS Code
- PowerShell
- Either:
  - a Windows `luna.exe` placed in `tools\`, or
  - WSL, which can build Luna automatically with the included setup script
- TI-Nspire CX II Connect in a supported browser

Luna:
https://github.com/ndless-nspire/Luna

TI-Nspire CX II Connect:
https://education.ti.com/en/products/computer-software/ti-nspire-cx-ii-connect

TI Python resources:
https://education.ti.com/en/activities/ti-codes/python/ti-nspire-cx-ii/python-modules

## Project layout

```text
ti-nspire-vscode-luna-starter/
├─ .vscode/
│  └─ tasks.json
├─ src/
│  ├─ hello.py
│  ├─ graphics_test.py
│  └─ drugwars.py
├─ scripts/
│  ├─ build.ps1
│  ├─ build-hello.ps1
│  ├─ build-graphics.ps1
│  ├─ clean.ps1
│  └─ setup-luna-wsl.ps1
├─ tools/
│  └─ README.md
└─ dist/
```

## Fastest setup on Windows with WSL

Open the extracted folder in VS Code, then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-luna-wsl.ps1
```

That script:

1. installs `build-essential`, `zlib1g-dev`, and `git` in WSL;
2. clones/updates Luna;
3. builds it with `make`;
4. copies the binary to `tools\luna-linux`.

It may ask for your Linux sudo password.

## Smoke test 1: plain Python

```powershell
.\scripts\build-hello.ps1
```

Expected:

```text
dist\Hello.tns
```

Transfer `Hello.tns` with TI-Nspire CX II Connect.

## Smoke test 2: TI graphics

```powershell
.\scripts\build-graphics.ps1
```

Expected:

```text
dist\GraphicsTest.tns
```

Transfer and run it on the calculator.

## Build Drug Wars starter

```powershell
.\scripts\build.ps1
```

Expected:

```text
dist\DrugWars.tns
```

## VS Code

Press:

```text
Ctrl+Shift+B
```

The default build task is **Build Drug Wars TNS**.

Other tasks are available from:

```text
Terminal -> Run Task...
```

## If you already have a Windows Luna executable

Put it at:

```text
tools\luna.exe
```

The build script prefers that over WSL automatically.

## Multiple Python files

Luna supports:

```text
luna InFile1.py [InFile2.py ...] OUTFILE.tns
```

Example:

```powershell
.\scripts\build.ps1 `
  -Source @("src\main.py", "src\ui.py", "src\game.py") `
  -Output "dist\MyGame.tns"
```

The first Python file is the one shown when the TNS opens.

## Normal development loop

```text
edit src\*.py
     |
Ctrl+Shift+B
     |
Luna
     |
dist\*.tns
     |
TI-Nspire CX II Connect
     |
calculator
```

## Important limitation

VS Code is only your source editor. TI-Nspire Python is a TI/MicroPython environment, not desktop CPython. Do not assume desktop packages such as pygame or numpy exist on the calculator.

Start with `hello.py`, then `graphics_test.py`, then the game.
