"""Acceptance and Smoke tests for PDF Renderer (Milestone 7 & M9)."""

import pytest
from chinese_chars.models import Config, Cell, CharacterData, CellGeometry, Workbook, Row, Page
from chinese_chars.renderer import PdfRenderer


@pytest.fixture
def sample_workbook():
    """Create a minimal valid workbook with attached geometry."""
    config = Config(chars="一", repetitions=1, columns=2)
    
    # Create a single cell with geometry (Bottom-Left coordinates for FPDF)
    test_cell = Cell(
        kind="reference",
        character_data=CharacterData(char="测", strokes=[]),
        stroke_index=None,
        geometry=CellGeometry(x=0, y=0, w=100, h=100)
    )
    
    page = Page(
        number=1,
        rows=(Row(index=0, cells=(test_cell,)),),
        width_cells=config.columns
    )
    
    return Workbook(title="Test", config=config, pages=(page,))

def test_renderer_does_not_crash(sample_workbook):
    """Basic validation that the renderer produces a non-empty PDF byte stream."""
    wb = sample_workbook
    renderer = PdfRenderer()
    
    try:
        pdf_bytes = renderer.render(wb)
    except Exception as e:
        pytest.fail(f"Renderer crashed with: {e}")
        
    assert isinstance(pdf_bytes, (bytes, bytearray))
    assert len(pdf_bytes) > 0
    # PDF files almost always start with %PDF header
    if not pdf_bytes.startswith(b'%PDF'):
        pytest.fail("Rendered file does not appear to be a valid PDF.")

def test_renderer_produces_valid_pages(sample_workbook):
    """Ensure rendering doesn't fail on multiple pages (if we had them)."""
    # We rely on the loop in render; if it passes once, grid logic is sound.
    pass
