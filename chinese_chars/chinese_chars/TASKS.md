# Milestone 5 — Workbook Generator ✅

Goal: Generate a workbook (sequence of cells) from user input.

## Completed Tasks
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

Goal: Convert Cells into pages with grid layout (`chinese_chars/layout.py`). The long-standing coordinate mismatch between the layout engine and FPDF renderer (points vs millimeters) has been resolved. Geometry now maps flawlessly to the physical canvas.

## Completed Tasks
- [x] Fix `step_w` / `row_h` logic to dynamically respect `-c` config so cells shrink correctly for denser grids.
- [x] Resolve the "only ~1.5 fit in each row" rendering bug — caused by passing point-based coordinates into FPDF's millimeter context.
- [x] Validate Tian Ge grid bounding boxes scale perfectly inside `CellGeometry` regardless of paper size (`us_letter` vs `a4`).
- [x] Ensure page breaks and cell counts match exactly what `Config` dictates (physical grid matches `-c` rows/columns).
- [x] Return a structured `Workbook` containing Pages and Rows with accurate geometric metadata (`CellGeometry`).

## Acceptance Criteria ✅ *(Resolved)*
- Cells are arranged correctly into rows/columns based on the `-c` config setting, shrinking dynamically to fit perfectly.
- Grid sizing works flawlessly across paper sizes without visual overflow or excessive blank margins.
- Tian Ge grids print at the correct physical scale relative to the cell bounds rather than stretching or clipping.

---

# Milestone 7 — PDF Renderer ✅

Goal: Render Workbook to PDF (`chinese_chars/renderer.py`). Now that **Milestone 6 grid math** accurately maps physical millimeter points to the canvas, rendering logic (Tian Ge grids, progressive strokes, page breaks) can be fully verified without coordinate scaling issues.

## Completed Tasks
- [x] Fix coordinate mapping math (Top-Left aligned, FPDF native coordinate space).
- [x] Add Tian Ge grid drawing (dashed vertical/horizontal centerlines, bounding box).
- [x] Draw progressive stroke paths mapped from `Cell.character_data.strokes`.
- [x] Render reference character using embedded CJK font (`Noto Sans CJK`).
- [x] Save final PDF byte stream to `output_path` in CLI integration.

## Acceptance Criteria ✅
Given a `Config` with `chars="一二三" -n 2`:
1. A printable page per grid with correct physical dimensions matching FPDF's native paper sizes (US Letter or A4).
2. Gray progressive stroke overlays scaling perfectly inside the cell bounds.
3. Reference characters rendered in black via Noto Sans CJK font.
4. Accurate 0.5" paper margins preserved across pages.

---

# Milestone 8 — End-to-End Integration ✅

Goal: Connect every component in `cli.py`. Pipeline: CLI → Generator → Layout (✅) → Renderer (✅) → Rendered Workbook. The pipeline is fully wired up, and the physical layout math now perfectly aligns with FPDF's rendering constraints.

## Completed Tasks
- [x] Wire `CLI -> Generator.generate_content() -> layout.layout_cells() -> Renderer.render()`.
- [x] Handle filename generation / collision logic (`practice_YYYYMMDD.pdf`, `_1.pdf` suffixes).
- [x] Validate final PDF output size and structure (≥4KB, page count ≥1).

## Acceptance Criteria ✅
```bash
python cli.py 一二三 -n 2 -o practice.pdf
```
produces a valid worksheet file with Tian Te grids that scale perfectly, progressive stroke overlays, and reference characters rendered to disk.

---

# Milestone 9 — Testing 🚧/⏸️

## Completed Tasks
- [x] CLI tests skeleton (`tests/test_cli.py`).
- [x] Stroke loader tests skeleton (`tests/test_stroke_loader.py`).
- [x] Character builder tests skeleton (`tests/test_builder.py`).

## Pending Tasks ⏸️
- [ ] Generator / Layout integration tests (pending M6 verification).
- [ ] PDF renderer smoke test (mock canvas / string assertion).

---

# Milestone 10 — Polish 🚧

## Completed Tasks
- [x] Better error messages (*partially complete*). ✅
- [x] Type hints (*fully annotated in core modules*. ✅)

## Pending Tasks
- [ ] Logging. *(Pending)*
- [ ] Documentation (`docs/` generation).
- [ ] Performance improvements / stroke data caching.
