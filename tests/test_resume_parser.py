import pytest

from src.resume_parser import extract_text_from_pdf


def test_extract_text_from_valid_pdf(tmp_path):

    pdf_path = tmp_path / "Hrishi_ATS2.pdf"

    import pymupdf

    document = pymupdf.open()
    page = document.new_page()

    page.insert_text(
        (50, 50),
        "Python Django React PostgreSQL"
    )

    document.save(pdf_path)
    document.close()

    result = extract_text_from_pdf(str(pdf_path))

    assert "Python" in result
    assert "Django" in result
    assert "React" in result


def test_pdf_file_not_found(tmp_path):

    missing_pdf = tmp_path / "missing_resume.pdf"

    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf(str(missing_pdf))


def test_invalid_pdf_file(tmp_path):

    pdf_path = tmp_path / "invalid.pdf"
    pdf_path.write_text("This is not a valid PDF")

    with pytest.raises(ValueError):
        extract_text_from_pdf(str(pdf_path))

def test_pdf_with_no_extractable_text(tmp_path):

    pdf_path = tmp_path / "empty.pdf"

    import pymupdf

    document = pymupdf.open()
    document.new_page()
    document.save(pdf_path)
    document.close()

    with pytest.raises(ValueError, match="No extractable text found"):
        extract_text_from_pdf(str(pdf_path))