# Document Verification Automation (Sanitized • E‑Governance IDs)

> Ethical, anonymized reconstruction of a production workflow I built for **e‑governance ID verification**.
> The repo uses **synthetic inputs** and generic names — no client data, internal code, or secrets.

## Problem (Anonymized)
Applicants upload **government ID documents** (Aadhaar, Voter ID, Passport, Driving License, PAN). 
Each application has:
- A **PDF bundle** containing the provided ID scans
- A **text/CSV report** with the details the applicant typed online (name, address, state, aadhaar, PAN, DOB, ...)

**Goal:** Automatically verify that details typed by the applicant **match** what appears in their documents.
Produce an **Excel report** with a **match percentage** per applicant; flag **OK** if score ≥ **90%** (tunable).

## Key Techniques
- OCR: `pytesseract` over rasterized PDF pages
- Normalization: Unicode cleanup, uppercasing, whitespace compression
- Matching: `rapidfuzz` token/partial ratios + regex format checks (PAN, Aadhaar, dates)
- Orchestration: simple CLI; outputs a single Excel for review

## Ethics & Confidentiality
- Only synthetic sample data is included.
- No client names, schemas, or internal identifiers appear.
- The architecture & code reflect my personal implementation approach, abstracted for public sharing.

## Folder Structure
```
doc-verify-automation/
  ├─ data/
  │  ├─ applicants/     # CSV inputs (synthetic)
  │  └─ pdfs/           # PDFs per application_id (synthetic)
  ├─ outputs/           # Excel reports
  ├─ src/
  │  ├─ extract_ocr.py
  │  ├─ match_rules.py
  │  ├─ utils.py
  │  └─ main.py
  ├─ requirements.txt
  └─ README.md
```


