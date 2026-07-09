"""Acceptance tests for Layout Engine (Milestone 6)."""

import pytest
from chinese_chars.models import Cell, Config, Row
from chinese_chars.layout import LayoutEngine


def _make_cells(count: int) -> list[Cell]:
    return [Cell(kind="blank", character_data=None, stroke_index=None) for _ in range(count)]


def test_layout_uses_config_columns():
    config = Config(chars="测试", columns=4)  # no repetitions
    engine = LayoutEngine(config)

    assert engine.config.columns == 4
    
    cells_per_page = max(25, config.columns * 6)
    raw_cells = _make_cells(cells_per_page)
    
    # build() expects list[list[Cell]] — wrap in outer list as a single character block 
    pages = engine.build([raw_cells])  # Pages is tuple[Page]
    assert len(pages) >= 1
    
    # Check first page's rows
    assert len(pages[0].rows) > 0
    
    # All rows should have at least one cell
    first_row = pages[0].rows[0]
    assert all(len(row.cells) for row in pages[0].rows)


def test_layout_empty_input():
    config = Config(chars="测试", columns=4)
    engine = LayoutEngine(config)

    pages = engine.build([])
    assert len(pages) == 0


def test_layout_overflow_rows_start_new_page_without_loopback():
    config = Config(chars="测试", columns=5)
    engine = LayoutEngine(config)

    char_blocks = [_make_cells(config.columns) for _ in range(engine.rows_per_page + 1)]
    pages = engine.build(char_blocks)

    assert len(pages) == 2
    assert len(pages[0].rows) == engine.rows_per_page
    assert len(pages[1].rows) == 1

    first_page_y_values = [row.cells[0].geometry.y for row in pages[0].rows]
    assert len(first_page_y_values) == len(set(first_page_y_values))

    assert pages[0].rows[0].cells[0].geometry.y == engine.margin
    assert pages[1].rows[0].cells[0].geometry.y == engine.margin
