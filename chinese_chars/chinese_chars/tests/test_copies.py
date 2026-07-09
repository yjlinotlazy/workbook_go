"""Tests for the copies (print repetition) feature."""

from io import BytesIO

from pypdf import PdfReader

from chinese_chars.generator import WorkbookGenerator
from chinese_chars.layout import layout_cells
from chinese_chars.models import Config, Cell


def _make_dummy_config(chars="一二", copies=3, columns=5) -> Config:
    """Helper to create a config with minimal char blocks for testing."""
    return Config(
        chars=chars,
        copies=copies,
        columns=columns,
        paper_size="us_letter",
        font_size=48,
        mode=1,
    )


def _make_dummy_char_blocks(count: int) -> list[list[Cell]]:
    """Helper to create dummy char blocks with given count."""
    return [[Cell(kind="reference", character_data=None, stroke_index=None)] for _ in range(count)]


class TestCopiesConfig:
    def test_copy_default_is_three(self):
        config = Config(chars="一")
        assert config.copies == 3

    def test_copy_explicit_value(self):
        assert Config(chars="一", copies=5).copies == 5

    def test_copy_one(self):
        assert Config(chars="一", copies=1).copies == 1


class TestCopiesLayout:
    def test_layout_repeats_pages_copies_times(self):
        """Each base page is repeated N times with sequential numbers."""
        config = Config(chars="一二", copies=2, columns=5)

        # Two chars, each producing one reference cell
        char_blocks = _make_dummy_char_blocks(2)
        wb = layout_cells(config, char_blocks)

        # 2 refs fit on a single page -> 1 base page * 2 copies = 2 total pages
        assert len(wb.pages) == 2

    def test_layout_repeats_pages_with_many_chars(self):
        """Multiple chars should each get their page(s) repeated."""
        config = Config(chars="一二三", copies=3, columns=5)
        char_blocks = _make_dummy_char_blocks(3)
        wb = layout_cells(config, char_blocks)

        # Depending on paper_size, 3 refs may fit on 1 page -> 3 total after copies
        assert all(p in range(1, len(wb.pages) + 1) for p in [page.number for page in wb.pages[:1]])
        # Total pages = base_pages * copies
        assert len(wb.pages) % config.copies == 0


class TestCopiesPdfPageCount:
    """Integration: copies should produce the right number of PDF pages."""

    def test_copy_1_produces_1_pdf_page(self):
        config = _make_dummy_config(copies=1)
        wb = layout_cells(config, _make_dummy_char_blocks(2))
        from chinese_chars.renderer import PdfRenderer
        pdf_bytes = PdfRenderer().render(wb)

        reader = PdfReader(BytesIO(pdf_bytes))
        assert len(reader.pages) == 1

    def test_copy_3_produces_3_pdf_pages(self):
        config = _make_dummy_config(copies=3)
        wb = layout_cells(config, _make_dummy_char_blocks(2))
        from chinese_chars.renderer import PdfRenderer
        pdf_bytes = PdfRenderer().render(wb)

        reader = PdfReader(BytesIO(pdf_bytes))
        assert len(reader.pages) == 3

    def test_copy_5_produces_5_pdf_pages(self):
        config = _make_dummy_config(copies=5)
        wb = layout_cells(config, _make_dummy_char_blocks(1))
        from chinese_chars.renderer import PdfRenderer
        pdf_bytes = PdfRenderer().render(wb)

        reader = PdfReader(BytesIO(pdf_bytes))
        assert len(reader.pages) == 5

    def test_copy_pages_are_increased_sequence(self):
        """Page numbers should be sequential across all copies."""
        config = _make_dummy_config(copies=2)
        wb = layout_cells(config, _make_dummy_char_blocks(1))

        numbers = [page.number for page in wb.pages]
        assert numbers == list(range(1, len(wb.pages) + 1))
        assert len(set(numbers)) == len(numbers)  # all unique
