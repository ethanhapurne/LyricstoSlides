"""Song parsing boundaries for lyric cleanup and section ordering."""

from __future__ import annotations

from .models import Slideshow, SongPage, SongSection

import re


def parse_song_page(raw_text: str) -> SongPage:
    """Parse one PDF page into a structured song representation.

    Implementation:
    - detect a likely title
    - remove standalone and inline chord notation
    - split content into labeled or unlabeled sections
    - attach parser warnings for ambiguous cases

    Args:
        raw_text (str): The raw text extracted from one PDF page.

    Returns:
        song (SongPage): The finalized structured representation of the song.
    """
    lines = raw_text.split("\n")
    cleaned_lines = []
    lyric_lines = lines[2:]

    # Removing chord lines
    for line in lyric_lines:
        if not is_chord_line(line):
            cleaned_lines.append(line)

    sections, warning = section_lines(cleaned_lines)

    song = SongPage(
        title="",
        page_number=0,
        raw_text="",
    )
    song.title = lines[1]           # title is second line
    song.page_number = int(lines[0])     # page number is first line
    song.raw_text = raw_text
    song.cleaned_lines = cleaned_lines
    song.sections = sections
    song.warning = warning

    return song


def build_slide_sequence(song_page: SongPage) -> Slideshow:
    """Expand parsed sections into slideshow order.

    Implementation:
    - add verse slides in natural order
    - repeat a labeled chorus or refrain after each verse
    - keep non-repeated sections in source order

    Args:
        song_page (SongPage): The parsed song data for one PDF page.

    Returns:
        slides (Slideshow): The ordered slides that should appear in the
            generated PowerPoint deck.
    """
    slides = Slideshow(
        title = song_page.title,
        body_sections = []
    )
    curr_chorus = None
    chorus_pattern = r"^chorus(\d*)$"

    for section in song_page.sections:
        match = re.match(chorus_pattern, section.type)

        # Updating the current chorus
        if match:
            curr_chorus = section

        # Adds the current verse to the 
        else:
            if curr_chorus is not None:
                slides.body_sections.append(curr_chorus)

            slides.body_sections.append(section)

    if curr_chorus is not None:
        slides.body_sections.append(curr_chorus)

    return slides





def section_lines(cleaned_lines) -> tuple[list[SongSection], bool]:
    """Split cleaned lyric lines into song sections.

    Implementation:
    - scan through the cleaned lyric lines in source order
    - detect section markers such as verse or chorus labels
    - group following lyric lines into the active section
    - flag a warning if the content cannot be sectioned cleanly

    Args:
        cleaned_lines (list[str]): The lyric lines after chord removal.

    Returns:
        tuple[list[SongSection], bool]: The parsed list of song sections and a
            warning flag indicating whether ambiguous formatting was found.
    """
    warning = False
    sections = []
    section_pattern = r"^(?:(\d+)(?:[.:])?|(R(\d*)(?::)?))(?=\s|$)"
    curr_section = None


    for line in cleaned_lines:
        # Checking if the line is the start of a new section
        match = re.match(section_pattern, line)
        if match:
            if curr_section is not None:
                sections.append(curr_section)

            verse_num = match.group(1)
            chorus_full = match.group(2)
            chorus_num = match.group(3)
            
            if verse_num:
                curr_section = SongSection(
                    type="verse",
                    label=verse_num,
                    lines=[],
                )
            
            else:
                curr_section = SongSection(
                    type=f"chorus{chorus_num}" if chorus_num else "chorus",
                    label=chorus_full,
                    lines=[],
                )

        if curr_section is None:
            warning = True
            continue

        curr_section.lines.append(line)

        # Checking if to raise an error
        if not match and len(curr_section.lines) == 1:
            warning = True

    if curr_section is not None:
        sections.append(curr_section)

    return sections, warning


def is_chord_token(token: str) -> bool:
    """Check whether a single token matches the expected chord pattern.

    Args:
        token (str): One whitespace-delimited token from a lyric line.

    Returns:
        bool: `True` when the token looks like a musical chord, otherwise
            `False`.
    """

    token = token.strip()
    if not token:
        return False
    return CHORD_PATTERN.match(token) is not None


def is_chord_line(line: str) -> bool:
    """Check whether most of a line is made up of chord tokens.

    Args:
        line (str): One line from the raw or cleaned song text.

    Returns:
        bool: `True` when the line is mostly chord notation, otherwise `False`.
    """

    tokens = line.split()
    if not tokens:
        return False
    
    chord_count = sum(is_chord_token(t) for t in tokens)
    return chord_count / len(tokens) >= 0.6  # threshold


CHORD_PATTERN = re.compile(
    r"^[A-G]"          # root note
    r"(#|b)?"          # optional sharp/flat
    r"(m|maj|min|dim|aug|sus|add)?"  # optional quality
    r"(\d+)?"          # optional number like 7, 9
    r"(/[A-G](#|b)?)?$"  # optional slash chord
)
