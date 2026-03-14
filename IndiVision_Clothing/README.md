# IndiVision: Indian Traditional Clothing Dataset

> **CSE3292 — Deep Learning for Computer Vision | January 2026**

## Overview

A curated, large-scale image classification dataset of **Indian Traditional Clothing** containing 2400+ images across **10 culturally distinct garment categories**. Designed to fill the gap in Western-centric computer vision datasets by providing India-specific clothing data with geographic and demographic diversity.

---

## Dataset Statistics

| Metric | Value |
|---|---|
| Total images | ≥ 2400 |
| Number of classes | 10 |
| Image format | JPEG (.jpg) |
| Train / Val / Test | 70% / 15% / 15% |

---

## Classes

| Class | Description |
|---|---|
| `Saree` | Traditional draped garment (cotton, georgette, chiffon) |
| `Lehenga` | Flared skirt + blouse ensemble; includes bridal and ghagra |
| `Salwar_Kameez` | Two/three-piece suit; Anarkali, churidar, Patiala styles |
| `Kurti` | Short/long tunic worn with leggings or palazzos |
| `Sherwani` | Men's long coat-like formal/wedding garment |
| `Kurta_Pajama` | Men's traditional kurta + loose trousers |
| `Dhoti_Kurta` | Men's dhoti (unstitched wrap) + kurta |
| `Bandhani` | Tie-dye fabric with circular dot patterns (Rajasthan/Gujarat) |
| `Banarasi_Silk` | Handwoven Varanasi silk with gold/silver zari brocade |
| `Kanjeevaram_Saree` | South Indian silk saree with wide contrasting borders |

---

## Folder Structure

```
IndiVision_Clothing/
├── images/
│   ├── train/         # 70% of each class
│   │   ├── Saree/
│   │   ├── Lehenga/
│   │   └── ...
│   ├── val/           # 15% of each class
│   └── test/          # 15% of each class
├── annotations/
│   └── metadata.csv   # image_id, filename, class, split, source, annotator, date
├── splits/
│   ├── train.txt
│   ├── val.txt
│   └── test.txt
├── docs/
│   └── class_definitions.md
├── README.md
└── LICENSE
```

---

## Annotation Metadata Format

```csv
image_id, filename, class, split, source, annotator, date
1, Saree_00001.jpg, Saree, train, indian_dresses_roboflow, auto, 2026-03-14
2, Lehenga_00002.jpg, Lehenga, train, web_scraped, auto, 2026-03-14
```

### Source Tags
- `indian_dresses_roboflow` — From INDIAN DRESSES.v1i.folder (CC BY 4.0)
- `sherwani_roboflow` — From sherwani.v1i.yolov8 (CC BY 4.0)
- `web_scraped` — Bing/Google image search via icrawler

---

## Data Sources & Licensing

| Source | License | Notes |
|---|---|---|
| [Roboflow INDIAN DRESSES](https://universe.roboflow.com/image-classification-pkvlc/indian-dresses) | CC BY 4.0 | Attribution required |
| [Roboflow Sherwani](https://universe.roboflow.com/rahil-mehta-0chuf/sherwani/dataset/1) | CC BY 4.0 | Attribution required |
| Bing/Google Image Search | Various | Educational use; non-commercial |

---

## Annotation Strategy

- **Labeling**: Image-level classification (folder-based automatic labeling)
- **Edge cases**: Defined in `docs/class_definitions.md`
- **Multi-annotator**: 100 images cross-checked between 2 team members
- **Visibility rule**: Annotate if ≥ 40% of garment is visible

---

## Ethical Considerations

- **Privacy**: Catalog/model images used; no personally identifiable crowd photos
- **Consent**: Sourced from CC-licensed repositories and Roboflow public datasets
- **Bias**: Includes male and female garments; covers North, South, East, and West Indian clothing traditions
- **Attribution**: All sources documented in metadata.csv

---

## Usage (Python)

```python
from pathlib import Path
from PIL import Image

dataset_root = Path("IndiVision_Clothing")
train_images = list((dataset_root / "images" / "train").rglob("*.jpg"))

img = Image.open(train_images[0])
print(img.size)  # (width, height)
```

---

## Citation

```
IndiVision Indian Traditional Clothing Dataset
Created as part of CSE3292 - Deep Learning for Computer Vision
January 2026
```

---

## License

Dataset annotations are released under **CC BY 4.0**.
Individual image source licenses apply as documented in `annotations/metadata.csv`.
