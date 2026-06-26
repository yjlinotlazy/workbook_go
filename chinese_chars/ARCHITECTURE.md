# Workbook Go Architecture

## Philosophy

Workbook Go is a worksheet generator.

The core responsibility of the project is to transform user requests into a device-independent workbook model.

The Generator produces a renderer-independent Workbook model. Rendering that model to PDF is the responsibility of the Renderer. This separation allows future support for additional output formats (such as SVG or PNG) without changing workbook generation logic.

The data flow is strictly one-way.

```
CLI
    ↓
Generator
    ↓
Workbook Model
    ↓
Renderer
    ↓
Output File
```

Every layer only depends on the layer below it.

---

# Design Principles

## Single Responsibility

Every module has exactly one responsibility.

Examples:

* CLI parses command line arguments.
* Generator builds workbook data.
* Layout decides where every cell is placed.
* Renderer draws graphics.
* StrokeLoader loads stroke data.

No module should perform multiple unrelated jobs.

---

## Renderer Knows Nothing

Renderer does NOT know Chinese.

Renderer does NOT know stroke order.

Renderer does NOT know workbook logic.

Renderer only knows how to draw graphical objects.

Renderer accepts a Workbook object and renders it.

---

## Layout Knows Nothing

Layout never loads stroke data.

Layout never reads dictionaries.

Layout never decides practice order.

Layout only arranges Cells into Rows and Pages.

---

## Generator Owns Business Logic

Generator is the heart of the application.

Generator is responsible for

* reading configuration
* loading stroke information
* creating practice cells
* generating blank cells
* producing the Workbook

All workbook rules belong here.

---

# Layers

```
CLI
│
├── parse arguments
├── validate arguments
└── call Generator
```

↓

```
Generator
│
├── StrokeLoader
├── CharacterBuilder
├── LayoutEngine
└── Workbook
```

↓

```
Renderer
│
├── PDF
├── SVG
└── PNG
```

---

# Data Model

The project revolves around the Workbook model.

```
Workbook

    Pages

        Rows

            Cells
```

A Cell contains graphical information only.

Example:

```
Cell

background

foreground

hint
```

Renderer only draws these components.

---

# Character Builder

CharacterBuilder converts one character into many Cells.

Example:

Character

```
永
```

↓

```
Reference Cell

Stroke 1

Stroke 1-2

Stroke 1-3

...

Blank

Blank

Blank
```

CharacterBuilder never performs page layout.

---

# Stroke Model

Stroke information should be represented in a renderer-independent format.

Example:

```
Character

    strokes

        Stroke

            order

            path
```

SVG, font outlines, or external data should all be converted into this common representation.

---

# Layout

Input

```
List[Cell]
```

Output

```
Workbook
```

Layout is responsible for

* page size
* rows
* columns
* margins
* page breaks

Layout never modifies Cell contents.

---

# Renderer

Renderer receives a completed Workbook.

Renderer must not modify Workbook.

Renderer must not perform business logic.

Renderer simply draws.

Pseudo-code

```
for page

    for row

        for cell

            draw background

            draw foreground

            draw hint
```

---

# CLI

CLI should stay as small as possible.

Responsibilities

* parse arguments
* validate arguments
* build Config
* invoke Generator
* invoke Renderer

CLI should never contain workbook logic.

---

# Configuration

Configuration should be immutable after creation.

Example

```
Config

characters

cells_per_row

page_size

output_file

font

grid_style
```

Every module receives Config instead of global variables.

---

# Error Handling

Errors should be detected as early as possible.

Examples

* invalid character
* missing stroke data
* unsupported font
* invalid page size

Do not silently ignore errors.

Return descriptive exceptions.

---

# Testing Strategy

Every module should be independently testable.

Recommended unit tests

```
CLI

StrokeLoader

CharacterBuilder

Layout

Renderer
```

Avoid tests that require the entire application.

---

# Coding Style

Prefer small functions.

Target function length

10–40 lines

Target file size

<500 lines

Avoid giant classes.

Avoid global state.

Avoid circular imports.

Use dataclasses whenever possible.

Prefer composition over inheritance.

---

# LLM Development Rules

This repository is intended to be developed with local LLMs.

When implementing features:

1. Only modify the files required by the current task.

2. Do not refactor unrelated modules.

3. Do not rename public APIs unless explicitly requested.

4. Preserve the layer boundaries.

5. If a change crosses multiple layers, implement one layer at a time.

6. Add tests for every new feature.

7. Never duplicate business logic.

8. Never move business logic into Renderer.

9. Keep commits small and focused.

---

# Future Extensions

The architecture should support future worksheet types without changing the core.

Possible future generators

* English handwriting
* Numbers
* Pinyin
* Math worksheets
* Mazes
* Cutting practice
* Coloring pages
* Copy writing
* Calligraphy

While you don't need to worry too much about supporting those, you should choose
variable/method/class namings to be generic, to avoid future refactoring.

Only new Generators should be required. Renderer and Layout should remain reusable.
