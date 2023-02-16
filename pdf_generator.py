from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_pdf(text):
    c = canvas.Canvas("advertisement.pdf", pagesize=letter)
    c.drawString(100, 750, text)
    c.save()
    return "advertisement.pdf"
