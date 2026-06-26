"""Acceptance tests for Character Builder (Milestone 4)."""

from chinese_chars.builder import CharacterBuilder
from chinese_chars.models import CharacterData, Stroke, StrokePoint


def _make_char_data(char: str = "二", stroke_count: int = 2) -> CharacterData:
    """Helper to create a minimal CharacterData with N strokes."""
    strokes = []
    for i in range(stroke_count):
        # Each stroke is just a line from center-left to center-right
        s_pts = [StrokePoint(t=0.0, x=0.2, y=0.5 - i * 0.2), StrokePoint(t=1.0, x=0.8, y=0.5 - i * 0.2)]
        strokes.append(Stroke(points=s_pts))
    return CharacterData(char=char, strokes=strokes)


def test_build_produces_reference_cell_first():
    """The first produced cell must be the reference."""
    data = _make_char_data("二", 2)
    result = CharacterBuilder.build(data, repetitions=1)
    
    assert len(result) > 0
    ref_cell = result[0]
    assert ref_cell.kind == "reference"
    assert ref_cell.character_data.char == "二"


def test_build_includes_progressive_stroke_cells():
    """Intermediate cells must be 'stroke-N' types in order."""
    data = _make_char_data("二", 2)
    result = CharacterBuilder.build(data, repetitions=0) # Just ref + strokes
    
    assert len(result) == 3 # 1 ref + 2 progressive
    assert result[1].kind == "stroke-1"
    assert result[2].kind == "stroke-2"


def test_build_includes_correct_number_of_blank_cells():
    """Cells at the end must be 'blank' and count matches `repetitions`."""
    data = _make_char_data("三", 3)
    repetitions_count = 5
    
    result = CharacterBuilder.build(data, repetitions=repetitions_count)
    
    total_expected = 1 + 3 + repetitions_count  # ref + 3 strokes + 5 blanks
    assert len(result) == total_expected
    
    # Check the last N cells are blank
    all_blanks_correct = all(cell.kind == "blank" for cell in result[-repetitions_count:])
    assert all_blanks_correct


def test_build_handles_zero_strokes():
    """If a character has no strokes, only reference and blanks should be produced."""
    data = CharacterData(char="?", strokes=[])
    result = CharacterBuilder.build(data, repetitions=2)
    
    assert len(result) == 3 # 1 ref + 2 blank
    assert result[0].kind == "reference"


def test_build_cell_stroke_indices():
    """Stroke cells must carry the correct `stroke_index`."""
    data = _make_char_data("一", 1)
    result = CharacterBuilder.build(data, repetitions=1)
    
    stroke_cells = [c for c in result if c.kind.startswith("stroke-")]
    assert len(stroke_cells) == 1
    assert stroke_cells[0].stroke_index == 1
