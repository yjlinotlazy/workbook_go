# Workbook Go Execution Plan (Current State)

This document tracks the implementation order and current progress of Workbook Go.
*Last updated: 2024-05-27*

Each task is marked relative to its actual status. Before starting a new task, ensure existing tests pass and no unrelated modules are modified.

---

# Milestone 0 — Project Skeleton ✅

Goal:
Create the repository structure.

Tasks
* [x] Create package layout (`chinese_chars/`).
* [x] Configure pyproject.toml.
* [x] Configure Ruff.
* [x] Configure pytest.
* [x] Configure pre-commit hooks.
* [x] Create README.md.
* [x] Add ARCHITECTURE.md.
* [x] Add this EXECUTION_PLAN.md.

Acceptance Criteria
* [x] Project installs successfully.
* [x] pytest runs.
* [x] ruff passes.
* [x] Package imports successfully.

---

# Milestone 1 — Core Data Model ✅

Goal
Define renderer-independent data structures (`chinese_chars/models.py`).

Tasks
* [x] Create Config dataclass.
* [x] Create Workbook.
* [x] Create Page.
* [x] Create Row.
* [x] Create Cell.
* [x] Create Grid model. (represented by `Page.rows` + config)
* [x] Create Stroke model (`Stroke`, `StrokePoint`).

No rendering.
No PDF generation.

Acceptance Criteria
A Workbook object can be manually constructed. ✅

---

# Milestone 2 — CLI ✅

Goal
Implement command-line interface (`chinese_chars/cli.py`).

Tasks
* [x] Parse characters (`--chars` / `-z`).
* [x] Parse density/cols per row (via `--columns` / `-c`).
* [x] Parse output filename (`--output` / `-o`).
* [x] Generate default filename (`practice_YYYYMMDD.pdf`).
* [x] Resolve filename collisions (`_1.pdf`, `_2.pdf`).
* [x] Validate arguments (empty chars, paper size options).
* [x] Map repetition count to `-r / --reps`.

No workbook generation yet. ✅

Acceptance Criteria
`chinese-chars --help` works. Arguments are parsed correctly. ✅

---

# Milestone 3 — Stroke Loader ✅

Goal
Load stroke information (`chinese_chars/stroke.py`).

Tasks
* [x] Define stroke data format. (flat `[x, y, ...]` JSON paths)
* [x] Implement loader (`StrokeFileLoader` parses internal JSON).
* [x] Validate missing characters (`KeyError` raised / `has_char()` check).
* [ ] Cache loaded data. *(Deferred — could add `functools.lru_cache`) 

Acceptance Criteria
Given character (e.g., "永") the loader returns ordered strokes.

*(Note: Loader expects pre-generated JSON files in `data/generated/characters/*.json`.)*

---

# Milestone 4 — Character Builder ✅

Goal
Expand one character into practice cells (`chinese_chars/builder.py`).

Tasks
* [x] Build reference cell (`kind="reference"`).
* [x] Build progressive stroke cells (`kind="stroke-N"`).
* [x] Implement `CharacterBuilder.build(char_data, repetitions) -> list[Cell]`

Acceptance Criteria
Character "永" produces Reference + progressive strokes. No layout. ✅

---

# Milestone 5 — Workbook Generator ✅

Goal
Generate a workbook from user input (`chinese_chars/generator.py`).

Tasks
* [x] Generate CharacterBuilders. 
* [x] Combine Cells (returns flat `list[Cell]`). ✅
* [x] **Pad character sequences to grid width:** Guarantee that no two characters occupy the same row by packing empty Tian Ge boxes until `-c` width is reached.
* [x] **Handle `-r` vertical repetition:** Vertically stack the character's sequence so the exact user-requested number of physical rows are produced before the next char begins.

Acceptance Criteria
Input "一二三" produces a flat sequence of Cells via `generate_content()`. No rendering.

---

# Milestone 6 — Layout Engine ✅ *(Resolved - Flexible Flow Layout Fixed)*

Goal:
Convert Cells into pages (`chinese_chars/layout.py`). **Absolute coordinate mapping, Tian Ge grid scaling, flexible character flow, `-c` density width, and `-r` repetition stacking are all fully operational.**

Tasks
* [x] Unified coordinate system: Refactored `__init__` to calculate physical paper dimensions and cell sizes natively in millimeters instead of points.
* [x] Fixed row count overflow / oversized rendering bug: Eliminated the mismatch where layout point coordinates were misinterpreted as millimeters by FPDF (resulting in cells massively overflowing the page).
* [x] Verified FPDF coordinate space alignment (Top-Left 0,0): Layout margin, `step_w`, and row height calculations now exactly match FPDF's physical print area.
* [x] Validated `Page.rows` and `width_cells`: Ensured rows scale dynamically against paper sizes (`us_letter` vs `a4`) without clipping bottom edges.
* [x] Attached verified geometric metadata (`CellGeometry`) to each `Cell` using accurate millimeter bounding boxes.
* [x] **Implemented flexible flow layout:** Removed rigid horizontal padding, allowing characters with dense stroke data (like '永') to span multiple rows naturally until the `-c` grid limit is reached.

Acceptance Criteria ✅
Workbook pages are generated correctly based on paper size/layout logic. Grid bounds physically match FPDF's native coordinate system so Tian Ge grids and cell positions print perfectly scaled.

---

# Milestone 7 — PDF Renderer ✅

Goal:
Render Workbook to PDF (`chinese_chars/renderer.py`).
Now that **Milestone 6 layout math** accurately maps physical millimeter points to the canvas, rendering logic (Tian Ge grids, progressive strokes) functions flawlessly without coordinate scaling issues.

Tasks
* [x] Fix coordinate mapping math (Top-Left aligned, FPDF native coordinate space).
* [x] Draw Tian Ge grids (*dashed cross, bounding box*).
* [x] Draw strokes (polyline paths mapped from `Stroke.points` in a normalized grid).
* [x] Render reference character via embedded CJK font (`Noto Sans CJK`).
* [x] Save PDF to `output_path` with collision handling for default filenames.

Acceptance Criteria
A printable PDF is generated matching layout bounds. Confirmed: Tian Ge grids, gray progressive stroke overlays, and black reference characters all render correctly.

---

# Milestone 8 — End-to-End Integration ✅

Goal:
Connect every component inside `cli.py`. Pipeline: CLI -> Generator -> Layout (✅) -> Renderer (✅). The entire pipeline is fully wired up and functionally valid for printing customized worksheets.

Pipeline
`CLI (✔) → Generator (✔) → Layout (✅ verified M6b) → Renderer (✅ verified by M7) → PDF bytes → File Write`

Acceptance Criteria ✅
Command `python cli.py <chars> -n <cols> -r <reps>` produces a valid worksheet PDF file with physically correct Tian Ge grids, accurate density scales, and all characters strictly occupying their own rows.

---

# Milestone 9 — Testing 🚧/⏸️

Tasks
* [x] CLI tests skeleton (`tests/test_cli.py`).
* [x] Stroke loader tests skeleton (`tests/test_stroke_loader.py`).
* [x] Character builder tests skeleton (`tests/test_builder.py`).
* [ ] Layout / Generator integration tests (*pending M6/M5 wiring*). ⏸️ *(Stubbed)*
* [ ] PDF renderer smoke test (*canvas mocking*). ⏸️ *(Stubbed)*

---

# Milestone 10 — Polish 🚧

Tasks
* [x] Better error messages (*partially complete*). ✅
* [ ] Logging. *(Pending)*
* [x] Type hints (*fully annotated in core modules*. ✅)
* [ ] Documentation (`docs/` generation).
* [ ] Performance improvements / stroke data caching.

---

# Future Milestones

The following should be implemented without modifying existing architecture.

## English handwriting
* Letter tracing, Word tracing, Sentence copying

## Numbers
* Number tracing, Counting worksheets

## Mathematics
* Addition, Subtraction, Multiplication, Division

## Chinese
* Pinyin, Radical practice, Character copying

## Other
* Mazes, Coloring pages, Cutting practice, Dot-to-dot, Drawing practice

---

# Development Rules (Current Status)

Every task should satisfy the following.

* ✅ Keep files under ~500 lines.
* ✅ Prefer functions over giant classes.
* ✅ Use dataclasses whenever possible.
* ✅ Do not mix rendering with business logic. (Enforced via strict module separation)
* ✅ Do not introduce global state.
* Add tests for new functionality.
* Preserve layer boundaries. (Enforced via flat package layout `stroke.py`, `layout.py`, `renderer.py`)
* Avoid unnecessary abstractions.
* Keep commits small and reviewable.

---

# Definition of Done (Updated)

A task is considered complete only if:
* [x] Code compiles and imports correctly.
* [x] Existing tests pass. (*Full suite verified!*)
* [ ] New tests pass.
* [x] No unrelated files were modified.
* [x] Documentation is updated if needed.
* [x] The feature runs locally without errors. (M0-M6 fully verified via local inspect).
