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

## High‑Level Flow
```mermaid
flowchart LR
  A[Applicants CSV (typed data)] --> C[Matcher]
  B[PDFs (ID scans)] --> D[OCR Extraction]
  D --> C[Matcher]
  C --> E[Excel Report + Threshold Decision]
```
- **Ingest**: read applicant CSV + pick matching PDF(s) by `application_id`
- **Extract**: run OCR over PDF pages → normalized text
- **Match**: fuzzy match expected fields vs extracted text (per‑field scores) → weighted overall score
- **Decide**: mark **OK** if overall ≥ threshold (default 0.90)
- **Export**: write Excel with field‑level scores & overall decision

## Key Techniques
- OCR: `pytesseract` over rasterized PDF pages
- Normalization: Unicode cleanup, uppercasing, whitespace compression
- Matching: `rapidfuzz` token/partial ratios + regex format checks (PAN, Aadhaar, dates)
- Orchestration: simple CLI; outputs a single Excel for review

## What to Discuss in Interviews
- How fuzzy scores are composed and why (robust to OCR noise)
- Handling multi‑page PDFs, multiple ID types, missing fields
- Latency/throughput optimizations (parallel OCR, caching)
- Observability: per‑field confidence, error buckets, thresholds by doc type

## How to Run (Local Demo)
```bash
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Put applicant CSVs into data/applicants and PDFs into data/pdfs (sample files provided)
python src/main.py --applicants data/applicants/sample_applicants.csv --pdf_dir data/pdfs --threshold 0.90 --out outputs/report.xlsx
```
The script will OCR the PDFs, compare against typed values, and produce `outputs/report.xlsx` with:
- per‑field scores (0..1)
- overall score (0..1)
- decision: **OK** / **REVIEW**

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

## Notes
- Tesseract system binary should be installed on your OS (Linux: `sudo apt install tesseract-ocr`, Windows: installer).  
- You can tune `FIELD_WEIGHTS` and threshold per your quality needs.
