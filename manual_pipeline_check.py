from src.resume_processor import process_resume_pdf

result = process_resume_pdf("Hrishi_ATS2.pdf")

print("\nExtracted Skills:")

for category, skills in result.items():

    print(f"\n{category}:")

    for skill in skills:
        print("-", skill)