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

# Milestone 6 — Layout Engine 🚧 (Current Focus)

**Status:** Work in Progress. Investigating grid math discrepancies, dynamic cell sizing failures, and FPDF coordinate mapping issues.

Goal: Convert Cells into pages with grid layout (`chinese_chars/layout.py`).

## Active Tasks
- [ ] Fix `step_w` / `row_h` logic to dynamically respect `-c` (columns) config so cells shrink correctly for denser grids.
- [ ] Investigate the "only ~1.5 fit in each row" rendering bug — likely a points-to-pixels mismatch or margin calculation error in geometry generation.
- [ ] Validate Tian Ge grid bounding boxes scale perfectly inside `CellGeometry` regardless of paper size (`us_letter` vs `a4`).
- [ ] Ensure page breaks and cell counts match exactly what `Config` dictates (e.g., physical grid matches `-c` rows/columns).
- [ ] Return a structured `Workbook` containing Pages and Rows with accurate geometric metadata (`CellGeometry`).

## Acceptance Criteria 🚧 *(Pending Fix)*
- Cells are arranged correctly into rows/columns based on the `-c` config setting, shrinking dynamically to fit perfectly.
- Grid sizing works flawlessly across paper sizes without visual overflow or excessive blank margins.
- Tian Ge grids print at the correct physical scale relative to the cell bounds rather than stretching or clipping.

### Blocked Milestones ⏸️
- Milestone 7 (PDF Renderer) and Milestone 8 (E2E Integration) are effectively blocked until M6 grid math accurately aligns with physical rendering.

---

# Milestone 7 — PDF Renderer ⏸️

Goal: Render Workbook to PDF (`chinese_chars/renderer.py`).
Blocked By: Milestone 6 grid math must produce accurate, perfectly-scaled FPDF coordinates before rendering fixes can be verified.

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

# Milestone 8 — End-to-End Integration ⏸️

Goal: Connect every component in `cli.py`. Pipeline: CLI → Generator → Layout → Renderer.
Blocked By: Milestones 6 & 7 must function with verified layout math before end-to-end wireup can be validated.

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
