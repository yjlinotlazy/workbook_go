# Workbook Go Execution Plan (Current State)

This document tracks the implementation order and current progress of Workbook Go.
*Last updated: 2024-05-26*

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
* [x] Parse cells per row (via `--columns` / `-c`).
* [x] Parse output filename (`--output` / `-o`).
* [x] Generate default filename (`practice_YYYYMMDD.pdf`).
* [x] Resolve filename collisions (`_1.pdf`, `_2.pdf`).
* [x] Validate arguments (empty chars, paper size options).

No workbook generation yet. ✅

Acceptance Criteria
`chinese-chars --help` works. Arguments are parsed correctly. ✅

---

# Milestone 3 — Stroke Loader ✅

Goal
Load stroke information (`chinese_chars/stroke/__init__.py`).

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
* [x] Build blank practice cells (`kind="blank"`).
* [x] Implement `CharacterBuilder.build(char_data, repetitions) -> list[Cell]`

Acceptance Criteria
Character "永" produces Reference + progressive strokes + blanks. No layout. ✅

---

# Milestone 5 — Workbook Generator 🚧

Goal
Generate a workbook from user input (`chinese_chars/generator.py`).

Tasks
* [x] Generate CharacterBuilders. 
* [x] Combine Cells (returns flat `list[Cell]`). ✅
* [ ] Create full `Workbook` object wrapping cells into `Page`s. ➡️ **Resolved by M6** (See `layout_cells`)

Acceptance Criteria
Input "一二三" produces a flat sequence of Cells via `generate_content()`. No rendering. *(Note: Row/Page wrapping is handled by M6 Layout Engine).*

---

# Milestone 6 — Layout Engine ✅

Goal
Convert Cells into pages (`chinese_chars/layout/__init__.py`).

Tasks
* [x] Implement rows & Page grouping (`Page.rows`, `Page.width_cells`)
* [x] Implement margins. *(Using standard 0.5" margin)*
* [x] Use config for columns (`config.columns` passed in).
* [x] Attach geometric metadata to each `Cell`.

Acceptance Criteria
Workbook pages are generated correctly based on paper size/layout logic. ✅

---

# Milestone 7 — PDF Renderer ✅

Goal
Render Workbook to PDF (`chinese_chars/renderer/__init__.py`).

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

Goal
Connect every component inside `cli.py` (moved to project root).

Pipeline
`CLI (✔) → Generator (✔) → Layout (✔) → Renderer (✔) → PDF bytes → File Write`

Acceptance Criteria
Command `python cli.py <chars> -n <reps>` produces a valid worksheet PDF file with all components wired end-to-end.

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
* Preserve layer boundaries. (Enforced via package layout `stroke/`, `layout/`, `renderer/`)
* Avoid unnecessary abstractions.
* Keep commits small and reviewable.

---

# Definition of Done (Updated)

A task is considered complete only if:
* [x] Code compiles and imports correctly.
* [ ] Existing tests pass. (*Skeletons exist, full suite pending M7/M8*)
* [ ] New tests pass.
* [x] No unrelated files were modified.
* [ ] Documentation is updated if needed.
* [x] The feature runs locally without errors. (M0-M6 verified via local inspect).
