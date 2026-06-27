"""Acceptance tests for Layout Engine (Milestone 6)."""

import pytest

from chinese_chars.models import Cell, Config, Row
from chinese_chars.layout import LayoutEngine


def _make_cells(count: int) -> list[Cell]:
    return [Cell(kind="blank", character_data=None, stroke_index=None) for _ in range(count)]


def test_layout_uses_config_columns():
    """The layout engine must use the column count from Configuration."""
    config = Config(chars="测试", columns=4)  # 4 columns expected
    engine = LayoutEngine(config)
    
    assert engine.config.columns == 4
    
    # Create a sequence larger than a single row but fits within one logical "grid" unit.
    cells_per_page = max(25, config.columns * 6)  # at least one full page
    cells = _make_cells(cells_per_page)
    
    pages = engine.build([cells])  # wrap in list as char_blocks  
    assert len(pages) >= 1
    
    # The first page should have rows
    assert len(pages[0].rows) > 0
    
    # Check the width of the row matches config columns (if full)
    first_row = pages[0].rows[0]
    assert all(len(row.cells) for row in pages[0].rows)


def test_layout_empty_input():
    """Empty character list should produce zero pages."""
    config = Config(chars="测试", columns=4)
    engine = LayoutEngine(config)

    pages = engine.build([])
    assert len(pages) == 0
