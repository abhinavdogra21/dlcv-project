"""
IndiVision Clothing Dataset Scraper
=====================================
Downloads images for Indian Traditional Clothing classes using icrawler.
Output goes to: raw_scraped/<ClassName>/

Usage:
    python3 scraper.py
"""

import os
import sys
import hashlib
import time
import logging
import shutil
from pathlib import Path
from PIL import Image

# Suppress icrawler verbose output
logging.getLogger("icrawler").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

try:
    from icrawler.builtin import BingImageCrawler, GoogleImageCrawler
except ImportError:
    print("icrawler not found. Run: pip3 install icrawler")
    sys.exit(1)

# ─── CONFIG ──────────────────────────────────────────────────────────────────
OUTPUT_DIR   = Path("raw_scraped")
TARGET_COUNT = 200          # images to download per class
MIN_RES      = 80           # min pixel dimension (width or height)
DELAY_SEC    = 0.3          # polite delay between batches

# ─── CLASS SEARCH QUERIES ────────────────────────────────────────────────────
CLASS_QUERIES = {
    "Saree": [
        "Indian woman wearing saree traditional",
        "saree draping styles Indian",
        "Indian silk cotton saree outfit",
        "saree fashion India full body",
    ],
    "Lehenga": [
        "Indian lehenga choli bridal",
        "embroidered lehenga skirt Indian woman",
        "ghagra choli Rajasthani outfit",
        "lehenga dupatta Indian fashion",
    ],
    "Salwar_Kameez": [
        "salwar kameez Indian woman suit",
        "anarkali salwar kameez Indian",
        "punjabi suit salwar kameez traditional",
        "churidar salwar kameez India",
    ],
    "Kurti": [
        "Indian kurti cotton woman fashion",
        "long kurti India ethnic wear",
        "printed cotton kurti Indian woman",
        "kurti with palazzo Indian outfit",
    ],
    "Sherwani": [
        "sherwani Indian groom traditional",
        "men sherwani ethnic Indian wedding",
        "designer sherwani Indian",
        "plain sherwani Indian groom outfit",
    ],
    "Kurta_Pajama": [
        "Indian men kurta pajama traditional",
        "kurta pajama ethnic wear India",
        "men cotton kurta pajama Indian",
        "indian kurta pajama festive",
    ],
    "Dhoti_Kurta": [
        "dhoti kurta Indian traditional men",
        "Indian man wearing dhoti kurta",
        "South Indian dhoti veshti traditional",
        "dhoti kurta Hindu festival outfit",
    ],
    "Bandhani": [
        "bandhani saree tie dye Indian",
        "bandhani dress Rajasthan India",
        "bandhani fabric Indian clothing",
        "bandhani dupatta Indian woman",
    ],
    "Banarasi_Silk": [
        "Banarasi silk saree zari weaving",
        "Banarasi saree gold brocade Indian",
        "Varanasi Banarasi saree traditional",
        "Banarasi silk saree wedding",
    ],
    "Kanjeevaram_Saree": [
        "Kanjeevaram saree South Indian silk",
        "Kanjivaram silk saree temple border",
        "Tamil Nadu Kanjeevaram saree",
        "Kanjeevaram saree wedding South India",
    ],
}

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def file_md5(path: Path) -> str:
    h = hashlib.md5()
    h.update(path.read_bytes())
    return h.hexdigest()


def is_valid_image(path: Path, min_dim: int = MIN_RES) -> bool:
    """Return True if the file is a readable image above min_dim."""
    try:
        with Image.open(path) as img:
            w, h = img.size
            return w >= min_dim and h >= min_dim
    except Exception:
        return False


def clean_folder(folder: Path):
    """Remove corrupt and duplicate images from folder. Returns (kept, removed) counts."""
    seen_hashes = set()
    kept = removed = 0
    for f in sorted(folder.iterdir()):
        if f.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            f.unlink(missing_ok=True)
            removed += 1
            continue
        if not is_valid_image(f):
            f.unlink(missing_ok=True)
            removed += 1
            continue
        h = file_md5(f)
        if h in seen_hashes:
            f.unlink(missing_ok=True)
            removed += 1
            continue
        seen_hashes.add(h)
        # Rename to jpg
        new_path = f.with_suffix(".jpg")
        if f.suffix.lower() != ".jpg":
            try:
                with Image.open(f) as img:
                    img.convert("RGB").save(new_path, "JPEG", quality=90)
                f.unlink()
            except Exception:
                f.unlink(missing_ok=True)
                removed += 1
                continue
        kept += 1
    return kept, removed


def count_images(folder: Path) -> int:
    if not folder.exists():
        return 0
    return sum(1 for f in folder.iterdir() if f.suffix.lower() in {".jpg", ".jpeg", ".png"})


def crawl_class(class_name: str, queries: list, target: int, out_dir: Path):
    """Download images for one class using Bing then Google crawlers."""
    class_dir = out_dir / class_name
    class_dir.mkdir(parents=True, exist_ok=True)

    remaining = target - count_images(class_dir)
    if remaining <= 0:
        print(f"  ✔ {class_name}: already has {count_images(class_dir)} images")
        return

    per_query = max(remaining // len(queries) + 1, 30)

    for qi, query in enumerate(queries):
        current = count_images(class_dir)
        if current >= target:
            break
        need = min(per_query, target - current + 10)   # slight over-fetch

        print(f"  [{qi+1}/{len(queries)}] Bing: '{query}' → {need} images ...", end="", flush=True)
        try:
            crawler = BingImageCrawler(
                storage={"root_dir": str(class_dir)},
                feeder_threads=2,
                parser_threads=2,
                downloader_threads=4,
            )
            crawler.crawl(
                keyword=query,
                max_num=need,
                min_size=(MIN_RES, MIN_RES),
                file_idx_offset="auto",
            )
        except Exception as e:
            print(f" [Bing error: {e}]", end="")

        print(f" → {count_images(class_dir)} total", flush=True)
        time.sleep(DELAY_SEC)

    # Google fallback if still short
    if count_images(class_dir) < target * 0.7:
        print(f"  ⚡ Google fallback for {class_name} ...", flush=True)
        try:
            crawler = GoogleImageCrawler(
                storage={"root_dir": str(class_dir)},
                feeder_threads=1,
                parser_threads=1,
                downloader_threads=3,
            )
            crawler.crawl(
                keyword=queries[0] + " India",
                max_num=target - count_images(class_dir) + 20,
                min_size=(MIN_RES, MIN_RES),
                file_idx_offset="auto",
            )
        except Exception as e:
            print(f"  [Google error: {e}]")
        time.sleep(DELAY_SEC)


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    print("=" * 60)
    print("IndiVision Clothing Dataset — Web Scraper")
    print(f"Target: {TARGET_COUNT} images per class | {len(CLASS_QUERIES)} classes")
    print("=" * 60)

    total_downloaded = 0

    for class_name, queries in CLASS_QUERIES.items():
        print(f"\n📦 Class: {class_name}")
        crawl_class(class_name, queries, TARGET_COUNT, OUTPUT_DIR)

        print(f"  🧹 Cleaning {class_name} ...", end="", flush=True)
        kept, removed = clean_folder(OUTPUT_DIR / class_name)
        print(f" kept={kept}, removed={removed}")
        total_downloaded += kept

    print("\n" + "=" * 60)
    print(f"✅ Scraping complete! Total clean images: {total_downloaded}")
    print(f"Output: {OUTPUT_DIR.resolve()}")
    print("Run build_dataset.py next to merge and structure the dataset.")
    print("=" * 60)

    # Per-class summary
    print("\nPer-class summary:")
    for cls in CLASS_QUERIES:
        n = count_images(OUTPUT_DIR / cls)
        status = "✔" if n >= TARGET_COUNT * 0.7 else "⚠"
        print(f"  {status} {cls:<25} {n} images")


if __name__ == "__main__":
    main()
