import pymupdf
from pathlib import Path


def extract_text_from_pdf(pdf_path):

    pdf_path = Path(pdf_path)

    # Check whether the PDF exists
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    document = None

    try:
        document = pymupdf.open(pdf_path)

        extracted_text = ""

        for page in document:
            extracted_text += page.get_text()

        extracted_text = extracted_text.strip()

        if not extracted_text:
            raise ValueError("No extractable text found in PDF.")

        return extracted_text

    except Exception as error:
        raise ValueError(f"Unable to process PDF: {error}") from error

    finally:
        if document is not None:
            document.close()