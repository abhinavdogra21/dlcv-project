# IndiVision Clothing Dataset: Class Definitions

This document outlines the specific inclusion criteria, descriptions, visual characteristics, and edge case handling for the 13 classes within the IndiVision dataset. These guidelines were used by the annotation team to maintain consistency.

## 1. Saree
- **Description:** A traditional women's garment consisting of an unstitched drape varying from 4.5 to 9 meters in length, typically wrapped around the waist with one end draped over the shoulder.
- **Visual Examples:** Can be made of various materials (cotton, georgette, silk) with or without borders.
- **Edge Cases:** 
    - *Is it a Saree or a Lehenga Saree?* Annotate as `Saree` if the draped element over the shoulder originates from an unstitched waist wrap. If it is a distinct pre-stitched skirt, annotate as `Lehenga`.
    - If the drape is Kanjeevaram or Banarasi Silk, it should be annotated under those specific sub-classes rather than the generic `Saree` class.

## 2. Lehenga
- **Description:** A form of an ankle-length skirt worn by Indian women, typically secured at the waist, leaving the lower back and midriff bare. It is worn with a fitted blouse (choli) and a dupatta.
- **Visual Examples:** Highly embroidered bridal lehengas, ghagra cholis, and modern flared ethnic skirts.
- **Edge Cases:** If the choli (blouse) is highly visible on its own but forms part of a lehenga set, annotate the entire ensemble as `Lehenga`.

## 3. Salwar_Kameez
- **Description:** A traditional outfit comprising a tunic (kameez) and typically loose or gathered trousers (salwar), accompanied by a dupatta. 
- **Visual Examples:** Patiala suits, Anarkali suits, straight-cut churidars.
- **Edge Cases:** If only the top part (kameez) is visible without the trousers, still annotate as `Salwar_Kameez` if it forms a traditional suit silhouette rather than a standalone `Kurti`.

## 4. Kurti
- **Description:** A shorter or standalone version of the kurta/kameez, typically worn by women over leggings, jeans, or palazzos.
- **Visual Examples:** Cotton daily-wear tunics, short A-line tops with Indian motifs.
- **Edge Cases:** Differentiated from `Salwar_Kameez` by the absence of a matching traditional lower garment/dupatta in the product/catalog image.

## 5. Blouse
- **Description:** A short, tailored, and fitted top worn by women, usually under a Saree or paired with a Lehenga.
- **Visual Examples:** Embroidered necklines, backless designs, or standard unembellished padded saree blouses.
- **Edge Cases:** If an image focuses tightly on the blouse itself without showing the full drape of a saree, label as `Blouse`.

## 6. Sherwani
- **Description:** A long coat-like garment worn by men in India, very similar to an achkan or doublet, typically worn over a kurta variations.
- **Visual Examples:** Heavy zari worked garments used for grooms, button-down from the front, reaching below the knees.
- **Edge Cases:** If it is shorter and collarless, it may be a `Nehru_Jacket` instead. 

## 7. Kurta_Pajama
- **Description:** A traditional men's outfit consisting of a loose, collarless shirt (kurta) and lightweight drawstring trousers (pajama).
- **Visual Examples:** Cotton daily-wear men's kurtas, festival kurtas with churidar bottoms.
- **Edge Cases:** If worn with a jacket, the dominant outer garment (e.g., `Nehru_Jacket`) takes precedence if it covers the majority of the kurta.

## 8. Dhoti_Kurta
- **Description:** A traditional men's garment where the lower half consists of an unstitched piece of cloth wrapped around the waist and legs (dhoti), paired with a standard kurta.
- **Visual Examples:** South Indian silk dhotis, Bengali style pleated dhotis.
- **Edge Cases:** Only label if the distinct wrapped style of the dhoti is clearly visible. If occluded, default to `Kurta_Pajama` if unsure.

## 9. Nehru_Jacket
- **Description:** A hip-length tailored coat for men or women, featuring a mandarin collar. Typically sleeveless or short-sleeved.
- **Visual Examples:** Solid color Modi/Nehru jackets worn over kurtas.
- **Edge Cases:** Must have a mandarin/stand-up collar and typically buttoned down the front. 

## 10. Palazzo
- **Description:** Wide-legged, loose, flowing trousers worn by women, frequently paired with Kurtis or short tunics.
- **Visual Examples:** Highly flared ethnic pants, often with borders or prints.
- **Edge Cases:** Only images focusing prominently on the wide-leg ethnic trousers (or where it is the highlighted garment) should be `Palazzo`.

## 11. Bandhani
- **Description:** A highly specialized tie-dye textile decorated by plucking the cloth into many tiny bindings to form a continuous pattern of dots.
- **Visual Examples:** Distinctive clustered dot patterns forming squares, waves, or webs on dupattas, sarees, or unstitched fabric.
- **Edge Cases:** Trumps generic classes. If a Saree is predominantly Bandhani print, it belongs in this class rather than generic `Saree`.

## 12. Banarasi_Silk
- **Description:** A highly complex and rich silk fabric woven in Varanasi, distinguished by intricate zari (gold/silver thread) brocade work and Mughal-inspired floral/foliate motifs.
- **Visual Examples:** Heavy silk sarees with thick gold borders and highly detailed all-over motifs.
- **Edge Cases:** Given precedence over the generic `Saree` class due to its distinct texture and regional significance.

## 13. Kanjeevaram_Saree
- **Description:** A traditional silk Saree originating from Kanchipuram, marked by heavy mulberry silk, vibrant distinct colors, and wide temple borders interlocked with the main body.
- **Visual Examples:** Solid bright colors (e.g., magenta, green) with thick contrast borders woven in gold.
- **Edge Cases:** Trumps generic `Saree`. If visually ambiguous between Banarasi and Kanjeevaram without metadata, annotators must rely on border styles (Kanjeevaram temple borders vs Banarasi Mughal motifs).
