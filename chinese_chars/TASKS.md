# Milestone 5 — Workbook Generator ✅

Goal: Generate a workbook (sequence of cells) from user input.

## Tasks

- [x] Implement `WorkbookGenerator` in `chinese_chars/generator.py`.
- [x] Connect `StrokeLoader` and `CharacterBuilder`.
- [x] Produce the full list of practice cells for every character in the config.
- [x] No layout logic (page breaks, margins) yet — returns the raw content sequence.

## Acceptance Criteria ✅

Given a `Config` with `chars="一二"`:
1. The generator successfully loads data for both characters.
2. It produces a combined list of cells via `generate_content()`.
3. Existing tests (Builder, Loader) still pass.

---

# Milestone 6 — Layout Engine ✅

Goal: Convert Cells into pages with grid layout (`chinese_chars/layout/__init__.py`).

## Tasks

- [x] Implement `layout_cells` function that groups flat cells into `Workbook`.
- [x] Apply `Config.columns`, paper size rules, and margins.
- [x] Return a structured `Workbook` containing Pages and Rows with geometric metadata (`CellGeometry`).

## Acceptance Criteria ✅

- Cells are arranged correctly into rows/columns based on the `columns` config setting.
- Page breaks occur when grid space is exhausted (e.g., 4x5 or 3x4 grids filling up).
- Geometry (`CellGeometry`) is attached to each `Cell` for the renderer.

---

# Milestone 7 — PDF Renderer ✅

Goal: Render Workbook to PDF (`chinese_chars/renderer/__init__.py`).

## Tasks

- [x] Fix coordinate mapping math (Top-Left aligned, FPDF native coordinate space).
- [x] Add Tian Ge grid drawing (dashed vertical/horizontal centerlines, bounding box).
- [x] Draw progressive stroke paths mapped from `Cell.character_data.strokes`.
- [x] Render reference character using embedded CJK font (`Noto Sans CJK`).
- [x] Save final PDF byte stream to `output_path` in CLI integration.

## Acceptance Criteria ✅

Given a `Config` with `chars="一二三" -n 2`:
1. A printable page per grid with correct paper dimensions (612×792pts US Letter / 595×842pts A4).
2. Gray progressive stroke overlays with correct normalization from source data.
3. Reference characters rendered in black via Noto Sans CJK font.
4. Accurate 0.5" paper margins preserved across pages.

---

# Milestone 8 — End-to-End Integration ✅

Goal: Connect every component in `cli.py`. Pipeline: CLI → Generator → Layout → Renderer.

## Tasks

- [x] Wire `CLI -> Generator.generate_content() -> layout.layout_cells() -> Renderer.render()`.
- [x] Handle filename generation / collision logic (`practice_YYYYMMDD.pdf`, `_1.pdf` suffixes).
- [x] Validate final PDF output size and structure (≥4KB, page count ≥1).

## Acceptance Criteria ✅

```bash
python cli.py 一二三 -n 2 -o practice.pdf
```
produces a valid worksheet file with Tian Ge grids, progressive stroke overlays,
and reference characters rendered to disk.

---

# Milestone 9 — Testing 🚧/⏸️

Tasks

- [x] CLI tests skeleton (`tests/test_cli.py`).
- [x] Stroke loader tests skeleton (`tests/test_stroke_loader.py`).
- [x] Character builder tests skeleton (`tests/test_builder.py`).
- [ ] Generator / Layout integration tests (pending M7/M8). ⏸️
- [ ] PDF renderer smoke test (mock canvas / string assertion). ⏸️

---

# Milestone 10 — Polish 🚧

Tasks

- [x] Better error messages (*partially complete*). ✅
- [ ] Logging. *(Pending)*
- [x] Type hints (*fully annotated in core modules*. ✅)
- [ ] Documentation (`docs/` generation).
- [ ] Performance improvements / stroke data caching.

---
