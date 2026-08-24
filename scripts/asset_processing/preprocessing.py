# scripts/prepare_assets.py

from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
print(f"Root: {ROOT}")
SRC = ROOT / "images" / "assets"
OUT = ROOT / "build" / "assets"

OUT.mkdir(parents=True, exist_ok=True)

ASSETS = {
    "header_skyline.png": ("header_skyline.bmp", (318, 60)),
    "police_car.png":     ("police_car.bmp",     (120, 90)),
    "mugger.png":         ("mugger.bmp",         (100, 90)),
    "dead_body.png":      ("dead_body.bmp",      (110, 75)),
    "trenchcoat.png":     ("trenchcoat.bmp",     (80, 100)),
    "doctor.png":         ("doctor.bmp",         (90, 100)),
    "gun.png":            ("gun.bmp",            (100, 50)),
    "gun_snub.png":       ("gun_snub.bmp",       (100, 50)),
    "gun_44.png":         ("gun_44.bmp",         (100, 50)),
    "subwaybg.png":       ("subwaybg.bmp",       (150, 90)),
}

def resize_crop(img, target_size):
    tw, th = target_size
    w, h = img.size

    scale = max(tw / w, th / h)

    nw = round(w * scale)
    nh = round(h * scale)

    img = img.resize((nw, nh), Image.Resampling.LANCZOS)

    left = (nw - tw) // 2
    top = (nh - th) // 2

    return img.crop((left, top, left + tw, top + th))


for src_name, (dst_name, size) in ASSETS.items():
    src = SRC / src_name
    dst = OUT / dst_name

    if not src.exists():
        print("Missing:", src)
        continue

    img = Image.open(src).convert("RGB")
    img = resize_crop(img, size)

    img.save(dst, format="BMP")

    print(
        f"{src_name:20} -> {dst_name:20} "
        f"{size[0]}x{size[1]}"
    )