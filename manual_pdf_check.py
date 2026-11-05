from src.resume_parser import extract_text_from_pdf

text = extract_text_from_pdf("Hrishi_ATS2.pdf")

print("Extracted Resume Text:")
print(text)