"""Command-line interface for LyricstoSlides."""

from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import run_conversion


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser for the application.

    Returns:
        argparse.ArgumentParser: The parser configured with the supported CLI
            arguments and flags.
    """

    parser = argparse.ArgumentParser(
        prog="lyrics-to-slides",
        description="Convert a PDF songbook into one PowerPoint file per page.",
    )
    parser.add_argument("input_pdf", type=Path, help="Path to the input PDF file.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("out"),
        help="Directory for generated PowerPoint files.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print additional conversion diagnostics.",
    )
    return parser


def main() -> int:
    """Run the CLI entry point.

    Implementation:
    - parse command-line arguments
    - call the conversion pipeline
    - optionally print page warnings in verbose mode
    - report how many presentations were generated

    Returns:
        int: Process exit status code, where `0` means success.
    """

    parser = build_parser()
    args = parser.parse_args()

    result = run_conversion(args.input_pdf, args.output_dir)

    if args.verbose:
        for page_number, warnings in result.warnings_by_song.items():
            for warning in warnings:
                print(f"[page {page_number}] {warning}")

    print(f"Generated {len(result.output_files)} presentation(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
