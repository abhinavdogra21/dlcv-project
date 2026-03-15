# IndiVision: Indian Traditional Clothing Dataset

> **CSE3292 — Deep Learning for Computer Vision | January 2026**

## Overview

A large-scale image classification dataset of **Indian Traditional Clothing** containing **3,950 images** across **13 culturally distinct garment categories**. Built to fill the gap in Western-centric computer vision datasets by providing India-specific clothing data.

Inspired by: **Fashion-101 / Indo Fashion Dataset**

---

## Dataset Statistics

| Metric | Value |
|---|---|
| Total images | 3,950 |
| Number of classes | 13 |
| Image format | JPEG (.jpg) |
| Image resolution | 224 × 224 px |
| Train / Val / Test | 70% / 15% / 15% |

---

## Classes

| Class | Count | Description |
|---|---|---|
| `Saree` | 350 | Traditional draped garment; cotton, georgette, silk variants |
| `Lehenga` | 350 | Flared skirt + blouse (choli); bridal, embroidered, ghagra |
| `Salwar_Kameez` | 350 | Tunic + loose trousers; Anarkali, churidar, Patiala styles |
| `Kurti` | 350 | Short/long tunic worn with leggings or palazzos |
| `Blouse` | 350 | Women's fitted top; worn under saree or lehenga |
| `Sherwani` | 350 | Men's long coat-like formal/wedding garment |
| `Kurta_Pajama` | 350 | Men's traditional kurta + loose trousers |
| `Dhoti_Kurta` | 350 | Men's dhoti (unstitched wrap) + kurta |
| `Nehru_Jacket` | 350 | Men's sleeveless/short-sleeved collarless jacket |
| `Palazzo` | 350 | Wide-leg women's trousers; ethnic Indian fashion |
| `Bandhani` | 150 | Tie-dye fabric with circular dot patterns (Rajasthan/Gujarat) |
| `Banarasi_Silk` | 150 | Varanasi handwoven silk with gold/silver zari brocade |
| `Kanjeevaram_Saree` | 150 | South Indian silk saree with wide contrasting borders |

---

## Folder Structure

```
IndiVision_Clothing/
├── images/
│   ├── train/          # 70% split — 2755 images
│   ├── val/            # 15% split — 586 images
│   └── test/           # 15% split — 609 images
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
| **train** | Used to train / fine-tune the model | 2,755 (70%) |
| **val** | Monitor model accuracy during training; tune hyperparameters | 586 (15%) |
| **test** | Final evaluation — model never sees this during training | 609 (15%) |

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
