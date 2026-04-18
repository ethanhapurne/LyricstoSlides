"""Domain models for PDF-to-PowerPoint conversion."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SongSection:
    """Store one parsed section of a song.

    A song section represents one logical lyric block such as a verse,
    chorus, bridge, intro, or outro. The parser should populate this model
    after deciding the section type and collecting the lyric lines that belong
    to that section.

    Args:
        type (str): The normalized section type, such as `verse`, `chorus`,
            `bridge`, or `intro`.
        label (str): The original or display label for the section, such as
            `Verse 1` or `Chorus`.
        lines (list[str]): The lyric lines that belong to this section.
    """

    type: str
    label: str
    lines: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Slideshow:
    """Store the content needed to build one PowerPoint slideshow.

    This model is the handoff between song parsing and PowerPoint generation.
    Each instance should contain the slide title and the lyric lines that will
    appear on that slide in the final presentation.

    Args:
        title (str): The title to display for the slideshow.
        body_sections (list[str]): The content that should appear in the
            body of each slide.
    """

    title: str
    body_sections: list[SongSection] = field(default_factory=list)



@dataclass(slots=True)
class SongPage:
    """Store the parsed result for one PDF page.

    Each page in the source PDF is treated as one song. This model should hold
    the original extracted text, the cleaned lyric lines, the detected song
    sections, and any warnings raised while parsing ambiguous content.

    Args:
        title (str): The detected song title for the page.
        page_number (int): The 1-based page number from the source PDF.
        raw_text (str): The original raw text extracted from the PDF page.
        cleaned_lines (list[str]): The lyric lines after cleanup, such as chord
            removal and whitespace normalization.
        sections (list[SongSection]): The parsed song sections in source order.
        warning (bool): Indicates whether the parser found ambiguous or
            potentially malformed content on the page.
    """

    title: str
    page_number: int
    raw_text: str
    cleaned_lines: list[str] = field(default_factory=list)
    sections: list[SongSection] = field(default_factory=list)
    warning: bool = False


@dataclass(slots=True)
class ConversionResult:
    """Store the final summary of a conversion run.

    After the pipeline processes the input PDF, this model should report which
    PowerPoint files were created and which pages produced warnings that may
    need manual review.

    Args:
        output_files (list[str]): The list of generated PowerPoint file paths.
        warnings_by_song (dict[int, list[str]]): Mapping of page numbers to the
            warnings collected while processing those pages.
    """

    output_files: list[str] = field(default_factory=list)
    warnings_by_song: dict[int, bool] = field(default_factory=dict)
