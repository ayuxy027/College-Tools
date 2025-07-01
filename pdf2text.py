"""pdf2text.py
A simple command-line utility to extract all textual content from one or more
PDF documents.

Example
-------
Extract text from a single PDF and print to stdout::

    python pdf2text.py /path/to/document.pdf

Extract text and write it to a file with the same base name::

    python pdf2text.py /path/to/document.pdf --save

Specify an explicit output path::

    python pdf2text.py /path/to/document.pdf output.txt

Process multiple PDFs at once::

    python pdf2text.py doc1.pdf doc2.pdf --save

Requirements
------------
This script depends on the ``PyPDF2`` package::

    pip install PyPDF2

``PyPDF2`` offers a straightforward text extraction API that works for the
majority of PDFs. If you need more advanced layout preservation consider
replacing it with ``pdfminer.six`` or ``PyMuPDF``.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Return all text found in *pdf_path*.

    Parameters
    ----------
    pdf_path : pathlib.Path
        Path to the PDF document.

    Returns
    -------
    str
        Concatenated text from every page in reading order.
    """
    reader = PdfReader(str(pdf_path))
    texts = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(texts)


def save_text(text: str, output_path: Path) -> None:
    """Write *text* to *output_path*, creating parent directories if necessary."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")


def _parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract plain text from PDF files and write them as .txt files next to the originals.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "input",
        nargs="+",
        type=Path,
        help="Path(s) to input PDF file(s).",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Also print extracted text to stdout (in addition to saving).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = _parse_arguments(argv)

    multiple_inputs = len(args.input) > 1

    for pdf_path in args.input:
        if not pdf_path.exists():
            print(f"❌ File not found: {pdf_path}", file=sys.stderr)
            continue
        if pdf_path.suffix.lower() != ".pdf":
            print(f"⚠️  Skipping non-PDF file: {pdf_path}", file=sys.stderr)
            continue

        try:
            text = extract_text_from_pdf(pdf_path)
        except Exception as exc:
            print(f"❌ Failed to read {pdf_path}: {exc}", file=sys.stderr)
            continue

        # Always save to .txt next to the PDF
        out_path = pdf_path.with_suffix(".txt")
        try:
            save_text(text, out_path)
            print(f"✅ Extracted text saved to {out_path}")
        except Exception as exc:
            print(f"❌ Could not write to {out_path}: {exc}", file=sys.stderr)

        # Optionally print to stdout
        if args.stdout:
            if multiple_inputs:
                banner = f"\n{'='*10} {pdf_path.name} {'='*10}\n"
                sys.stdout.write(banner)
            sys.stdout.write(text + "\n")


if __name__ == "__main__":
    main() 