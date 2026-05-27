"""Compression des images PNG -> JPEG (max 900px, qualite 85%)"""
import sys, os
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
from PIL import Image

IMAGES_DIR = Path(__file__).parent / "images"
MAX_SIZE = 900       # px on longest dimension
QUALITY = 85

# These are original/legacy images — on ne les touche pas
SKIP = {
    "ostrich.webp", "fish-meme.png", "flamingo-pink.png",
    "sunflowers-sun.png", "vegan-activist.png", "nutrition-chemicals.png",
    "edison-lightbulb.png",
    "tiktok_araignees.jpg", "tiktok_araignees_en.jpg",
}

converted = []
total_before = 0
total_after = 0

for png in sorted(IMAGES_DIR.glob("*.png")):
    if png.name in SKIP:
        continue

    before = png.stat().st_size
    total_before += before

    jpg = png.with_suffix(".jpg")

    try:
        img = Image.open(png).convert("RGB")
        w, h = img.size
        # Redimensionner si nécessaire
        if max(w, h) > MAX_SIZE:
            ratio = MAX_SIZE / max(w, h)
            new_size = (int(w * ratio), int(h * ratio))
            img = img.resize(new_size, Image.LANCZOS)

        img.save(jpg, "JPEG", quality=QUALITY, optimize=True)
        after = jpg.stat().st_size
        total_after += after

        gain = (1 - after / before) * 100
        print(f"  {png.name} : {before//1024}Ko -> {after//1024}Ko ({gain:.0f}%)")
        converted.append(png.name)

        # Supprimer le PNG original
        png.unlink()

    except Exception as e:
        print(f"  ERREUR {png.name}: {e}")

print()
print(f"Total avant : {total_before//1024//1024} Mo")
print(f"Total apres : {total_after//1024//1024} Mo")
print(f"Gain total  : {(1 - total_after/total_before)*100:.0f}%")
print(f"Images converties : {len(converted)}")
