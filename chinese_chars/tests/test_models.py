"""Acceptance tests for core data model (Task 1.0)."""

from chinese_chars.models import (
    Cell,
    CharacterData,
    Config,
    Page,
    Row,
    Stroke,
    Workbook,
)


def test_construct_minimal_workbook():
    """Build a minimal workbook without any I/O."""
    cfg = Config(chars="一二", repetitions=2)

    stroke1 = Stroke(
        points=[
            _make_sp(t=0.0, x=0.0, y=0.5),
            _make_sp(t=1.0, x=1.0, y=0.5),
        ],
    )
    char_data = CharacterData(char="一", strokes=[stroke1])

    cell_ref = Cell(kind="reference", character_data=char_data, stroke_index=None)
    row = Row(index=0, cells=(cell_ref,))
    page = Page(number=1, rows=(row,), width_cells=3)
    wb = Workbook(title="Practice", config=cfg, pages=(page,))

    assert wb.title == "Practice"
    assert len(wb.pages[0].rows[0].cells) == 1


# ── helpers ───────────────────────────────────────────────────────────

def _make_sp(t: float, x: float, y: float):
    """Helper to avoid importing StrokePoint here."""
    from chinese_chars.models import StrokePoint

    return StrokePoint(t=t, x=x, y=y)
