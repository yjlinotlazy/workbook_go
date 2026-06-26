# IMPORTER.md

# Import Pipeline

## Philosophy

Chinese Chars must **never depend directly on third-party data formats**.

External datasets are considered **raw data**, not part of Chinese Chars' internal architecture.

Business logic must never parse third-party files directly.

Instead, every external dataset must first be imported into Chinese Chars' own internal data format.

The import process is a one-time conversion.

```text
External Dataset
        │
        ▼
Importer
        │
        ▼
Chinese Chars Internal Data
        │
        ▼
StrokeLoader
        │
        ▼
CharacterBuilder
        │
        ▼
Renderer
```

Only the Importer understands external formats.

Everything else only understands the internal model.

---

# Why

Suppose the project initially uses MakeMeAHanzi.

The raw dataset may contain

* SVG paths
* medians
* decomposition
* radical information
* metadata
* version-specific fields

Chinese Chars does not need most of this information.

If business logic reads these files directly, every module becomes tightly coupled to the dataset.

If the dataset changes, the entire application must change.

Instead, only the Importer understands the third-party format.

---

# Responsibilities

## Importer

Responsible for

* reading external datasets
* validating data
* converting formats
* discarding unnecessary fields
* generating Chinese Chars internal data

The Importer runs only when data is updated.

It is **not** used during normal worksheet generation.

---

## StrokeLoader

StrokeLoader never reads third-party files.

StrokeLoader only loads Chinese Chars internal data.

It should not know about

* MakeMeAHanzi
* Hanzi Writer
* external JSON layouts
* SVG package formats

---

# Internal Data Format

Chinese Chars defines its own internal representation.

Example

```json
{
  "character": "永",
  "stroke_count": 8,
  "strokes": [
    {
      "order": 1,
      "path": "..."
    },
    {
      "order": 2,
      "path": "..."
    }
  ]
}
```

Additional fields may be added in the future without affecting external datasets.

---

# Directory Structure

```text
data/

    raw/
        makemeahanzi/
            graphics.txt
            dictionary.txt

    generated/
        characters/
            一.json
            二.json
            三.json
            永.json
```

Raw data is never modified.

Generated data may be regenerated at any time.

---

# Import Command

Example

```bash
python scripts/import_makemeahanzi.py
```

The command should

1. Read raw files.
2. Validate input.
3. Convert into the internal model.
4. Write generated data.

Running the importer multiple times should produce identical results.

---

# Business Code Rules

Business logic must never

* open graphics.txt
* parse third-party JSON
* inspect external field names

Business logic should only call

```python
character = stroke_loader.load("永")
```

Nothing else.

---

# Future Data Sources

Chinese Chars should be able to replace the source dataset without changing business logic.

Possible future sources include

* First try: MakeMeAHanzi: already downloaded to /home/yli/Dropbox/github/makemeahanzi
* Other candidates
  * Hanzi Writer
  * custom SVG datasets
  * commercial font datasets
  * user-generated stroke data

Adding a new data source should require writing a new Importer only.

No changes should be required to

* CharacterBuilder
* LayoutEngine
* Renderer

---

# Importer Design Rules

An Importer should

* be deterministic
* validate input
* fail loudly on malformed data
* never silently discard errors
* generate reproducible output

Importers should not perform workbook generation.

Importers should not render graphics.

Importers should only transform data.

---

# Internal Model Is the Source of Truth

Once imported, Chinese Chars should operate exclusively on its internal data model.

No runtime code should depend on the original external dataset.

This separation keeps the codebase stable, simplifies testing, and makes it easy to replace or upgrade external data sources in the future.
