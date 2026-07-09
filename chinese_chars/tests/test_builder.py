"""Acceptance tests for Character Builder (Milestone 4)."""

from chinese_chars.builder import CharacterBuilder
from chinese_chars.models import CharacterData, Stroke, StrokePoint


def _make_char_data(char="二", stroke_count=2):
    strokes = []
    for i in range(stroke_count):
        s_pts = [StrokePoint(t=0.0, x=0.2, y=0.5 - i * 0.2), StrokePoint(t=1.0, x=0.8, y=0.5 - i * 0.2)]
        strokes.append(Stroke(points=s_pts))
    return CharacterData(char=char, strokes=strokes)


def test_build_produces_reference_cell_first():
    data = _make_char_data("二", 2)
    result = CharacterBuilder.build([data])
    assert len(result) > 0
    ref_cell = result[0][0]
    assert ref_cell.kind == "reference"


def test_build_includes_progressive_stroke_cells():
    data = _make_char_data("二", 2)
    result = CharacterBuilder.build([data], mode=2)
    assert len(result[0]) == 3


def test_build_handles_zero_strokes():
    data = CharacterData(char="?", strokes=[])
    result = CharacterBuilder.build([data])
    assert len(result) == 1
    assert result[0][0].kind == "reference"

def test_build_cell_stroke_indices():
    data = _make_char_data("一", 1)
    result = CharacterBuilder.build([data], mode=2)
    stroke_cells = [c for c in result[0] if c.kind.startswith("stroke-")]
    assert len(stroke_cells) == 1
    assert stroke_cells[0].stroke_index == 1


COLS = 5

def test_build_mode_1_produces_fixed_width_blocks():
    """Mode 1: each char block = ref + strokes + completions (remaining columns)."""
    data = _make_char_data("二", 2)
    result = CharacterBuilder.build([data], mode=1, columns=COLS)
    
    # First is ref, then progressive strokes, then completions
    assert result[0][0].kind == "reference"
    stroke_cells = [c for c in result[0] if c.kind.startswith("stroke-")]
    assert len(stroke_cells) == 2  
    complete_cells = [c for c in result[0] if c.kind == "complete"]
    assert len(complete_cells) == COLS - 1 - 2  
    
    # Total cells = columns (1 ref + 2 strokes + 2 completions)
    assert len(result[0]) == COLS


def test_build_mode_3_produces_tracing_grids():
    """Mode 3: ref + (columns-1) complete grids."""
    data = _make_char_data("二", 2)
    result = CharacterBuilder.build([data], mode=3, columns=COLS)
    assert len(result[0]) == COLS
    assert result[0][0].kind == "reference"
    complete_cells = [c for c in result[0] if c.kind == "complete"]
    assert len(complete_cells) == COLS - 1


def test_build_mode_1_few_strokes():
    """Mode 1 with fewer strokes than columns: completions fill the gap."""
    data = _make_char_data("一", 1)
    result = CharacterBuilder.build([data], mode=1, columns=COLS)
    
    assert result[0][0].kind == "reference"
    assert len([c for c in result[0] if c.kind.startswith("stroke-")]) == 1
    complete_cells = [c for c in result[0] if c.kind == "complete"]
    # 1 ref + 1 stroke + (5 - 2) completions = 5 total
    assert len(complete_cells) == COLS - 2
    assert len(result[0]) == COLS


def test_build_mode_1_many_strokes_wraps_and_fills_row():
    """Mode 1 fills the remaining row after strokes wrap past one line."""
    data = _make_char_data("三", 5)  # 5 strokes = columns exactly (ref takes slot 1, leaves none)
    result = CharacterBuilder.build([data], mode=1, columns=COLS)
    
    assert result[0][0].kind == "reference"
    complete_cells = [c for c in result[0] if c.kind == "complete"]
    # ref + 5 strokes = 6 cells, then 4 complete cells fill the second row.
    assert len(complete_cells) == COLS - 1
    assert len(result[0]) == COLS * 2


def test_build_mode_1_exactly_at_column_limit():
    """ref + strokes exactly equals columns: zero completions."""
    data = _make_char_data("三", 4)  # ref=1, strokes=4 -> total=5=columns -> no room for completions
    result = CharacterBuilder.build([data], mode=1, columns=COLS)
    
    assert len(result[0]) == COLS  # exactly fills it
    complete_cells = [c for c in result[0] if c.kind == "complete"]
    assert len(complete_cells) == 0
