from PyPDF2 import PdfReader


def extract_text_from_pdf(byte_file):
    reader = PdfReader(byte_file)
    page = reader.pages[0]
    return page.extract_text()
