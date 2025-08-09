from rapidfuzz import fuzz
import regex as re
from .utils import normalize_text, sanitize_id, PAN_REGEX, AADHAAR_REGEX, DATE_REGEX

FIELD_WEIGHTS = {
    "name": 0.22,
    "dob": 0.18,
    "pan": 0.20,
    "aadhaar": 0.20,
    "address": 0.15,
    "state": 0.05
}

STATE_ALIASES = {
    # add common abbreviations or spelling variants here if needed
}

def score_name(expected: str, text: str) -> float:
    e = normalize_text(expected)
    t = normalize_text(text)
    return max(
        fuzz.token_set_ratio(e, t) / 100.0,
        fuzz.partial_ratio(e, t) / 100.0
    )

def score_dob(expected: str, text: str) -> float:
    e = normalize_text(expected)
    t = normalize_text(text)
    m = DATE_REGEX.search(t)
    cand = m.group(1) if m else ""
    return max(
        fuzz.partial_ratio(e, cand)/100.0,
        fuzz.partial_ratio(e, t)/100.0
    )

def score_pan(expected: str, text: str) -> float:
    e = sanitize_id(expected)
    t = sanitize_id(text)
    found = PAN_REGEX.search(t)
    cand = found.group(0) if found else ""
    return max(
        fuzz.ratio(e, cand)/100.0,
        fuzz.partial_ratio(e, t)/100.0
    )

def score_aadhaar(expected: str, text: str) -> float:
    e = sanitize_id(expected)
    t = sanitize_id(text)
    # normalize spacing to 4-4-4
    t_spaced = re.sub(r"(\d{4})(\d{4})(\d{4})", r"\1 \2 \3", t)
    found = re.search(r"\b\d{4}\s\d{4}\s\d{4}\b", t_spaced)
    cand = sanitize_id(found.group(0)) if found else ""
    return max(
        fuzz.ratio(e, cand)/100.0,
        fuzz.partial_ratio(e, t)/100.0
    )

def score_address(expected: str, text: str) -> float:
    e = normalize_text(expected)
    t = normalize_text(text)
    return max(
        fuzz.token_set_ratio(e, t) / 100.0,
        fuzz.partial_ratio(e, t) / 100.0
    )

def score_state(expected: str, text: str) -> float:
    e = normalize_text(STATE_ALIASES.get(expected, expected))
    t = normalize_text(text)
    return max(
        fuzz.token_set_ratio(e, t) / 100.0,
        fuzz.partial_ratio(e, t) / 100.0
    )

def compute_overall(scores: dict) -> float:
    total = 0.0
    for k, w in FIELD_WEIGHTS.items():
        total += w * scores.get(k, 0.0)
    return total
