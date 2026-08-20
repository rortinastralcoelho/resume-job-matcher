import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts raw text from a PDF byte stream.
    """
    extracted_text = ""
    try:
        # Open the PDF directly from the uploaded bytes
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                extracted_text += page.get_text("text") + "\n"
    except Exception as e:
        logger.error(f"Failed to process PDF: {e}")
        raise ValueError("Could not extract text from the provided PDF.")

    return extracted_text.strip()