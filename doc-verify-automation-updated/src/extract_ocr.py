from pypdf import PdfReader
from PIL import Image, ImageDraw
import pytesseract
import numpy as np
import io
import cv2

from .image_enhance import enhance_for_ocr

def pdf_to_images_simple(pdf_path: str):
    # Convert each PDF page's text to an image (demo fallback for public repo).
    reader = PdfReader(pdf_path)
    images = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        if not txt.strip():
            continue
        img = Image.new("RGB", (1700, 2200), "white")
        draw = ImageDraw.Draw(img)
        draw.multiline_text((50, 50), txt, fill="black")
        images.append(img)
    return images

def ocr_pdf(pdf_path: str) -> str:
    pages = pdf_to_images_simple(pdf_path)
    texts = []
    for pil_img in pages:
        # -> BGR np array
        bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        enh = enhance_for_ocr(bgr)
        pil_enh = Image.fromarray(enh)
        text = pytesseract.image_to_string(pil_enh)
        texts.append(text)
    return "\n".join(texts)
