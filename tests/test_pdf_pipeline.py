from unittest import result

import pymupdf

from src.resume_processor import process_resume_pdf


def test_process_resume_pdf(tmp_path):

    pdf_path = tmp_path / "Hrishi_ATS2.pdf"

    document = pymupdf.open()
    page = document.new_page()

    page.insert_text(
        (50, 50),
        """
        Python Developer
        Skills: Python, Django, React.js, PostgreSQL, GenAI
        """
    )

    document.save(pdf_path)
    document.close()

    result = process_resume_pdf(str(pdf_path))

    assert result["Programming Languages"] == ["Python"]
    assert result["Backend Development"] == ["Django"]
    assert result["Frontend Development"] == ["React"]
    assert result["Databases and Storage"] == ["PostgreSQL"]
    assert result["Generative AI and LLMs"] == ["Generative AI"]