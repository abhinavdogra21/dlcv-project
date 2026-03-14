# Class Definitions — IndiVision Indian Traditional Clothing Dataset

## Overview
This document defines the 10 clothing classes used in the dataset, including visual descriptions, key identifiers, and edge-case rules.

---

## 1. Saree
**Description:** A traditional draped garment consisting of a long unstitched cloth (5–9 meters) wrapped around the body. Includes cotton, georgette, chiffon, and other non-silk variants.

**Visual identifiers:**
- Long drape starting from waist, with pallu over shoulder
- Worn with petticoat and blouse
- Various regional draping styles (Nivi, Bengali, Gujarati, Maharashtrian)

**Edge cases:**
- If the saree is clearly Banarasi silk → assign `Banarasi_Silk`
- If clearly Kanjeevaram → assign `Kanjeevaram_Saree`
- If clearly Bandhani pattern → assign `Bandhani`
- If bridal, contemporary or vintage but no specific regional silk identifier → assign `Saree`

---

## 2. Lehenga
**Description:** A long flared skirt paired with a choli (blouse) and dupatta. Includes bridal lehenga, ghagra-choli, and embroidered lehenga.

**Visual identifiers:**
- Flared full-length skirt
- Paired with short blouse (choli)
- Usually has heavy embroidery, mirror work, or embellishments
- Worn during weddings and festivals

**Edge cases:**
- Ghagra-choli → `Lehenga`
- If has mirror work but is a short dress with no skirt → `Kurti`

---

## 3. Salwar_Kameez
**Description:** A two or three-piece outfit consisting of a long tunic (kameez) and loose trousers (salwar), often with a dupatta. Includes Anarkali, churidar, Patiala styles.

**Visual identifiers:**
- Long tunic reaching mid-thigh or below
- Loose or fitted trousers
- Anarkali: flared umbrella-cut tunic

**Edge cases:**
- Very short tunic with trousers → `Kurti`
- If clearly recognizable as Anarkali style → `Salwar_Kameez`

---

## 4. Kurti
**Description:** A short or long tunic worn by women, typically paired with leggings, palazzos, or jeans. More casual than Salwar Kameez.

**Visual identifiers:**
- Hemline between hip and knee
- Usually not paired with matching bottoms
- Often printed (block print, digital print, tie-dye)

**Edge cases:**
- If the kurti is knee-length with matching salwar → `Salwar_Kameez`

---

## 5. Sherwani
**Description:** A long coat-like garment worn by Indian men, mainly for weddings and formal occasions. Has Mughal/Central Asian origins.

**Visual identifiers:**
- Long coat reaching knee or below
- Worn by men
- Buttoned front
- Paired with churidar or dhoti

**Edge cases:**
- Plain Sherwani or designed: both are `Sherwani`
- Short jacket/nehru jacket → not a sherwani, exclude

---

## 6. Kurta_Pajama
**Description:** A men's traditional two-piece outfit consisting of a kurta (long tunic) paired with pajama (loose trousers). Widely worn across India.

**Visual identifiers:**
- Men's collarless or band-collar tunic
- Hemline below hip to mid-calf
- Paired with straight or tapered trousers

**Edge cases:**
- With churidar bottoms → `Kurta_Pajama`
- With dhoti → `Dhoti_Kurta`

---

## 7. Dhoti_Kurta
**Description:** Men's outfit comprising a dhoti (unstitched lower garment wrapped around waist/legs) with a kurta.

**Visual identifiers:**
- White/off-white unstitched cloth wrapped around waist
- Tucked between legs
- Paired with short or long kurta
- Common in South India (veshti/mundu) and North India

**Edge cases:**
- If lower garment is clearly stitched trousers → `Kurta_Pajama`

---

## 8. Bandhani
**Description:** Traditional Indian tie-dye textile featuring circular dot patterns. May appear as sarees, dupattas, or dress material.

**Visual identifiers:**
- Circular or geometric dot pattern formed by tie-dye technique
- Vibrant colors (red, yellow, green on dark base)
- Common in Gujarat and Rajasthan

**Edge cases:**
- Bandhani saree → `Bandhani` (not `Saree`)
- Lehenga with Bandhani fabric → `Bandhani`
- Plain printed dots (not tie-dye) → do not classify as Bandhani

---

## 9. Banarasi_Silk
**Description:** Handwoven silk sarees from Varanasi with intricate gold/silver zari work, floral or Mughal motifs.

**Visual identifiers:**
- Glossy silk fabric with metallic thread weaving
- Dense floral/Mughal/geometric brocade patterns
- Gold or silver zari border and pallu
- Rich, heavy appearance

**Edge cases:**
- Other brocade sarees not from Banarasi tradition → `Saree`

---

## 10. Kanjeevaram_Saree
**Description:** South Indian silk saree from Kanchipuram known for wide contrasting borders and bold colors.

**Visual identifiers:**
- Thick, heavy silk with a distinct wide border in contrasting color
- Gold zari thread woven into the fabric
- Border and body fabric are often different colors
- Temple motifs (rudraksha, checks, stripes)

**Edge cases:**
- Other South Indian sarees (Kerala kasavu, Mysore silk) without thick contrasting border → `Saree`

---

## Annotation Rules Summary

| Rule | Policy |
|---|---|
| Minimum visibility | Annotate if ≥ 40% of the garment is visible |
| Multiple garments | Assign the most prominent/focal garment class |
| Unclear class | Do not include in dataset; discard image |
| Background ambiguity | Focus on garment, not background setting |
| Catalog/e-commerce images | Accepted; garment must be the main subject |
