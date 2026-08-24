# Luna tool location

This starter kit does **not** redistribute a Luna binary.

Luna project:
https://github.com/ndless-nspire/Luna

Two supported choices:

1. **Windows binary**
   - Put `luna.exe` in this `tools` folder.
   - `scripts/build.ps1` will use it automatically.

2. **Build Luna in WSL**
   - Run:
     `powershell -ExecutionPolicy Bypass -File .\scripts\setup-luna-wsl.ps1`
   - This builds Luna from source using `make` and `zlib1g-dev`.
   - The resulting ELF executable is copied to `tools/luna-linux`.
   - `scripts/build.ps1` will invoke it through `wsl.exe`.

Luna Python syntax:
`luna InFile1.py [InFile2.py...] OUTFILE.tns`

Per the Luna README, Python conversion requires a TI-Nspire CX II running OS 5.2 or later.
