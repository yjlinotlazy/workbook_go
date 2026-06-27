"""Character Builder (Milestone 4).

Loops over every character and produces [[ref, st1,...], ...]
for each char's practice sequence. No grid padding — layout handles that.
"""

from __future__ import annotations

from chinese_chars.models import Cell, CharacterData, Stroke


class CharacterBuilder:
    """Builds per-character cell sequences from a list of CharacterData."""

    @staticmethod
    def build(chars: list[CharacterData]) -> list[list[Cell]]:
        """Loop over every char and produce [[ref, st1,...], ...] for each.

        Only produces cells whose strokes are already defined on `char_data`.
        NO blank practice cells — layout pads to grid columns / adds blanks.
        """
        result: list[list[Cell]] = []
        for data in chars:
            sequence = CharacterBuilder._one_char(data)
            result.append(sequence)
        return result

    @staticmethod
    def _one_char(char_data: CharacterData) -> list[Cell]:
        cells: list[Cell] = []
        total_strokes = len(char_data.strokes)

        # Compute full character bbox (all strokes combined) — used for consistent stroke normalization
        all_pts: list[StrokePoint] = []
        for s in char_data.strokes:
            all_pts.extend(s.points)
        if all_pts:
            min_x = min(p.x for p in all_pts)
            min_y = min(p.y for p in all_pts)
            max_x = max(p.x for p in all_pts)
            max_y = max(p.y for p in all_pts)
            full_bbox: tuple[float, float, float, float] | None = (min_x, min_y, max_x, max_y)
        else:
            full_bbox = None

        # 1. Reference Cell (black, all strokes visible)
        ref_cell = Cell(
            kind="reference",
            character_data=char_data,
            stroke_index=None
        )
        cells.append(ref_cell)

        # 2. Progressive Stroke Cells 
        for i in range(1, total_strokes + 1):
            cumulative_points: list[Stroke] = char_data.strokes[:i]
            # Embed full_bbox so renderer can normalize all progressive cells consistently
            layer_data = CharacterData(
                char=" ", 
                strokes=cumulative_points,
                full_bbox=full_bbox
            )
            
            stroke_cell = Cell(
                kind=f"stroke-{i}",
                character_data=layer_data,
                stroke_index=i
            )
            cells.append(stroke_cell)
        return cells
