"""
IndiVision Clothing Dataset Builder
=====================================
Merges existing Roboflow data + scraped images into a clean dataset.

Source 1: INDIAN DRESSES.v1i.folder/  (20 classes → mapped to 10)
Source 2: sherwani.v1i.yolov8/        (3 classes → mapped to 10)
Source 3: raw_scraped/                (10 classes, already labelled)

Output:   IndiVision_Clothing/

Splits: 70% train / 15% val / 15% test

Usage:
    python3 build_dataset.py
"""

import os
import shutil
import csv
import random
import hashlib
import datetime
from pathlib import Path
from PIL import Image

# ─── CONFIG ──────────────────────────────────────────────────────────────────
SEED         = 42
TRAIN_RATIO  = 0.70
VAL_RATIO    = 0.15
# TEST_RATIO = 0.15 (remainder)

SOURCE_ROBOFLOW    = Path("INDIAN DRESSES.v1i.folder")
SOURCE_SHERWANI    = Path("sherwani.v1i.yolov8")
SOURCE_SCRAPED     = Path("raw_scraped")
OUTPUT_DIR         = Path("IndiVision_Clothing")

# ─── CLASS MAPPING: old Roboflow names → new 10 classes ──────────────────────
ROBOFLOW_MAP = {
    # Saree family
    "Saree":                  "Saree",
    "Banarasi_Saree":         "Banarasi_Silk",
    "Kanjeevaram_Saree":      "Kanjeevaram_Saree",
    "Bandhani_Saree":         "Bandhani",
    "Bridal_Saree":           "Saree",
    "Contemporary_Saree":     "Saree",
    "Designer_Saree":         "Saree",
    "Modern_Saree":           "Saree",
    "Vintage_Saree":          "Saree",
    # Lehenga family
    "Lehenga":                "Lehenga",
    "Embroidered_Lehenga":    "Lehenga",
    "Ghagra":                 "Lehenga",
    # Salwar / Anarkali
    "Salwar_Kameez":          "Salwar_Kameez",
    "Anarkali":               "Salwar_Kameez",
    # Kurti / Choli
    "Kurti":                  "Kurti",
    "Choli":                  "Kurti",
    "Mirror_Work_Dress":      "Kurti",
    # Broad Indian Dress categories
    "Ethnic_Indian_Dress":    "Kurti",
    "Festive_Indian_Dress":   "Lehenga",
    "Traditional_Indian_Dress": "Salwar_Kameez",
}

SHERWANI_MAP = {
    "Desgin sherwani":  "Sherwani",
    "Plain sherwani":   "Sherwani",
    "Plain kurta":      "Kurta_Pajama",
}

VALID_CLASSES = [
    "Saree", "Lehenga", "Salwar_Kameez", "Kurti",
    "Sherwani", "Kurta_Pajama", "Dhoti_Kurta",
    "Bandhani", "Banarasi_Silk", "Kanjeevaram_Saree",
]

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def file_md5(path: Path) -> str:
    h = hashlib.md5()
    h.update(path.read_bytes())
    return h.hexdigest()


def is_valid_image(path: Path) -> bool:
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception:
        return False


def convert_and_copy(src: Path, dst: Path):
    """Copy image to dst, converting to RGB JPEG."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        with Image.open(src) as img:
            img.convert("RGB").save(dst, "JPEG", quality=90)
    except Exception:
        pass


# ─── COLLECTION ──────────────────────────────────────────────────────────────

class ImageRecord:
    def __init__(self, src_path, class_name, source_name):
        self.src_path = src_path
        self.class_name = class_name
        self.source = source_name
        self.md5 = None

    def compute_hash(self):
        try:
            self.md5 = file_md5(self.src_path)
        except Exception:
            self.md5 = None


def scan_roboflow(base: Path, class_map: dict, source_tag: str) -> list:
    records = []
    for split in ["train", "valid", "test"]:
        split_dir = base / split
        if not split_dir.exists():
            continue
        for class_dir in split_dir.iterdir():
            if not class_dir.is_dir():
                continue
            mapped = class_map.get(class_dir.name)
            if mapped is None:
                continue
            for img in class_dir.iterdir():
                if img.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
                    if is_valid_image(img):
                        records.append(ImageRecord(img, mapped, source_tag))
    return records


def scan_sherwani(base: Path, class_map: dict) -> list:
    """Scan sherwani dataset whose images are in train/images/ with labels in train/labels/."""
    records = []
    labels_dir = base / "train" / "labels"
    images_dir = base / "train" / "images"
    if not images_dir.exists():
        return records

    # Read data.yaml to get class names
    yaml_path = base / "data.yaml"
    class_names = []
    if yaml_path.exists():
        for line in yaml_path.read_text().splitlines():
            if line.strip().startswith("names:"):
                raw = line.split(":", 1)[1].strip().strip("[]")
                class_names = [c.strip().strip("'\"") for c in raw.split(",")]

    for img in images_dir.iterdir():
        if img.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        if not is_valid_image(img):
            continue
        # Determine class from label file
        label_file = labels_dir / (img.stem + ".txt")
        class_name = None
        if label_file.exists():
            lines = label_file.read_text().strip().splitlines()
            if lines:
                try:
                    cls_idx = int(lines[0].split()[0])
                    raw_name = class_names[cls_idx] if cls_idx < len(class_names) else None
                    class_name = class_map.get(raw_name)
                except Exception:
                    pass
        if class_name:
            records.append(ImageRecord(img, class_name, "sherwani_roboflow"))
    return records


def scan_scraped(base: Path) -> list:
    records = []
    if not base.exists():
        return records
    for class_dir in base.iterdir():
        if not class_dir.is_dir():
            continue
        class_name = class_dir.name
        if class_name not in VALID_CLASSES:
            continue
        for img in class_dir.iterdir():
            if img.suffix.lower() in {".jpg", ".jpeg", ".png"}:
                if is_valid_image(img):
                    records.append(ImageRecord(img, class_name, "web_scraped"))
    return records


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    random.seed(SEED)
    today = datetime.date.today().isoformat()

    print("=" * 60)
    print("IndiVision Clothing Dataset — Builder")
    print("=" * 60)

    # 1. Collect all records
    print("\n📂 Scanning sources...")
    records = []
    r1 = scan_roboflow(SOURCE_ROBOFLOW, ROBOFLOW_MAP, "indian_dresses_roboflow")
    print(f"  INDIAN DRESSES dataset: {len(r1)} images")
    records += r1

    r2 = scan_sherwani(SOURCE_SHERWANI, SHERWANI_MAP)
    print(f"  Sherwani dataset:       {len(r2)} images")
    records += r2

    r3 = scan_scraped(SOURCE_SCRAPED)
    print(f"  Web scraped:            {len(r3)} images")
    records += r3

    print(f"\n  Total raw records: {len(records)}")

    # 2. Deduplicate by hash
    print("\n🔍 Deduplicating...")
    seen_hashes = set()
    unique_records = []
    for rec in records:
        rec.compute_hash()
        if rec.md5 and rec.md5 not in seen_hashes:
            seen_hashes.add(rec.md5)
            unique_records.append(rec)
    print(f"  Unique images: {len(unique_records)} (removed {len(records)-len(unique_records)} duplicates)")

    # 3. Group by class
    class_groups = {cls: [] for cls in VALID_CLASSES}
    for rec in unique_records:
        if rec.class_name in class_groups:
            class_groups[rec.class_name].append(rec)

    print("\n📊 Per-class counts (before split):")
    for cls, recs in class_groups.items():
        print(f"  {cls:<25} {len(recs)} images")

    # 4. Split and copy
    print("\n📁 Building dataset folder structure...")
    OUTPUT_DIR.mkdir(exist_ok=True)

    metadata_rows = []
    split_files = {"train": [], "val": [], "test": []}
    image_id = 1

    for cls, recs in class_groups.items():
        random.shuffle(recs)
        n = len(recs)
        n_train = int(n * TRAIN_RATIO)
        n_val   = int(n * VAL_RATIO)

        splits = (
            [("train", r) for r in recs[:n_train]] +
            [("val",   r) for r in recs[n_train:n_train+n_val]] +
            [("test",  r) for r in recs[n_train+n_val:]]
        )

        for split_name, rec in splits:
            fname = f"{cls}_{image_id:05d}.jpg"
            dst = OUTPUT_DIR / "images" / split_name / cls / fname
            convert_and_copy(rec.src_path, dst)

            rel_path = f"images/{split_name}/{cls}/{fname}"
            metadata_rows.append({
                "image_id":  image_id,
                "filename":  fname,
                "class":     cls,
                "split":     split_name,
                "source":    rec.source,
                "annotator": "auto",
                "date":      today,
            })
            split_files[split_name].append(rel_path)
            image_id += 1

    # 5. Annotations CSV
    ann_dir = OUTPUT_DIR / "annotations"
    ann_dir.mkdir(exist_ok=True)
    csv_path = ann_dir / "metadata.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["image_id","filename","class","split","source","annotator","date"])
        writer.writeheader()
        writer.writerows(metadata_rows)
    print(f"  ✔ metadata.csv written ({len(metadata_rows)} rows)")

    # 6. Split txt files
    splits_dir = OUTPUT_DIR / "splits"
    splits_dir.mkdir(exist_ok=True)
    for split_name, paths in split_files.items():
        (splits_dir / f"{split_name}.txt").write_text("\n".join(paths) + "\n")
    print(f"  ✔ split files written  train={len(split_files['train'])} val={len(split_files['val'])} test={len(split_files['test'])}")

    # 7. Summary
    total = len(metadata_rows)
    print(f"\n{'='*60}")
    print(f"✅ Dataset built! Total images: {total}")
    print(f"   Location: {OUTPUT_DIR.resolve()}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
