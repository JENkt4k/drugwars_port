#!/usr/bin/env python3
"""Build a minimal TI-Nspire Python test containing only the skyline image.

This is intentionally independent of the Drug Wars game.  It answers one
question: can the CX II start a small Python program and render one embedded
image represented as compact run-length data?

Encoding format per run (8 hex chars):
    yy xx ww cc
where yy=row, xx=start x, ww=run width, cc=palette index.
The image is stored at quarter resolution and rendered as 4x4 blocks.
"""

from pathlib import Path
import argparse

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is required: python -m pip install pillow")
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[2]


def resize_crop(img, target):
    tw, th = target
    scale = max(tw / img.width, th / img.height)
    nw = max(1, round(img.width * scale))
    nh = max(1, round(img.height * scale))
    img = img.resize((nw, nh), Image.Resampling.NEAREST)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))


def encode(path, display_size=(316, 60), render_scale=4, colors=8):
    sw = max(1, display_size[0] // render_scale)
    sh = max(1, display_size[1] // render_scale)

    img = Image.open(path).convert("RGB")
    img = resize_crop(img, (sw, sh))
    q = img.quantize(
        colors=colors,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    )

    palette_raw = q.getpalette()
    px = q.load()

    used = set()
    for y in range(sh):
        for x in range(sw):
            used.add(px[x, y])
    used = sorted(used)
    remap = {old: i for i, old in enumerate(used)}
    palette = [tuple(palette_raw[i * 3:i * 3 + 3]) for i in used]

    chunks = []
    runs = 0
    for y in range(sh):
        x = 0
        while x < sw:
            old = px[x, y]
            x2 = x + 1
            while x2 < sw and px[x2, y] == old and (x2 - x) < 255:
                x2 += 1
            width = x2 - x
            chunks.append(f"{y:02x}{x:02x}{width:02x}{remap[old]:02x}")
            runs += 1
            x = x2

    return sw, sh, render_scale, palette, "".join(chunks), runs


def make_source(sw, sh, scale, palette, data):
    return f'''# GENERATED minimal TI-Nspire skyline rendering test\nfrom ti_draw import *\nfrom ti_system import *\n\nW=318\nH=212\nSCALE={scale}\nPALETTE={repr(tuple(palette))}\nDATA={data!r}\n\ndef draw_skyline(ox, oy):\n    i=0\n    n=len(DATA)\n    while i<n:\n        y=int(DATA[i:i+2],16)\n        x=int(DATA[i+2:i+4],16)\n        w=int(DATA[i+4:i+6],16)\n        p=int(DATA[i+6:i+8],16)\n        c=PALETTE[p]\n        set_color(c[0],c[1],c[2])\n        fill_rect(ox+x*SCALE,oy+y*SCALE,w*SCALE,SCALE)\n        i+=8\n\ndef main():\n    use_buffer()\n    set_color(0,0,0)\n    fill_rect(0,0,W,H)\n    set_color(235,235,235)\n    draw_text(6,18,\"ONE IMAGE TEST\")\n    draw_skyline(1,28)\n    set_color(80,255,90)\n    draw_text(6,112,\"SKYLINE RENDERED\")\n    set_color(180,180,180)\n    draw_text(6,138,\"ENTER/ESC TO EXIT\")\n    paint_buffer()\n    while True:\n        k=get_key(1)\n        if k==\"enter\" or k==\"esc\":\n            break\n\nmain()\n'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default=str(ROOT / "images" / "assets" / "header_skyline.png"),
    )
    parser.add_argument(
        "--output",
        default=str(ROOT / "build" / "generated" / "single_skyline_test.py"),
    )
    args = parser.parse_args()

    src = Path(args.input)
    out = Path(args.output)
    if not src.exists():
        raise FileNotFoundError(src)

    sw, sh, scale, palette, data, runs = encode(src)
    source = make_source(sw, sh, scale, palette, data)
    compile(source, str(out), "exec")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(source, encoding="utf-8")

    print(f"Encoded source: {src}")
    print(f"Stored size: {sw}x{sh}, render scale: {scale}x")
    print(f"Palette colors: {len(palette)}")
    print(f"RLE runs: {runs}")
    print(f"Generated Python: {out}")
    print(f"Generated size: {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
