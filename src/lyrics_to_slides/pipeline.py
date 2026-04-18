"""End-to-end conversion orchestration."""

from __future__ import annotations

from pathlib import Path

from .models import ConversionResult

from lyrics_to_slides.pdf_ingest import *
from lyrics_to_slides.pptx_writer import *
from lyrics_to_slides.song_parser import *



def run_conversion(pdf_path: Path, output_dir: Path) -> ConversionResult:
    """Convert an input PDF into one PowerPoint file per page.

    Implementation:
    - extract raw page text from the PDF
    - parse each page into song metadata and sections
    - build slide sequences
    - generate one `.pptx` file per page
    - collect warnings in the final run summary

    Args:
        pdf_path (Path): The source PDF containing one song per page.
        output_dir (Path): The directory where generated PowerPoint files
            should be written.

    Returns:
        ConversionResult: A summary of created output files and page warnings.
    """
    results = ConversionResult(
        output_files = [],
        warnings_by_song = {}

    )

    raw_text = extract_pages(pdf_path)
    for lyrics in raw_text:
        song = parse_song_page(lyrics)
        pptx = build_slide_sequence(song)
        powerpoint_path = write_presentation(output_dir, pptx)
        
        # Return call
        results.output_files.append(powerpoint_path)
        if song.warning:
            results.warnings_by_song[song.page_number] = True

    return results
