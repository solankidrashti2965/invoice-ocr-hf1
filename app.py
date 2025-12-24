import pytesseract
from PIL import Image
import gradio as gr
import re

# Linux path for Tesseract (Hugging Face)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def extract_invoice(image):
    text = pytesseract.image_to_string(image)

    invoice_no = re.search(r'Invoice\s*#?\s*(\d+)', text)
    total = re.search(r'Total\s*\$?([\d,.]+)', text)

    return {
        "invoice_number": invoice_no.group(1) if invoice_no else "Not found",
        "total_amount": total.group(1) if total else "Not found",
        "raw_text": text
    }

iface = gr.Interface(
    fn=extract_invoice,
    inputs=gr.Image(type="pil", label="Upload Invoice Image"),
    outputs=gr.JSON(label="Extracted Invoice Data"),
    title="Invoice OCR Automation",
    description="Upload an invoice image to extract invoice number and total amount"
)

iface.launch()
