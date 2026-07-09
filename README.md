# Workbook Go

Workbook Go is a printable worksheet generator for kids.

当前主要功能是生成汉字练字 PDF：输入一组汉字，程序会按笔顺数据生成带田字格的练习纸。每个字可以包含参考字、逐笔叠加提示、描红格和空白练习格。

## Features

- Generate printable Chinese handwriting worksheets as PDF.
- Support US Letter and A4 paper.
- Configure grid density by setting the number of cells per row.
- Choose one of three practice modes:
  - Mode 1: reference character, progressive stroke cells, then tracing cells.
  - Mode 2: reference character, progressive stroke cells, then blank cells from layout padding.
  - Mode 3: reference character plus tracing cells only.
- Repeat generated pages with `--copies`.
- Automatically create a dated output filename when `--output` is not provided.
- Load stroke data from the repository's internal JSON format, including generated MakeMeAHanzi imports.

## Repository Layout

```text
.
├── README.md
├── tests/
└── chinese_chars/
    ├── pyproject.toml
    ├── cli.py
    ├── chinese_chars/
    │   ├── builder.py
    │   ├── config.py
    │   ├── generator.py
    │   ├── layout.py
    │   ├── models.py
    │   ├── renderer.py
    │   └── stroke.py
    ├── data/
    │   └── generated/characters/
    ├── scripts/
    │   └── import_makemeahanzi.py
    ├── ARCHITECTURE.md
    ├── DATA_PIPELINE.md
    └── Requirements.md
```

The `chinese_chars/` directory is the Python project. Run install, CLI, and tests from that directory unless noted otherwise.

## Requirements

- Python 3.11 or newer
- `fpdf2`
- A CJK font available to the PDF renderer

The renderer currently tries common Linux font paths such as:

- `/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc`
- `/usr/share/fonts/TTF/uming.ttc`
- `/usr/share/fonts/TTF/ukai.ttc`

Reference characters are rendered with `Ukai`, so install a compatible CJK font if PDF generation fails while setting the font.

## Installation

```bash
cd chinese_chars
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

For development tools with a tool that supports dependency groups:

```bash
uv sync --dev
```

Or install the development tools directly with pip:

```bash
python -m pip install pytest ruff pre-commit
```

## Usage

Generate a worksheet for several characters:

```bash
cd chinese_chars
chinese-chars 一二三四五 -n 5 -o output/practice.pdf
```

The same command can also be run through the module entry point:

```bash
python -m chinese_chars 一二三四五 -n 5 -o output/practice.pdf
```

If `--output` is omitted, the CLI writes to `practice_YYYYMMDD.pdf` in the current directory. If that file already exists, it appends a numeric suffix such as `practice_YYYYMMDD_1.pdf`.

### Options

```text
chars                 Characters to practice, for example 一二三
-n, -c, --density    Number of grid cells per row. Default: 5
-p, --paper          Paper size: us_letter or a4. Default: us_letter
-m, --mode           Practice mode: 1, 2, or 3. Default: 1
-k, --copies         Number of copies for each generated page. Default: 2
-o, --output         Output PDF path
-v, --version        Print CLI version
```

Examples:

```bash
chinese-chars 永 -m 1 -n 5 -k 2 -o output/yong.pdf
chinese-chars 春夏秋冬 --paper a4 --density 6 --mode 3
```

## Practice Modes

Mode 1 is the default. For each character, it creates a reference cell, progressive stroke cells, and then fills any remaining cells in that character block with complete tracing cells.

Mode 2 creates a reference cell and progressive stroke cells. The layout engine pads the rest of the row or page with blank practice grids.

Mode 3 creates a reference cell followed by complete tracing cells, without step-by-step stroke progression.

All modes use Tianzige-style grid cells with an outer border and center guide lines.

## Data

Worksheet generation uses internal character JSON files under:

```text
chinese_chars/data/generated/characters/
chinese_chars/data/
```

The loader prefers `data/generated/characters/<char>.json` and falls back to `data/<char>.json`.

Internal JSON is the runtime source of truth. External datasets are converted first and are not read by normal workbook generation. See `chinese_chars/DATA_PIPELINE.md` for the full data pipeline.

To regenerate data from MakeMeAHanzi, update the raw dataset path in `scripts/import_makemeahanzi.py` if needed, then run:

```bash
cd chinese_chars
python scripts/import_makemeahanzi.py
```

## Architecture

The generation pipeline is intentionally one-way:

```text
CLI
  -> WorkbookGenerator
  -> CharacterBuilder
  -> LayoutEngine
  -> PdfRenderer
  -> PDF file
```

The main layers are:

- `cli.py`: parses command-line arguments, validates inputs, writes the PDF.
- `stroke.py`: loads internal stroke JSON into renderer-independent models.
- `builder.py`: turns each character into reference, stroke, complete, and blank cells.
- `layout.py`: arranges cells into rows and pages with physical coordinates.
- `renderer.py`: draws grids, reference characters, and stroke paths into a PDF.
- `models.py`: defines the workbook data model shared by the pipeline.

More detail is documented in `chinese_chars/ARCHITECTURE.md`.

## Tests

Run the test suite from the Python project directory:

```bash
cd chinese_chars
python -m pytest tests --import-mode=importlib
```

Run a specific test file:

```bash
python -m pytest tests/test_builder.py --import-mode=importlib
```

The explicit import mode avoids pytest module-name collisions caused by the repository's duplicated `tests/` and `chinese_chars/tests/` file names.

## Current Scope

Workbook Go currently focuses on Chinese handwriting worksheets. The code is structured so other worksheet types or renderers can be added later without changing the core workbook model.
