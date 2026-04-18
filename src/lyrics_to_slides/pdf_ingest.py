"""PDF ingestion boundaries."""

from __future__ import annotations

from pathlib import Path

import pdfplumber


def _split_nonempty_lines(text: str | None) -> list[str]:
    """Return stripped non-empty lines from extracted PDF text."""
    if not text:
        return []

    return [line.strip() for line in text.splitlines() if line.strip()]


def _extract_header_lines(page: pdfplumber.page.Page) -> list[str]:
    """Return the page number and title lines for a PDF page."""
    width, height = page.width, page.height
    title_crop = page.crop((0, 0, width, height * 0.10))

    header_lines = _split_nonempty_lines(title_crop.extract_text())
    if len(header_lines) >= 2:
        return header_lines[:2]

    full_lines = _split_nonempty_lines(page.extract_text())
    return full_lines[:2]


def _extract_body_text(page: pdfplumber.page.Page) -> str:
    """Return the lyric body from the table region or full page text."""
    tables = page.extract_tables()
    if tables and tables[0] and tables[0][0]:
        first_cell = tables[0][0]
        if isinstance(first_cell, list):
            return "\n".join(first_cell)
        if isinstance(first_cell, str):
            return first_cell

    full_lines = _split_nonempty_lines(page.extract_text())
    return "\n".join(full_lines[2:])


def extract_pages(pdf_path: Path) -> list[str]:
    """Return raw text for each page in the input PDF.

    Implementation:
    - open the PDF file and iterate through its pages in order
    - extract the title and lyric content for each page
    - combine the page content into one raw text block per page
    - return a list where each item represents one song/page

    Args:
        pdf_path (Path): The path to the input PDF file.

    Returns:
        lyrics_list (list[str]): A list of raw page strings, with one item
            for each page in the PDF.
    """
    lyrics_list = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            header_lines = _extract_header_lines(page)
            table_text = _extract_body_text(page)

            # Adding the combination to the lyrics_list
            lyrics_parts = [*header_lines]
            if table_text:
                lyrics_parts.append(table_text)
            lyrics = "\n".join(lyrics_parts)
            lyrics_list.append(lyrics)

    return lyrics_list

#extract_pages("Sample.pdf")
