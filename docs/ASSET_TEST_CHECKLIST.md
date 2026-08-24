# Asset rendering test

## What the first hardware test proved

The first graphical-v2 build ran successfully, but the skyline did not appear. This confirms that Luna packing a BMP into the TNS archive is **not sufficient for TI Python `ti_image.load_image()`**.

TI documents that `load_image("name")` only sees images that are part of the TNS document in a **Notes or Graphs application**. Luna can pack arbitrary files/BMP resources into the TNS, but those packed resources are not automatically inserted as Notes/Graphs images. Luna issue #14 also reports BMP files added by Luna not appearing in the image tab of TI's Script Editor.

## New test path: self-contained embedded pixel art

Use:

```powershell
python -m pip install pillow
.\scripts\build-graphical-embedded-assets.ps1
```

This build does not use `ti_image.load_image()` at runtime. Instead it:

1. reads the PNG files in `images/assets/`;
2. resizes/crops each asset;
3. downsamples to half resolution;
4. quantizes each asset to 8 colors;
5. row-run-length encodes the pixels;
6. injects the encoded data into a generated Python source file;
7. renders the art using `ti_draw.fill_rect()`;
8. calls the existing working `scripts/build.ps1` Luna pipeline.

Expected output:

```text
dist\DrugWarsGraphicalEmbedded.tns
```

The generated intermediate source is:

```text
build\generated\drugwars_ti_nspire_cx2_graphical_embedded.py
```

## First hardware checks

- Title screen: skyline appears behind/around the title.
- Trenchcoat screen: trenchcoat artwork appears.
- Travel: subway artwork appears.
- Mugging event: mugger artwork appears.
- Dead-body find: dead-body artwork appears.
- Police-related event: police-car artwork appears.
- Gun offer: appropriate gun sprite appears.
- Doctor/healing event: doctor artwork appears.

Because the artwork is compiled into Python data, these checks do not depend on TI image-resource naming or Notes/Graphs insertion order.
