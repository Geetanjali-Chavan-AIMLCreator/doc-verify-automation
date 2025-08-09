import re, unicodedata

PAN_REGEX = re.compile(r"[A-Z]{5}[0-9]{4}[A-Z]")
AADHAAR_REGEX = re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b")
DATE_REGEX = re.compile(r"\b(\d{2,4}[-/](\d{1,2})[-/](\d{1,2}))\b")

def normalize_text(s: str) -> str:
    if s is None:
        return ""
    s = unicodedata.normalize("NFKD", str(s))
    s = s.upper()
    s = re.sub(r"\s+", " ", s).strip()
    return s

def sanitize_id(s: str) -> str:
    if s is None: return ""
    return re.sub(r"\s+", "", s).upper()
