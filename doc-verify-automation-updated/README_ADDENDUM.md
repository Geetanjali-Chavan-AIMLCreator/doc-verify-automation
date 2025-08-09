# Document Verification Automation (Sanitized • E‑Governance IDs)

**Pipeline you used (captured here, safely):**

1) **Image Processing / Enhancement** on each PDF page image
   - grayscale → **denoise** (bilateral) → **unsharp mask** → **CLAHE** contrast → **adaptive threshold**
2) **OCR extraction** (pytesseract) from enhanced images
3) **Regex + pattern matching** against applicant-entered text file/CSV
   - PAN / Aadhaar format checks
   - DOB normalization
   - Fuzzy string match for Name & Address
4) **Scoring** → **Excel report** → **OK** if overall ≥ 90%

You can tune steps in `src/image_enhance.py` and field rules in `src/match_rules.py`.
