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
        Generate grouped practice cells: one inner list per character.
        Layout handles blank-cell insertion and row/column padding.
        """
        loader = StrokeFileLoader()
        char_data_list = [loader.load(char) for char in config.chars]

        # Pass mode + columns to CharacterBuilder
        return CharacterBuilder.build(char_data_list, mode=config.mode, columns=config.columns)
