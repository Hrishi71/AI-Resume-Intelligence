from src.text_cleaner import clean_resume_text


def test_remove_extra_spaces():
    text = "Python     Django    React"
    result = clean_resume_text(text)

    assert result == "Python Django React"


def test_remove_newlines():
    text = "Python\nDjango\nReact"
    result = clean_resume_text(text)

    assert result == "Python Django React"


def test_remove_leading_and_trailing_spaces():
    text = "   Python Django   "
    result = clean_resume_text(text)

    assert result == "Python Django"


def test_empty_string():
    text = ""
    result = clean_resume_text(text)

    assert result == ""