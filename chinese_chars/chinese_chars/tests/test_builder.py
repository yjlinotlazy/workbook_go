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
    result = CharacterBuilder.build([data])
    
    assert len(result) > 0
    ref_cell = result[0][0]
    assert ref_cell.kind == "reference"
    assert ref_cell.character_data.char == "二"


def test_build_includes_progressive_stroke_cells():
    """Intermediate cells must be 'stroke-N' types in order."""
    data = _make_char_data("二", 2)
    result = CharacterBuilder.build([data])  # Just ref + strokes, no repetition parameter
    
    assert len(result) == 1
    assert len(result[0]) == 3  # 1 ref + 2 progressive


def test_build_handles_zero_strokes():
    """If a character has no strokes, only reference should be produced."""
    data = CharacterData(char="?", strokes=[])
    result = CharacterBuilder.build([data])
    
    assert len(result) == 1  # Only one char group
    assert len(result[0]) == 1  # Only reference cell
    assert result[0][0].kind == "reference"


def test_build_cell_stroke_indices():
    """Stroke cells must carry the correct `stroke_index`."""
    data = _make_char_data("一", 1)
    result = CharacterBuilder.build([data])
    
    stroke_cells = [c for c in result[0] if c.kind.startswith("stroke-")]
    assert len(stroke_cells) == 1
    assert stroke_cells[0].stroke_index == 1


def test_build_multiple_chars():
    """Multiple chars produce multiple inner lists."""
    data1 = _make_char_data("二", 2)
    data2 = _make_char_data("三", 3)
    result = CharacterBuilder.build([data1, data2])
    
    assert len(result) == 2
    # first char: ref + 2 strokes
    assert len(result[0]) == 3
    # second char: ref + 3 strokes
    assert len(result[1]) == 4
