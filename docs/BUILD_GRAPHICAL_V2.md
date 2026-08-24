# Build graphical v2

Use the existing WSL Luna asset-build script, but point it at:

```powershell
src\drugwars_ti_nspire_cx2_graphical_v2.py
```

and output a distinct test document, for example:

```text
dist\DrugWarsGraphicalV2.tns
```

The generated TNS must contain the prepared BMP resources in the order documented in `ASSET_LOADING.md`.
