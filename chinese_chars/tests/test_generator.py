"""Acceptance tests for Workbook Generator (Milestone 5)."""

from chinese_chars.models import Config
from chinese_chars.generator import WorkbookGenerator


def test_generate_content():
    """Generate Content produces expected flat sequence."""
    # "一" is a real character in our data/generated/characters directory.
    cfg = Config(chars="一", repetitions=1, columns=3)
    
    gen = WorkbookGenerator()
    cells_list = gen.generate_content(cfg)
    
    # Expectations:
    # 1 Reference Cell
    # 1 Progressive Stroke (1 stroke in "一")
    # 1 blank practice cell (for repetition 1)
    # Total = 3 cells for this one character.
    assert len(cells_list) == 3
    
    assert cells_list[0].kind == 'reference' 
    assert cells_list[1].kind == 'stroke-1'
    assert cells_list[2].kind == 'blank'
