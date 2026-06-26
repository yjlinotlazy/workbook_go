# TASKS.md

# Task 0.1 — Bootstrap the Project

## Goal

Create the initial project structure and development environment for chinese_chars.

This task **does not implement any worksheet generation functionality**. Its sole purpose is to create a clean, maintainable Python project that future tasks can build upon.

---

# Background

Chinese Chars (chinese_chars sub-project) is a command-line tool that generates printable handwriting worksheets for children.

The implementation will follow the architecture described in `ARCHITECTURE.md`.

This task only creates the repository skeleton.

---

# Scope

## In Scope

* Create the Python package structure.
* Configure project tooling.
* Create an installable package.
* Create a minimal CLI entry point.
* Configure testing and linting.
* Ensure the repository builds successfully.

## Out of Scope

Do **NOT** implement:

* Worksheet generation
* PDF rendering
* Layout engine
* Stroke loading
* Character processing
* Tian grid drawing
* Business logic

If any of these are implemented, the task has exceeded its scope.

---

# Required Directory Structure

```text
chinese_chars/
│
├── __init__.py
├── __main__.py
├── cli.py
├── config.py
├── models.py
│
├── layout/
│   └── __init__.py
│
├── renderer/
│   └── __init__.py
│
├── stroke/
│   └── __init__.py
│
├── utils/
│   └── __init__.py
│
tests/
│
README.md
ARCHITECTURE.md
EXECUTION_PLAN.md
TASKS.md
pyproject.toml
```

The modules may contain placeholder implementations.

---

# Requirements

## Package

The project must be installable with

```bash
pip install -e .
```

---

## CLI

Expose a command

```bash
chinese-chars --help
```

The command should execute successfully.

For now, invoking the command may simply print

```text
chinese-chars v0.1.0

This feature has not been implemented yet.
```

No worksheet generation should occur.

---

## Tooling

Configure

* Ruff
* pytest
* pre-commit

The configuration should be minimal and conventional.

---

## Package Metadata

Create a `pyproject.toml` that includes:

* project name
* version
* description
* Python requirement (3.11+)
* console script entry point

Avoid unnecessary dependencies.

---

# Tests

Create minimal smoke tests.

Suggested tests include

* package imports successfully
* CLI can execute with `--help`

Do not create placeholder tests for future functionality.

---

# Constraints

* Do not invent future APIs.
* Do not design rendering interfaces.
* Do not create abstract base classes.
* Do not create unnecessary inheritance.
* Keep placeholder code minimal.
* Prefer dataclasses where appropriate.
* Keep every file under approximately 200 lines.

---

# Acceptance Criteria

The following commands should all succeed.

```bash
pip install -e .

ruff check .

pytest

chinese-chars --help
```

No warnings or errors should be produced.

---

# Definition of Done

This task is complete when:

- [x] Repository structure matches the architecture.
- [x] Package installs successfully.
- [x] CLI executes successfully.
- [x] All tests pass.
- [x] Ruff passes.
- [ ] No worksheet functionality has been implemented.
- [ ] No rendering functionality has been configured.
- [ ] The repository is ready for Task 1.0 (Core Data Model).

---

# Files Expected to Change

- pyproject.toml
- README.md
- chinese_chars/**
- tests/**
- .gitignore
- .pre-commit-config.yaml (optional)

No other files should be modified.

---

# Deliverables

When this task is complete, provide:

1. A short summary of what was implemented.
2. The list of files created or modified.
3. The output of:

   * `ruff check .` → All checks passed ✅
   * `pytest` → 3 passed in 0.02s (package imports, CLI --help, no worksheet generation)
4. Any assumptions that were made.
5. Any issues that should be addressed in future tasks.

Do not begin the next task automatically.
