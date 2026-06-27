"""Tests for Workbook Generator (Milestone 5)."""

from chinese_chars.generator import WorkbookGenerator
from chinese_chars.models import Config


def test_generate_content():
    """Generate Content produces expected char-level cell groups."""
    cfg = Config(chars="一", columns=3)

    gen = WorkbookGenerator()
    cells_list = gen.generate_content(cfg)
    
    # Expectation: one item per char, each being a list of cells (ref + strokes + optional blanks)
    assert len(cells_list) == 1
    assert len(cells_list[0]) > 0
