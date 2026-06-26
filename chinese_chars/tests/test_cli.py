"""Smoke tests and feature tests for CLI parsing (Milestone 2)."""

import chinese_chars
import cli as cli


def test_package_imports() -> None:
    """Package imports without error."""
    assert hasattr(cli, "main")


def test_cli_help_prints_usage(capsys) -> None:
    """CLI --help executes and displays usage information."""
    try:
        cli.main(argv=["--help"])
    except SystemExit as e:
        assert e.code == 0
    
    captured = capsys.readouterr()
    assert "usage: chinese-chars" in captured.out.lower()


def test_cli_version_prints_version(capsys) -> None:
    """CLI -v prints the correct version string."""
    try:
        cli.main(argv=["-v"])
    except SystemExit:
        pass  # argparse exits after printing version
    
    captured = capsys.readouterr()
    assert chinese_chars.__version__ in captured.out


def test_parses_chinese_characters(capsys, monkeypatch):
    """Parsing valid Chinese characters produces expected config output."""
    # Mock rendering and generator to avoid filesystem dependencies
    def dummy_render(self, workbook):
        return b'%PDF-1.4 fake'
    
    def dummy_gen(*args):
        from chinese_chars.models import Cell 
        return [Cell(kind="blank", character_data=None)]
    
    import chinese_chars.renderer as r
    import chinese_chars.generator as g
    monkeypatch.setattr(r.PdfRenderer, 'render', dummy_render)
    monkeypatch.setattr(g.WorkbookGenerator, 'generate_content', dummy_gen)
    
    cli.main(argv=["一二三"])
    captured = capsys.readouterr()
    assert "Characters : 一二三" in captured.out


def test_parsing_default_repetitions(capsys, monkeypatch):
    """Using default repetitions shows '3' when not specified."""
    def dummy_render(self, workbook):
        return b'%PDF-1.4 fake'
    import chinese_chars.renderer as r
    import chinese_chars.generator as g
    monkeypatch.setattr(r.PdfRenderer, 'render', dummy_render)
    monkeypatch.setattr(g.WorkbookGenerator, 'generate_content', lambda *args: [])

    cli.main(argv=["一"])
    captured = capsys.readouterr()
    assert "Repetitions: 3" in captured.out


def test_parsing_custom_repetitions(capsys, monkeypatch):
    """Using -n sets the custom repetition count."""
    def dummy_render(self, workbook):
        return b'%PDF-1.4 fake'
    import chinese_chars.renderer as r
    import chinese_chars.generator as g
    monkeypatch.setattr(r.PdfRenderer, 'render', dummy_render)
    monkeypatch.setattr(g.WorkbookGenerator, 'generate_content', lambda *args: [])

    cli.main(argv=["一", "-n", "5"])
    captured = capsys.readouterr()
    assert "Repetitions: 5" in captured.out


def test_resolves_filename_collision(tmp_path) -> None:
    """Ensure output filename increments on collision."""
    base = tmp_path / "practice_20240101.pdf"
    base.touch()
    
    second = cli._find_unique_name(base)
    assert str(second).endswith("practice_20240101_1.pdf")
    
    second.touch()
    third = cli._find_unique_name(base)
    assert str(third).endswith("practice_20240101_2.pdf")


def test_default_filename_format() -> None:
    """Default output filename follows practice_YYYYMMDD.pdf format."""
    result = cli._resolve_output(None)
    assert result.suffix == ".pdf"
    assert result.stem.startswith("practice_")
    assert result.suffix == ".pdf"
    assert result.stem.startswith("practice_")


def test_chars_validation_rejects_empty() -> None:
    """Empty string provided for chars triggers validation error."""
    try:
        cli.main(argv=[""])
        assert False, "Should have raised ArgumentTypeError"  # noqa: PT017
    except Exception as exc:
        assert "需要至少一个汉字" in str(exc)