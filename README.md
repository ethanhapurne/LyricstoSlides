# LyricstoSlides

`LyricstoSlides` is a Python CLI that converts a songbook PDF into projector-ready PowerPoint presentations.

Each PDF page is treated as one song. The tool extracts the page header and lyrics, removes chord-only lines, groups the remaining text into sections, expands chorus repeats, and writes one `.pptx` file per song.

## What It Does

- Reads a PDF with `pdfplumber`
- Treats each page as a separate song
- Uses the first two extracted header lines as page number and song title
- Removes lines that are mostly chord notation
- Detects verse and refrain markers in the lyric body
- Builds slideshow order by reusing the latest detected chorus
- Generates one PowerPoint file per page with a title slide and lyric slides

## Output Format

Generated presentations use a simple worship-slide layout:

- 16:9 slides (`33.87cm x 19.05cm`)
- Black background
- Centered white text
- Automatic font-size reduction to keep lines on screen without wrapping
- `-AMIN-` footer on the final slide

## Installation

The project requires Python 3.11 or newer.

```bash
pip install -e .
```

That installs the package and its dependencies from [pyproject.toml](/Users/ethanhapurne/Documents/Coding/GitHub/LyricstoSlides/pyproject.toml).

## Usage

```bash
lyrics-to-slides path/to/songbook.pdf --output-dir out
```

Optional flags:

- `--output-dir`: destination folder for generated `.pptx` files. Defaults to `out`
- `--verbose`: prints parser warnings for pages with ambiguous formatting

You can also run it directly from source:

```bash
PYTHONPATH=src python3 -m lyrics_to_slides.cli Sample.pdf --output-dir out --verbose
```

On the included sample PDF, the CLI successfully generates a PowerPoint presentation.

## Expected PDF Structure

The current parser works best when each page follows this pattern:

1. First header line: numeric page number
2. Second header line: song title
3. Remaining content: lyrics, ideally grouped into labeled sections

Section markers currently recognized:

- Verse labels that start with a number such as `1`, `2`, or `3:`
- Refrain / chorus labels that start with `R`, such as `R`, `R:`, or `R1`

Chord removal currently happens at the line level: if at least 60% of the tokens on a line look like chord symbols, that full line is removed before section parsing.

## Project Layout

```text
src/lyrics_to_slides/
  __init__.py
  cli.py
  models.py
  pdf_ingest.py
  song_parser.py
  pptx_writer.py
  pipeline.py
```

## Pipeline Overview

- [cli.py](/Users/ethanhapurne/Documents/Coding/GitHub/LyricstoSlides/src/lyrics_to_slides/cli.py): parses arguments and runs the conversion
- [pdf_ingest.py](/Users/ethanhapurne/Documents/Coding/GitHub/LyricstoSlides/src/lyrics_to_slides/pdf_ingest.py): extracts page headers and lyric body text from the PDF
- [song_parser.py](/Users/ethanhapurne/Documents/Coding/GitHub/LyricstoSlides/src/lyrics_to_slides/song_parser.py): removes chord lines, identifies sections, and builds slide order
- [pptx_writer.py](/Users/ethanhapurne/Documents/Coding/GitHub/LyricstoSlides/src/lyrics_to_slides/pptx_writer.py): creates the PowerPoint slides and saves each deck
- [pipeline.py](/Users/ethanhapurne/Documents/Coding/GitHub/LyricstoSlides/src/lyrics_to_slides/pipeline.py): orchestrates the end-to-end run

## Current Notes

- One PDF page becomes one `.pptx` file
- Output files are named from the detected song title
- The parser is format-sensitive and works best with consistent header and section labeling
- Verbose warning output depends on pages being flagged during parsing
