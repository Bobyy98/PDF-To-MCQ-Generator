# text.py

import PyPDF2
import random

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            page_text = page.extract_text().splitlines()
            text += "\n".join([line for line in page_text if line and line[0].isalpha()])
    return text

def select_text_from_pdf(pdf_path, batch_size=10000, num_batches=2):
    pdf_text = extract_text_from_pdf(pdf_path)
    total_length = len(pdf_text)

    if total_length < batch_size * num_batches:
        return pdf_text

    selected_text = ""
    for _ in range(num_batches):
        start = random.randint(0, total_length - batch_size)
        selected_text += pdf_text[start:start + batch_size]

    return selected_text
