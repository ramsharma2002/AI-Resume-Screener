import pdfplumber
import docx2txt

def extract_text(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text() + " "
    elif file_path.endswith(".docx"):
        text = docx2txt.process(file_path)
    return " ".join(text.lower().split())
