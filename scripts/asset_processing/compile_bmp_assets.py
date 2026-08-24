#!/usr/bin/env python3
"""
Compile PNG artwork into a self-contained TI-Nspire Python source file.

Why this exists:
TI's ti_image.load_image() can only see images inserted into a Notes or
Graphs application in the TNS document. Luna's arbitrary/BMP resources are
packed into the TNS archive, but are not exposed to TI Python's ti_image API.

This compiler therefore:
  1. resizes/crops each PNG to the intended calculator size,
  2. downsamples by 2 for compact pixel art,
  3. quantizes to 8 colors,
  4. run-length encodes every row,
  5. injects the RLE data and renderer into the graphical v2 source.

The generated program uses only ti_draw fill_rect(), so no ti_image resource
lookup is required at runtime.
"""

from pathlib import Path
import argparse

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is required.")
    print("Install with:  python -m pip install pillow")
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[2]

ASSETS = {
    "header_skyline": ("header_skyline.png", (318, 60)),
    "police_car":     ("police_car.png",     (120, 90)),
    "mugger":         ("mugger.png",         (100, 90)),
    "dead_body":      ("dead_body.png",      (110, 75)),
    "trenchcoat":     ("trenchcoat.png",     (80, 100)),
    "doctor":         ("doctor.png",         (90, 100)),
    "gun":            ("gun.png",            (100, 50)),
    "gun_snub":       ("gun_snub.png",       (100, 50)),
    "gun_44":         ("gun_44.png",         (100, 50)),
    "subwaybg":       ("subwaybg.png",       (150, 90)),
}


def resize_crop(img, target):
    tw, th = target
    scale = max(tw / img.width, th / img.height)
    nw = max(1, round(img.width * scale))
    nh = max(1, round(img.height * scale))
    img = img.resize((nw, nh), Image.Resampling.NEAREST)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))


def encode_asset(path, target, colors=8, render_scale=2):
    # Store at half resolution, then render each encoded pixel as a 2x2 block.
    sw = max(1, target[0] // render_scale)
    sh = max(1, target[1] // render_scale)

    img = Image.open(path).convert("RGB")
    img = resize_crop(img, (sw, sh))
    q = img.quantize(
        colors=colors,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    )

    raw_palette = q.getpalette()
    used = sorted(set(q.getdata()))
    remap = {old: i for i, old in enumerate(used)}
    palette = tuple(
        tuple(raw_palette[i * 3:i * 3 + 3])
        for i in used
    )

    px = q.load()
    rows = []
    run_count = 0

    for y in range(sh):
        runs = []
        x = 0
        while x < sw:
            old = px[x, y]
            x2 = x + 1
            while x2 < sw and px[x2, y] == old:
                x2 += 1
            runs.append((x, x2 - x, remap[old]))
            run_count += 1
            x = x2
        rows.append(tuple(runs))

    return render_scale, palette, tuple(rows), run_count


def make_asset_block(asset_dir):
    encoded = {}
    total_runs = 0

    for key, (filename, target) in ASSETS.items():
        path = asset_dir / filename
        if not path.exists():
            raise FileNotFoundError("Required asset missing: " + str(path))

        scale, palette, rows, runs = encode_asset(path, target)
        encoded[key] = (scale, palette, rows)
        total_runs += runs
        print(
            f"{filename:22} -> {target[0]:3}x{target[1]:3} "
            f"({runs:5} RLE runs)"
        )

    lines = [
        "# ------------------------------------------------------------",
        "# GENERATED EMBEDDED PIXEL ART",
        "# Do not edit this data by hand; regenerate with",
        "# scripts/asset_processing/compile_bmp_assets.py",
        "# ------------------------------------------------------------",
        "ASSET_DATA = {",
    ]

    for key, value in encoded.items():
        lines.append(repr(key) + ":" + repr(value) + ",")

    lines.extend([
        "}",
        "",
        "def load_assets():",
        "    # Compatibility with graphical v2 startup.",
        "    return",
        "",
        "def show_asset(name, x, y):",
        "    spec = ASSET_DATA.get(name)",
        "    if spec is None:",
        "        return False",
        "    scale, palette, rows = spec",
        "    try:",
        "        for ry in range(len(rows)):",
        "            row = rows[ry]",
        "            for run in row:",
        "                rx, rw, pi = run",
        "                c = palette[pi]",
        "                set_color(c[0], c[1], c[2])",
        "                fill_rect(x + rx * scale, y + ry * scale,",
        "                          rw * scale, scale)",
        "        return True",
        "    except:",
        "        return False",
        "",
    ])

    print("Total encoded horizontal runs:", total_runs)
    return "\n".join(lines)


def patch_template(template_text, asset_block):
    template_text = template_text.replace("from ti_image import *\n", "")

    begin = template_text.find("# Embedded image resources.")
    end_marker = "# ----------------------------\n# Game constants"
    end = template_text.find(end_marker, begin)

    if begin < 0 or end < 0:
        raise RuntimeError(
            "Could not locate the graphical-v2 asset-loader block. "
            "The template format may have changed."
        )

    patched = template_text[:begin] + asset_block + "\n" + template_text[end:]
    patched = patched.replace(
        "Graphical Edition",
        "Graphical Edition v3 - Embedded Assets",
        1,
    )
    return patched


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--template",
        default=str(ROOT / "src" / "drugwars_ti_nspire_cx2_graphical_v2.py"),
    )
    parser.add_argument(
        "--assets",
        default=str(ROOT / "images" / "assets"),
    )
    parser.add_argument(
        "--output",
        default=str(ROOT / "build" / "generated" /
                    "drugwars_ti_nspire_cx2_graphical_embedded.py"),
    )
    args = parser.parse_args()

    template = Path(args.template)
    asset_dir = Path(args.assets)
    output = Path(args.output)

    if not template.exists():
        raise FileNotFoundError("Template missing: " + str(template))

    block = make_asset_block(asset_dir)
    source = patch_template(template.read_text(encoding="utf-8"), block)

    compile(source, str(output), "exec")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(source, encoding="utf-8")

    print("")
    print("Generated:", output)
    print("Size:", output.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
