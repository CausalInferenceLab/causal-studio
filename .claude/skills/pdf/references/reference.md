# PDF Advanced Reference

## pypdfium2 — High-Performance Rendering

```python
import pypdfium2 as pdfium

pdf = pdfium.PdfDocument("document.pdf")

# Render page to image
page = pdf[0]
bitmap = page.render(scale=2)  # 2x scale = 144 DPI
pil_image = bitmap.to_pil()
pil_image.save("page_1.png")

# Extract text with coordinates
textpage = page.get_textpage()
for i in range(textpage.count_chars()):
    char = textpage.get_charbox(i)
    print(f"Char: {textpage.get_text_range(i, 1)}, Box: {char}")

pdf.close()
```

**When to prefer pypdfium2**: High-quality image rendering, pixel-accurate text extraction, processing large batches.

---

## pdf-lib (JavaScript)

```javascript
import { PDFDocument, rgb, StandardFonts } from 'pdf-lib';
import fs from 'fs';

// Load and modify
const pdfBytes = fs.readFileSync('input.pdf');
const pdfDoc = await PDFDocument.load(pdfBytes);

const page = pdfDoc.getPages()[0];
const font = await pdfDoc.embedFont(StandardFonts.Helvetica);
page.drawText('Hello World', { x: 50, y: 700, size: 20, font, color: rgb(0, 0, 0) });

const output = await pdfDoc.save();
fs.writeFileSync('output.pdf', output);
```

**When to use**: Node.js environments, browser-side PDF generation.

---

## Batch Processing

```python
import os
from pathlib import Path
from pypdf import PdfReader
import logging

logging.basicConfig(level=logging.INFO)

def process_pdfs(input_dir: str, output_dir: str):
    Path(output_dir).mkdir(exist_ok=True)
    errors = []
    
    for pdf_file in Path(input_dir).glob("*.pdf"):
        try:
            reader = PdfReader(str(pdf_file))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            
            out_path = Path(output_dir) / (pdf_file.stem + ".txt")
            out_path.write_text(text, encoding="utf-8")
            logging.info(f"Processed: {pdf_file.name}")
        except Exception as e:
            logging.error(f"Failed: {pdf_file.name} — {e}")
            errors.append((str(pdf_file), str(e)))
    
    return errors
```

---

## Memory-Efficient Large File Processing

```python
import pdfplumber

def stream_text(pdf_path: str):
    """Yield text page by page to avoid loading entire PDF into memory."""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            yield i + 1, page.extract_text() or ""

for page_num, text in stream_text("large_document.pdf"):
    print(f"--- Page {page_num} ---")
    print(text)
```

---

## Handling Encrypted / Corrupted PDFs

```python
from pypdf import PdfReader

# Encrypted PDF
reader = PdfReader("encrypted.pdf")
if reader.is_encrypted:
    reader.decrypt("password")

# Corrupted PDF — try qpdf first
import subprocess
result = subprocess.run(
    ["qpdf", "--recover", "corrupted.pdf", "repaired.pdf"],
    capture_output=True, text=True
)
if result.returncode != 0:
    print("qpdf repair failed:", result.stderr)
```

---

## OCR Fallback for Mixed PDFs

```python
import pdfplumber
import pytesseract
from pdf2image import convert_from_path

def extract_with_ocr_fallback(pdf_path: str) -> list[str]:
    """Use pdfplumber first; fall back to OCR if page has no text."""
    pages_text = []
    images = None  # lazy-load

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and text.strip():
                pages_text.append(text)
            else:
                if images is None:
                    images = convert_from_path(pdf_path, dpi=200)
                pages_text.append(pytesseract.image_to_string(images[i]))

    return pages_text
```

---

## Tool Selection Guide

| Use case | Recommended tool |
|----------|-----------------|
| Simple text extraction | pdfplumber |
| Tables | pdfplumber |
| High-quality image rendering | pypdfium2 |
| Merge / split / rotate | pypdf |
| Create new PDFs | reportlab |
| JavaScript / browser | pdf-lib |
| CLI text extraction | pdftotext (poppler) |
| CLI manipulation | qpdf |
| OCR | pytesseract + pdf2image |
| Repair corrupted | qpdf --recover |

## Library Licenses

| Library | License |
|---------|---------|
| pypdf | BSD |
| pdfplumber | MIT |
| reportlab | BSD |
| pypdfium2 | Apache 2.0 |
| pdf-lib | MIT |
| poppler-utils | GPL-2 |
| qpdf | Apache 2.0 |
