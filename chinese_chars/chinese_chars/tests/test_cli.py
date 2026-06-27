"""Smoke tests and feature tests for CLI parsing (Milestone 2)."""

import chinese_chars
import cli as cli


def test_package_imports() -> None:
    """Package imports without error."""
    assert hasattr(cli, "main")


def test_cli_help_prints_usage(capsys) -> None:
    try:
        cli.main(argv=["--help"])
    except SystemExit as e:
        assert e.code == 0
    
    captured = capsys.readouterr()
    assert "usage: chinese-chars" in captured.out.lower()


def test_cli_version_prints_version(capsys) -> None:
    try:
        cli.main(argv=["-v"])
    except SystemExit:
        pass
    
    captured = capsys.readouterr()
    assert chinese_chars.__version__ in captured.out


def test_parses_chinese_characters(capsys, monkeypatch):
    """Parsing valid Chinese characters produces expected config output."""
    def dummy_render(self, workbook):
        return b'%PDF-1.4 fake'

    # generator.generate_content() returns list[list[Cell]] — one inner list per char
    def dummy_gen(*_args): 
        from chinese_chars.models import Cell
        # Return [[cells_for_char1], [cells_for_char2], ...] — 3 chars = 3 blocks  
        return [
            [Cell(kind="reference", character_data=None, stroke_index=None)],  
            [Cell(kind="blank", character_data=None, stroke_index=None)],
            [Cell(kind="blank", character_data=None, stroke_index=None)]
        ]

    import chinese_chars.renderer as r
    import chinese_chars.generator as g
    monkeypatch.setattr(r.PdfRenderer, 'render', dummy_render)
    monkeypatch.setattr(g.WorkbookGenerator, 'generate_content', dummy_gen)
    
    cli.main(argv=["一二三"])
    captured = capsys.readouterr()
    assert "Characters" in captured.out


def test_resolves_filename_collision(tmp_path) -> None:
    base = tmp_path / "practice_20240101.pdf"
    base.touch()
    
    second = cli._find_unique_name(base)
    assert str(second).endswith("practice_20240101_1.pdf")
    
    second.touch()
    third = cli._find_unique_name(base)
    assert str(third).endswith("practice_20240101_2.pdf")


def test_default_filename_format() -> None:
    result = cli._resolve_output(None)
    assert result.suffix == ".pdf"
    assert result.stem.startswith("practice_")


def test_chars_validation_rejects_empty() -> None:
    try:
        cli.main(argv=[""])
        assert False, "Should have raised ArgumentTypeError"
    except Exception as exc:
        assert "需要至少一个汉字" in str(exc)
