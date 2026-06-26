"""Workbook Generator (Milestone 5).

Combines StrokeLoader and CharacterBuilder to produce practice content.
No layout logic (pages/rows) lives here.
"""

from .models import Cell, Config
from .stroke import StrokeFileLoader
from .builder import CharacterBuilder


class WorkbookGenerator:
    """Generates the full sequence of cells for a workbook based on config."""

    def generate_content(self, config: Config) -> list[list[Cell]]:
        """
        Generate a flat list of all practice cells from configuration.

        Characters are simply streamed left-to-right, one after another. They will
        span exactly as many rows as their content requires without any rigid
        column-padding or forced horizontal alignment. The final layout will be
        handled by the layout module.
        """
        loader = StrokeFileLoader()
        total_cells: list[Cell] = []

        for char in config.chars:
            data = loader.load(char)

            # Build the full sequence: Reference + Strokes + `-r` blank practice cells
            sequence = CharacterBuilder.build(data)
            total_cells.append(sequence)

        return total_cells
