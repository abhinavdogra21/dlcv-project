"""
IndiVision Clothing Dataset Verifier
=====================================
Verifies the final dataset structure, counts, and image integrity.

Usage:
    python3 verify_dataset.py
    python3 verify_dataset.py --per-class
    python3 verify_dataset.py --check-corrupt
"""

import sys
import csv
import argparse
from pathlib import Path
from PIL import Image

DATASET_DIR = Path("IndiVision_Clothing")
VALID_CLASSES = [
    "Saree", "Lehenga", "Salwar_Kameez", "Kurti",
    "Sherwani", "Kurta_Pajama", "Dhoti_Kurta",
    "Bandhani", "Banarasi_Silk", "Kanjeevaram_Saree",
]
MIN_PER_CLASS_TRAIN = 60   # relaxed minimum


def count_by_class_split():
    counts = {}
    for split in ["train", "val", "test"]:
        counts[split] = {}
        for cls in VALID_CLASSES:
            d = DATASET_DIR / "images" / split / cls
            n = sum(1 for f in d.iterdir() if f.suffix.lower() in {".jpg", ".jpeg", ".png"}) if d.exists() else 0
            counts[split][cls] = n
    return counts


def check_corrupt():
    bad = []
    for split in ["train", "val", "test"]:
        for cls in VALID_CLASSES:
            d = DATASET_DIR / "images" / split / cls
            if not d.exists():
                continue
            for img in d.iterdir():
                if img.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                    continue
                try:
                    with Image.open(img) as im:
                        im.verify()
                except Exception:
                    bad.append(str(img))
    return bad


def verify_csv():
    csv_path = DATASET_DIR / "annotations" / "metadata.csv"
    if not csv_path.exists():
        return False, "metadata.csv not found"
    rows = list(csv.DictReader(open(csv_path)))
    required = {"image_id", "filename", "class", "split", "source", "annotator", "date"}
    if not required.issubset(rows[0].keys() if rows else set()):
        return False, f"Missing columns. Found: {rows[0].keys() if rows else 'empty'}"
    return True, len(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-class",    action="store_true", help="Show per-class image counts")
    parser.add_argument("--check-corrupt",action="store_true", help="Check for corrupt images")
    args = parser.parse_args()

    print("=" * 60)
    print("IndiVision Clothing Dataset — Verifier")
    print("=" * 60)

    if not DATASET_DIR.exists():
        print(f"❌ Dataset directory not found: {DATASET_DIR}")
        sys.exit(1)

    counts = count_by_class_split()
    total = sum(sum(c.values()) for c in counts.values())
    train_total = sum(counts["train"].values())
    val_total   = sum(counts["val"].values())
    test_total  = sum(counts["test"].values())

    print(f"\n📊 Total images : {total}")
    print(f"   Train        : {train_total}")
    print(f"   Val          : {val_total}")
    print(f"   Test         : {test_total}")

    status_total = "✅" if total >= 2400 else "⚠️ "
    print(f"\n{status_total} Target ≥ 2400 images: {'PASS' if total >= 2400 else f'FAIL (have {total})'}")

    if args.per_class or True:
        print("\n📋 Per-class breakdown (train | val | test | TOTAL):")
        all_ok = True
        for cls in VALID_CLASSES:
            tr = counts["train"].get(cls, 0)
            va = counts["val"].get(cls, 0)
            te = counts["test"].get(cls, 0)
            tot = tr + va + te
            ok = tr >= MIN_PER_CLASS_TRAIN
            all_ok = all_ok and ok
            sym = "✔" if ok else "⚠"
            print(f"  {sym} {cls:<25}  {tr:>4} | {va:>4} | {te:>4} | {tot:>5}")
        print(f"\n  Minimum train images per class (≥{MIN_PER_CLASS_TRAIN}): {'PASS ✅' if all_ok else 'FAIL ⚠️ (some classes need more images)'}")

    # CSV check
    ok, info = verify_csv()
    if ok:
        print(f"\n✅ metadata.csv: valid ({info} rows)")
    else:
        print(f"\n❌ metadata.csv: {info}")

    # File structure check
    required_dirs = ["images/train", "images/val", "images/test", "annotations", "splits", "docs"]
    missing = [d for d in required_dirs if not (DATASET_DIR / d).exists()]
    if missing:
        print(f"\n⚠️  Missing directories: {missing}")
    else:
        print(f"\n✅ Folder structure: all required directories present")

    # Split files
    for sf in ["train.txt", "val.txt", "test.txt"]:
        p = DATASET_DIR / "splits" / sf
        if p.exists():
            n = len(p.read_text().strip().splitlines())
            print(f"   splits/{sf}: {n} entries")

    if args.check_corrupt:
        print("\n🔬 Checking for corrupt images...")
        bad = check_corrupt()
        if bad:
            print(f"  ⚠️  Found {len(bad)} corrupt images:")
            for b in bad[:10]:
                print(f"    {b}")
        else:
            print("  ✅ No corrupt images found")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
