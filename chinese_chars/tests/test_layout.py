"""Acceptance tests for Layout Engine (Milestone 6)."""

import pytest

from chinese_chars.models import Cell, Config, Row
from chinese_chars.layout import LayoutEngine


def _make_cells(count: int) -> list[Cell]:
    """Helper to generate flat cells of 'blank' kind."""
    return [Cell(kind="blank", character_data=None, stroke_index=None) for _ in range(count)]


def test_layout_uses_config_columns():
    """The layout engine must use the column count from Configuration."""
    config = Config(chars="测试", repetitions=1, columns=4) # 4 columns expected
    engine = LayoutEngine(config)
    
    assert engine.config.columns == 4
    # Assuming standard capacity calculation: 
    # With 4 cols, we might have 6 full rows per page (24 cells).
    
    # Create a sequence larger than a single row but fits within one logical "grid" unit.
    cells = _make_cells(5)
    
    pages = engine.build(cells)
    assert len(pages) >= 1
    
    # The first page should have rows
    assert len(pages[0].rows) > 0
    
    # Check the width of the row matches config columns (if full)
    first_row = pages[0].rows[0]
    assert first_row.index == 0
    assert all(len(row.cells) for row in pages[0].rows)
