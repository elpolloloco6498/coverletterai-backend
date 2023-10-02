from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph


def text_to_pdf(text):
    # Create a BytesIO buffer to save the PDF
    buffer = BytesIO()

    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Create a list to store the flowables (elements) of the PDF
    elements = []

    # Define a style for the paragraphs
    # styles = getSampleStyleSheet()
    style = ParagraphStyle(name='CustomStyle', fontSize=12)

    # Split the text into paragraphs
    paragraphs = text.split('\n')

    # Create a Paragraph object for each paragraph
    for paragraph in paragraphs:
        p = Paragraph(paragraph, style)
        p.spaceAfter = 8  # Add vertical spacing after each paragraph
        elements.append(p)

    # Build the PDF document
    doc.build(elements)

    # File pointer at the beginning of the buffer
    buffer.seek(0)

    return buffer.getvalue()
