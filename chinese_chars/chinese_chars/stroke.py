"""Stroke loading module.

Reads stroke data from Chinese Chars' internal JSON storage format
defined in `DATA_PIPELINE.md`. Never reads external third-party files.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .models import CharacterData, Stroke, StrokePoint


#: Directory where valid, imported character data lives
INTERNAL_STORAGE_DIR = Path(__file__).resolve().parent.parent / "data"


class StrokeFileLoader:
    """Loads stroke information from Chinese Chars' internal JSON storage."""

    def __init__(self, storage_dir: Path | None = None) -> None:
        """Initialize the loader with a custom storage directory (optional)."""
        self.storage_dir = storage_dir or INTERNAL_STORAGE_DIR

    def load(self, char: str) -> CharacterData:
        """Load `CharacterData` for `char` from disk. Raises KeyError if not found."""
        filepath = self._get_filepath(char)

        if not filepath.exists():
            raise KeyError(f"Stroke data not found for `{char}` at {filepath}")

        raw_data: Dict[str, Any] = json.loads(filepath.read_text(encoding="utf-8"))
        return self._parse_internal_json(raw_data)

    def has_char(self, char: str) -> bool:
        """Check if internal storage contains data for `char`."""
        filepath = self._get_filepath(char)
        if filepath.exists():
            return True
        # Fallback: check generated/characters subdirectory
        fallback = INTERNAL_STORAGE_DIR / "generated" / "characters" / f"{char}.json"
        return fallback.exists()

    def _get_filepath(self, char: str) -> Path:
        """Get the path to the JSON file for `char`.
        
        Search order:
          1. Custom storage_dir (if provided)
          2. generated/characters/<char>.json (new importer output with medians)
          3. INTERNAL_STORAGE_DIR/<char>.json (legacy, fallback)
        """
        if self.storage_dir != INTERNAL_STORAGE_DIR:
            return self.storage_dir / f"{char}.json"
        
        # Prefer generated/characters (new importer with medians) over legacy
        generated = INTERNAL_STORAGE_DIR / "generated" / "characters" / f"{char}.json"
        if generated.exists():
            return generated
        
        legacy = INTERNAL_STORAGE_DIR / f"{char}.json"
        return legacy

    def _parse_internal_json(self, data: Dict[str, Any]) -> CharacterData:
        """Convert raw JSON dictionary into a `CharacterData` model."""
        char_name = data.get("character", "unknown")
        if not isinstance(char_name, str):
            raise ValueError("'character' field in internal JSON must be a string.")

        strokes_raw = data.get("strokes", [])

        if not isinstance(strokes_raw, list):
            raise ValueError("'strokes' field must be an array.")

        valid_strokes: List[Stroke] = []
        for item in strokes_raw:
            stroke_path = self._parse_stroke_entry(item)
            if stroke_path is not None:
                valid_strokes.append(stroke_path)

        return CharacterData(char=char_name, strokes=valid_strokes)

    def _parse_stroke_entry(self, raw_item: Any) -> Stroke | None:
        """
        Parses a single stroke entry from internal JSON.
        
        Priority: if 'medians' (centerline) field exists, use it.
        Otherwise fall back to the thick filled 'path' as-is.
        Internal path format is flat coordinates: [x1, y1, x2, y2, ...].
        """
        if not isinstance(raw_item, dict):
            return None  # Skip malformed items gracefully

        entry_path = raw_item.get("path")
        
        if "order" not in raw_item or "path" not in raw_item:
            raise ValueError(f"Invalid stroke entry missing 'order' or 'path': {raw_item}")

        if not isinstance(entry_path, list):
            raise ValueError(f"'path' must be a list of numbers. Found {type(entry_path)}")

        # Prefer medians (centerline) over thick filled contour for cleaner rendering
        use_coords = raw_item.get("medians", entry_path)

        points: List[StrokePoint] = []

        # Ensure all path coordinates are float-compatible.
        try:
            flat_points: List[float] = [float(p) for p in use_coords]
        except (ValueError, TypeError):
            raise ValueError(f"'path' must contain numeric coordinates. Found {use_coords}")

        n_coord_pairs = len(flat_points) // 2
        if len(flat_points) % 2 != 0:
            raise ValueError("Path coordinates must form [x,y] pairs.")

        # Normalize `t` logic for the current stroke (goes from 0.0 to 1.0).
        total_steps = n_coord_pairs - 1 if n_coord_pairs > 1 else 1

        for i in range(n_coord_pairs):
            tx = flat_points[i * 2]
            ty = flat_points[i * 2 + 1]

            # `t` is the normalized progression along this specific stroke path.
            t_val = i / total_steps if total_steps > 0 else 0.0

            points.append(StrokePoint(t=t_val, x=tx, y=ty))

        return Stroke(points=points) if points else None
