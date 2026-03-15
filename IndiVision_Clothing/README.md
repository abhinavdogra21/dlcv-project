# IndiVision: Indian Traditional Clothing Dataset

> **CSE3292 — Deep Learning for Computer Vision | January 2026**

## Overview

A large-scale image classification dataset of **Indian Traditional Clothing** containing **3,218 images** across **12 culturally distinct garment categories**. Built to fill the gap in Western-centric computer vision datasets by providing India-specific clothing data.

Inspired by: **Fashion-101 / Indo Fashion Dataset**

---

## Dataset Statistics

| Metric | Value |
|---|---|
| Total images | 3,218 |
| Number of classes | 12 |
| Image format | JPEG (.jpg) |
| Image resolution | 224 × 224 px |
| Train / Val / Test | 70% / 15% / 15% |

---

## Classes

| Class | Count | Description |
|---|---|---|
| `Saree` | 300 | Traditional draped garment; cotton, georgette, silk variants |
| `Lehenga` | 343 | Flared skirt + blouse (choli); bridal, embroidered, ghagra |
| `Salwar_kameez` | 350 | Tunic + loose trousers; Anarkali, churidar, Patiala styles |
| `Kurti` | 346 | Short/long tunic worn with leggings or palazzos |
| `Blouse` | 300 | Women's fitted top; worn under saree or lehenga |
| `Sherwani` | 344 | Men's long coat-like formal/wedding garment |
| `Men's_kurta` | 178 | Men's traditional kurta |
| `Nehru_Jacket` | 348 | Men's sleeveless/short-sleeved collarless jacket |
| `Palazzo` | 305 | Wide-leg women's trousers; ethnic Indian fashion |
| `Bandhani` | 124 | Tie-dye fabric with circular dot patterns (Rajasthan/Gujarat) |
| `Banarasi_Silk` | 147 | Varanasi handwoven silk with gold/silver zari brocade |
| `Kanjeevaram_Saree` | 133 | South Indian silk saree with wide contrasting borders |

---

## Folder Structure

```
IndiVision_Clothing/
├── images/
│   ├── train/          # 70% split — 2254 images
│   ├── val/            # 15% split — 483 images
│   └── test/           # 15% split — 481 images
├── annotations/
│   └── metadata.csv    # Full annotation with split info
├── metadata/
│   └── annotations.csv # Clean annotation CSV (PDF format)
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

## What are train / val / test?

| Split | Purpose | Size |
|---|---|---|
| **train** | Used to train / fine-tune the model | 2,254 (70%) |
| **val** | Monitor model accuracy during training; tune hyperparameters | 483 (15%) |
| **test** | Final evaluation — model never sees this during training | 481 (15%) |

---

## Annotation CSV Format

`metadata/annotations.csv` — per the project PDF specification:

```csv
image_id,filename,label,annotator,date,source
1,Saree_00001.jpg,Saree,Abhinav Dogra,2026-02-15,cbazaar.com
2,Lehenga_00351.jpg,Lehenga,Kartik Sansanwal,2026-03-13,craftcouncil.in
```

### Image Naming Convention
```
<ClassName>_<NNNNN>.jpg
Example: Banarasi_Silk_00042.jpg
```

---

## Data Sources & Licensing

| Source Type | Examples | License | Notes |
|---|---|---|---|
| **E-commerce Websites** | `ajio.com`, `biba.in`, `cbazaar.com`, `craftsvilla.com`, `fabindia.com`, `limeroad.com`, `myntra.com`, `nykafashion.com`, `pantaloons.com`, `tatacliq.com`, `utsavfashion.com`, `westside.com` | Fair Use / Research Use | High-quality catalog images of Indian clothing. |
| **Government & Handicraft Portals** | `handlooms.nic.in`, `india.gov.in/textiles`, `texmin.nic.in`, `craftcouncil.in`, `sikshalochan.nic.in` | Open / Fair Use | Authentic handloom and textile archives. |
| **Educational Institutions** | `nift.ac.in` | Research Use | Fashion and textile design reference images. |

---

## Ethical Considerations

- **Privacy**: Catalog/model images used; no personally identifiable crowd photos
- **Bias**: Covers male and female garments; North, South, East, and West Indian traditions
- **Attribution**: All sources documented in `metadata/annotations.csv`

---

## Citation

```
IndiVision Indian Traditional Clothing Dataset
CSE3292 — Deep Learning for Computer Vision, January 2026
```
