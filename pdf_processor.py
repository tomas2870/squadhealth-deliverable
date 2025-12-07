from pdf2image import convert_from_path
import pytesseract


def pdf_to_images(pdf_path, dpi=300):
    """
    Convert PDF to images.
    
    Args:
        pdf_path: Path to PDF file
        dpi: Resolution for conversion
        
    Returns:
        List of PIL Image objects
    """
    return convert_from_path(pdf_path, dpi=dpi)


def images_to_text(images, lang="eng"):
    """
    Extract text from images using OCR.
    
    Args:
        images: List of PIL Image objects
        lang: Tesseract language code
        
    Returns:
        Concatenated text from all images
    """
    pages_text = []
    
    for img in images:
        text = pytesseract.image_to_string(img, lang=lang)
        pages_text.append(text)
    
    return "\n".join(pages_text)


def extract_text_from_pdf(pdf_path, dpi=300, lang="eng"):
    """
    Extract text from a PDF using OCR.
    
    Args:
        pdf_path: Path to PDF file
        dpi: Resolution for conversion
        lang: Tesseract language code
        
    Returns:
        Extracted text string
    """
    images = pdf_to_images(pdf_path, dpi=dpi)
    text = images_to_text(images, lang=lang)
    return text