from PyPDF2 import PdfReader
import os


def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        print(f"🤓 Reading {len(reader.pages)} page/s")
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

if __name__ == "__main__":
    print("PDF Parser Test")
    print("=" * 50)

    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(script_dir, "test.pdf")

    syllabus_text = extract_text_from_pdf(pdf_path)

    print("Extracted Text:")
    print(syllabus_text)
    print("\n " + "=" * 50)
    print(f"Total Characters Extracted: {len(syllabus_text)}")
    print("Test Completed")
