"""Workbook data model — renderer-independent structures."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CellGeometry:
    """Bounding box coordinates for a cell in PDF points."""
    x: float
    y: float  
    w: float
    h: float


@dataclass(frozen=True)
class Config:
    """Generator configuration for workbook creation."""

    chars: str  # characters to practice, e.g. "一二三"
    repetitions: int  # number of practice rows per character
    columns: int = 3  # cells per row on the page
    paper_size: str = "us_letter"  # paper format ("a4" | "us_letter")
    font_size: int = 48  # reference character font size in pt


@dataclass(frozen=True)
class StrokePoint:
    """A single point in a stroke path."""

    t: float  # normalized progression along the stroke [0, 1]
    x: float
    y: float


@dataclass(frozen=True)
class Stroke:
    """A single brush stroke of one character."""

    points: list[StrokePoint]  # ordered path


@dataclass(frozen=True)
class CharacterData:
    """Metadata + stroke list for one Chinese character."""

    char: str  # the Unicode character, e.g. "永"
    strokes: list[Stroke]  # ordered strokes


@dataclass(frozen=True)
class Cell:
    """One grid cell on a page."""

    kind: str  # "reference" | "stroke-N" | "blank"
    character_data: CharacterData | None  # only for reference / stroke cells
    stroke_index: int | None = None  # N for "stroke-N" cells
    geometry: CellGeometry | None = None  # geometric metadata attached during layout


@dataclass(frozen=True)
class Row:
    """A horizontal list of cells."""

    index: int  # row number
    cells: tuple[Cell, ...]  # fixed-length tuple per row


@dataclass(frozen=True)
class Page:
    """One printable worksheet page."""

    number: int  # 1-based page number
    rows: tuple[Row, ...]  # grid of cells
    width_cells: int  # columns on this page


@dataclass(frozen=True)
class Workbook:
    """Top-level workbook — ordered sequence of pages."""

    title: str  # document title
    config: Config  # generator settings used
    pages: tuple[Page, ...]  # all pages in order
