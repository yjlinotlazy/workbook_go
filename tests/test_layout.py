"""Acceptance tests for Layout Engine (Milestone 6)."""

import pytest

from chinese_chars.models import Cell, Config, Row
from chinese_chars.layout import LayoutEngine


def _make_cells(count: int) -> list[Cell]:
    """Helper to generate flat cells of 'blank' kind."""
    return [Cell(kind="blank", character_data=None, stroke_index=None) for _ in range(count)]


def test_layout_uses_config_columns():
    """The layout engine must use the column count from Configuration."""
    config = Config(chars="测试", columns=4)  # 4 columns expected
    
    assert config.columns == 4

    cells_per_page = config.columns * 6  # Assuming 6 rows per page (standard for US Letter)
    cells = _make_cells(24)

    pages = engine.build(cells)
    assert len(pages) >= 1

    first_row = pages.pages[0].rows[0]
    assert all(len(cells) == config.columns for row in pages.pages[0].rows for cells in [row])


def test_layout_empty_input():
    """Empty character list should produce zero pages."""
    config = Config(chars="", columns=4)
    engine = LayoutEngine(config)

    pages = engine.build([])
    assert len(pages) == 0


def test_character_boundary_preservation():
    """After padding and flattening, each character's cells occupy full columns."""
    config = Config(chars="一二", columns=3)
    engine = LayoutEngine(config)

    char_cells = [
        _make_cells(2),  # Character 1: 2 cells (needs 1 blank)
        _make_cells(2),  # Character 2: 2 cells (needs 1 blank)
    ]

    pages = engine.build(char_cells)
    
    # Total cells should be 3*6=18, with each char padded to 3 columns 
    assert len(pages) >= 1
    total_cells = sum(1 for row in pages.pages[0].rows for cell in row.cells)
    assert total_cells == config.columns * 2

def test_multiple_pages():
    """Many characters should create multiple pages."""
    large_config = Config(chars="一二三", columns=4)
    engine = LayoutEngine(large_config)

    rows_per_page = large_paper_rows()
    pages_per_word = (18 + rows_per_page - 1) // rows_per_page
    
    char_cells = _make_cells([_make_cells(5)] * 30)  # 30 characters with 5 cells each

    pages = engine.build(char_cells)
    
    assert len(pages) == pages_per_word


def large_paper_rows() -> int:
    """Return expected rows per page for standard paper."""
    return 6

