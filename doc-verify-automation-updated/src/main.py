import argparse, os
import pandas as pd
from pathlib import Path
from .extract_ocr import ocr_pdf
from .match_rules import score_name, score_dob, score_pan, score_aadhaar, score_address, score_state, compute_overall

def find_pdf(pdf_dir: Path, application_id: str):
    cand = pdf_dir / f"{application_id}.pdf"
    return cand if cand.exists() else None

def run(applicants_csv: Path, pdf_dir: Path, out_xlsx: Path, threshold: float):
    df = pd.read_csv(applicants_csv)
    rows = []
    for _, r in df.iterrows():
        app_id = str(r.get("application_id", ""))
        pdf_path = find_pdf(pdf_dir, app_id)
        if not pdf_path:
            rows.append({"application_id": app_id, "status": "MISSING_PDF"})
            continue
        text = ocr_pdf(str(pdf_path))

        scores = {}
        scores["name"] = score_name(r.get("name", ""), text)
        scores["dob"] = score_dob(str(r.get("dob", "")), text)
        scores["pan"] = score_pan(str(r.get("pan", "")), text)
        scores["aadhaar"] = score_aadhaar(str(r.get("aadhaar", "")), text)
        scores["address"] = score_address(str(r.get("address", "")), text)
        scores["state"] = score_state(str(r.get("state", "")), text)

        overall = compute_overall(scores)
        decision = "OK" if overall >= threshold else "REVIEW"
        row = {"application_id": app_id, **scores, "overall": overall, "decision": decision}
        rows.append(row)

    out_df = pd.DataFrame(rows)
    out_df.to_excel(out_xlsx, index=False)
    print(f"Wrote report: {out_xlsx}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--applicants", required=True, help="CSV with columns: application_id,name,address,state,aadhaar,pan,dob")
    p.add_argument("--pdf_dir", required=True, help="Folder containing <application_id>.pdf files")
    p.add_argument("--threshold", type=float, default=0.90)
    p.add_argument("--out", default="outputs/report.xlsx")
    args = p.parse_args()
    run(Path(args.applicants), Path(args.pdf_dir), Path(args.out), args.threshold)
