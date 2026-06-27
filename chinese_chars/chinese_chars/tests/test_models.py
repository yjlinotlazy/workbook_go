"""Tests for data model."""

from chinese_chars.models import Cell, Config, Row, Page, Workbook


def test_construct_minimal_workbook():
    """Build a minimal workbook without any I/O."""
    row = Row(index=0, cells=tuple())  # empty row
    p = Page(number=1, rows=(row,), width_cells=3)
    
    config = Config(chars="一二")
    wb = Workbook(
        title="Minimal",
        config=config,
        pages=(p,)
    )
    
    assert wb.title == "Minimal"
    assert len(wb.pages) == 1

def test_config_defaults():
    """Config should have correct default values."""
    config = Config(chars="test")
    
    assert config.chars == "test"
    assert config.columns == 3
    assert config.paper_size == "us_letter"
    assert config.font_size == 48
