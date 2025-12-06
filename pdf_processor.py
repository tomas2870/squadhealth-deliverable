# pdf_processor.py

import os
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

def pdf_to_images(pdf_path: str, dpi: int = 300):
    # poppler_path is optional if poppler is on PATH; otherwise you can pass it explicitly
    images = convert_from_path(pdf_path, dpi=dpi)
    return images

def images_to_text(images, lang):
    pages_text = []

    for img in images:
        text = pytesseract.image_to_string(img, lang=lang)
        pages_text.append(text)

    full_text = "".join(pages_text)
    return full_text


def extract_text_from_pdf(pdf_path, dpi: int = 300, lang: str = "eng"):
    images = pdf_to_images(pdf_path, dpi=dpi)
    text = images_to_text(images, lang=lang)
    print(text)
    return text