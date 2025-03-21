import pdfplumber 
import spacy

def extract_text_ftom_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    return text.strip()

path = "random.pdf"
print(extract_text_ftom_pdf(path))