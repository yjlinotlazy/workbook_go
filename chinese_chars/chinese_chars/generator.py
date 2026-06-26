"""Workbook Generator (Milestone 5).

Combines StrokeLoader and CharacterBuilder to produce practice content.
No layout logic (pages/rows) lives here.
"""

from chinese_chars.models import Cell, Config
from chinese_chars.stroke import StrokeFileLoader
from chinese_chars.builder import CharacterBuilder


class WorkbookGenerator:
    """Generates the full sequence of cells for a workbook based on config."""

    def generate_content(self, config: Config) -> list[Cell]:
        """Generate a flat list of all practice cells from configuration."""
        loader = StrokeFileLoader()
        total_cells: list[Cell] = []

        for char in config.chars:
            data = loader.load(char)
            
            # Build the row/sequence of cells for this character
            char_sequence = CharacterBuilder.build(data, config.repetitions)
            total_cells.extend(char_sequence)
            
        return total_cells 
