"""
PDF Service for parsing slide PDFs into clean Markdown text.
Supports PyMuPDF (fitz) with fallback to pypdf.
"""

from pathlib import Path
from typing import Union


def extract_pdf_to_markdown(pdf_path: Union[str, Path]) -> str:
    """Extract text from a PDF file and format it into Markdown.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Extracted Markdown string representation of the PDF slides.
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    # Try PyMuPDF (fitz)
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(path)
        markdown_pages = []
        for i, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            if text:
                markdown_pages.append(f"## Slide {i}\n\n{text}")
        doc.close()
        if markdown_pages:
            return "\n\n---\n\n".join(markdown_pages)
    except Exception:
        pass

    # Fallback to pypdf
    try:
        from pypdf import PdfReader

        reader = PdfReader(path)
        markdown_pages = []
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            text = text.strip()
            if text:
                markdown_pages.append(f"## Slide {i}\n\n{text}")
        if markdown_pages:
            return "\n\n---\n\n".join(markdown_pages)
    except Exception:
        pass

    return f"# {path.stem}\n\n[Could not extract text content from PDF]"
