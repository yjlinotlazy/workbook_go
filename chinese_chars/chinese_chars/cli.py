"""Command-line interface for Chinese Chars Workbook Generator.

Connects the pipeline: 
Generator -> Layout -> Renderer -> File Save.
"""

from __future__ import annotations

import argparse
import os
from datetime import date
from pathlib import Path
from typing import Sequence

from chinese_chars.config import DEFAULT_COLUMNS, DEFAULT_FONT_SIZE, PAPER_SIZE_OPTIONS
from chinese_chars.models import Config
from chinese_chars.generator import WorkbookGenerator
from chinese_chars.layout import layout_cells
from chinese_chars.renderer import PdfRenderer


def main(*, argv: Sequence[str] | None = None) -> None:
    """Entry point for the CLI."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    # 1. Validation
    chars = _validate_chars(args.chars)
    paper_size = _validate_paper(args.paper)
    
    cfg = Config(
        chars=chars,
        columns=args.columns,
        paper_size=paper_size,
        font_size=DEFAULT_FONT_SIZE,
        mode=args.mode,
    )

    # 2. Pipeline Execution
    print(f"Characters : {cfg.chars}")
    
    content_cells = WorkbookGenerator().generate_content(cfg)
    structured_workbook = layout_cells(cfg, content_cells)
    
    renderer = PdfRenderer()
    pdf_bytes = renderer.render(structured_workbook)
    
    # 3. Save Output
    output_path = _resolve_output(Path(args.output) if args.output else None)
    output_path.write_bytes(pdf_bytes)
    print(f"PDF saved to {output_path}")


def _build_parser() -> argparse.ArgumentParser:
    """Creates the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="chinese-chars",
        description="Generate printable Chinese handwriting worksheets (M7 & M8)"
    )
    
    parser.add_argument("chars", help="Characters to practice (e.g. '一二三')")
    parser.add_argument("-n", "-c", "--density", dest='columns', type=int, default=DEFAULT_COLUMNS, help="每行格子数 (default: 5)")

    parser.add_argument("-p", "--paper", default="us_letter", choices=PAPER_SIZE_OPTIONS, metavar="SIZE")
    
    parser.add_argument(
        "-m", "--mode", type=int, default=1, choices=[1, 2, 3],
        help="Practice mode: 1=overlay+tracing(default), 2=stroke-blank, 3=tracing-only"
    )
    
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument("-o", "--output", help="Output PDF filepath")
    output_group.add_argument("-v", "--version", action="version", version=f"chinese-chars 0.1.0")
    return parser


def _validate_chars(chars: str) -> str:
    """Strips whitespace and validates that Chinese characters are present."""
    if not chars or chars.strip() == "":
        raise argparse.ArgumentTypeError("需要至少一个汉字 Please provide at least one character.")
    
    import unicodedata
    return chars.strip()


def _validate_paper(paper: str) -> str:
    """Ensures paper size is valid."""
    if paper not in PAPER_SIZE_OPTIONS:
        raise argparse.ArgumentTypeError(f"Invalid paper size '{paper}'. Use us_letter or a4.")
    return paper


def _resolve_output(output_path: Path | None) -> Path:
    """Resolves the output file path with collision handling."""
    if output_path is not None and output_path.exists():
        return _find_unique_name(output_path)
    
    # Default filename: practice_YYYYMMDD_X.pdf
    today = date.today().strftime("%Y%m%d")
    base = Path(f"practice_{today}.pdf")
    
    if base.exists():
        return _find_unique_name(base)
    return base


def _find_unique_name(file_path: Path) -> Path:
    """Finds the next unique filename if the target exists (e.g., _1.pdf, _2.pdf)."""
    stem = file_path.stem
    suffix = file_path.suffix
    parent = file_path.parent
    
    # Determine current max suffix
    import re
    matches = re.finditer(r"_(\d+)\.pdf$", stem)
    nums = [int(m.group(1)) for m in matches]
    current_max = max(nums) if nums else 0
        
    while True:
        new_name = parent / f"{stem}_{current_max + 1}{suffix}"
        if not new_name.exists():
            return new_name
        current_max += 1


if __name__ == "__main__":
    main()
