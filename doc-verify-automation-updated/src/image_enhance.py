import cv2
import numpy as np

def enhance_for_ocr(bgr):
    # 1) grayscale
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    # 2) denoise (bilateral filter keeps edges)
    den = cv2.bilateralFilter(gray, d=7, sigmaColor=50, sigmaSpace=50)
    # 3) unsharp mask
    blur = cv2.GaussianBlur(den, (0,0), 2.0)
    usm = cv2.addWeighted(den, 1.7, blur, -0.7, 0)
    # 4) CLAHE contrast
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    con = clahe.apply(usm)
    # 5) adaptive threshold (binary)
    thr = cv2.adaptiveThreshold(con, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 35, 11)
    return thr
