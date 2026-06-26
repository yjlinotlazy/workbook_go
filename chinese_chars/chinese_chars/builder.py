"""Character Builder (Milestone 4).

Expands a single `CharacterData` into a sequence of practice cells.
Never performs layout or page logic.
"""

from __future__ import annotations

from chinese_chars.models import Cell, CharacterData, Stroke


class CharacterBuilder:
    """Builds a list of practice Cells from character data + config."""

    @staticmethod
    def build(char_data: CharacterData, repetitions: int) -> list[Cell]:
        """
        Expand one char into cells for practice.

        Sequence per character:
        1. Reference cell (full reference in black).
        2. Progressive "stroke-N" cells (gray overlays) up to total stroke count.
        3. Blank cells for independent practice (based on `repetitions`).
        """
        total_strokes = len(char_data.strokes)
        cells: list[Cell] = []

        # 1. Reference Cell
        ref_cell = Cell(
            kind="reference", 
            character_data=char_data, 
            stroke_index=None
        )
        cells.append(ref_cell)

        # 2. Progressive Stroke Cells
        for i in range(1, total_strokes + 1):
            # Gather points from strokes 1 to i
            cumulative_points: list[Stroke] = char_data.strokes[:i]
            
            # Create a temporary CharacterData just to carry the path layers for the renderer later
            layer_data = CharacterData(char=" ", strokes=cumulative_points)
            
            stroke_cell = Cell(
                kind=f"stroke-{i}",
                character_data=layer_data,
                stroke_index=i
            )
            cells.append(stroke_cell)

        # 3. Blank Cells for independent practice
        for _ in range(repetitions):
            blank_cell = Cell(kind="blank", character_data=None, stroke_index=None)
            cells.append(blank_cell)

        return cells 
