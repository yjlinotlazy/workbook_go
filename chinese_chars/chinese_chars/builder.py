"""Character Builder (Milestone 4).

Loops over every character and produces cell sequences for each practice mode:

Mode 1 (overlay+tracing): [ref, stroke-1..N, complete...xk] -> fixed-width per char
                          where k = max(0, columns - ref - strokes)
Mode 2 (stroke-blank)   : [ref, stroke-1..N]             -> layout pads with blanks
Mode 3 (tracing-only)   : [ref, complete...x(N)]         -> no progressive overlay

No layout logic: each char block produces its own sequence. Layout handles cross-char padding.
"""

from __future__ import annotations

from chinese_chars.models import Cell, CharacterData, Stroke


class CharacterBuilder:
    """Builds per-character cell sequences from a list of CharacterData."""

    @staticmethod
    def build(chars, mode=1, columns=None):
        """Loop over every char and produce cell sequence based on mode.

        Args:
            chars: list of CharacterData for each character to practice.
            mode: 1=overlay+tracing (default), 2=stroke-blank, 3=tracing-only
            columns: grid column count (used for padding completions in modes 1/3)
        """
        result = []
        for data in chars:
            sequence = CharacterBuilder._one_char(data, mode, columns)
            result.append(sequence)
        return result

    @staticmethod
    def _one_char(char_data, mode, columns):
        """Generate cell sequence for a single character per practice mode."""
        char_strokes = len(char_data.strokes)

        # Compute full character bbox (all strokes combined) - used for consistent stroke normalization
        all_pts = []
        for s in char_data.strokes:
            all_pts.extend(s.points)
        if all_pts:
            min_x = min(p.x for p in all_pts)
            min_y = min(p.y for p in all_pts)
            max_x = max(p.x for p in all_pts)
            max_y = max(p.y for p in all_pts)
            full_bbox = (min_x, min_y, max_x, max_y)
        else:
            full_bbox = None

        # 1. Reference Cell (black, all strokes visible) - common to all modes
        ref_cell = Cell(kind="reference", character_data=char_data, stroke_index=None)

        cells = [ref_cell]

        if mode == 1:
            # Overlay + tracing: ref -> progressive strokes -> completions (if any room)
            cells.extend(
                CharacterBuilder._progressive_strokes(
                    char_data, char_strokes, full_bbox
                )
            )

            # Add traceable grids only if there's leftover column space
            if columns is not None:
                n_remaining = (
                    columns - 1 - char_strokes
                ) % columns  # leave ref cell open
                if n_remaining > 0:
                    complete_data = CharacterData(
                        char=char_data.char,
                        strokes=char_data.strokes,
                        full_bbox=full_bbox,
                    )
                    cells.extend(
                        [
                            Cell(
                                kind="complete",
                                character_data=complete_data,
                                stroke_index=None,
                            )
                        ]
                        * n_remaining
                    )

        elif mode == 2:
            # Stroke -> Blank: ref + progressive only (layout pads with blanks via pad_chars)
            cells.extend(
                CharacterBuilder._progressive_strokes(
                    char_data, char_strokes, full_bbox
                )
            )

        elif mode == 3:
            # Tracing-only: ref + complete grids directly (no step-by-step overlay)
            complete_data = CharacterData(
                char=char_data.char, strokes=char_data.strokes, full_bbox=full_bbox
            )
            if columns is not None and char_strokes > 0:
                cells.extend(
                    [
                        Cell(
                            kind="complete",
                            character_data=complete_data,
                            stroke_index=None,
                        )
                    ]
                    * (columns - 1)
                )

        return cells

    @staticmethod
    def _progressive_strokes(char_data, total_strokes, full_bbox):
        """Generate progressive stroke overlay cells (stroke-1 through stroke-N)."""
        strokes_cells = []
        for i in range(1, total_strokes + 1):
            cumulative_points = char_data.strokes[:i]
            layer_data = CharacterData(
                char=" ", strokes=cumulative_points, full_bbox=full_bbox
            )
            strokes_cells.append(
                Cell(kind=f"stroke-{i}", character_data=layer_data, stroke_index=i)
            )
        return strokes_cells
