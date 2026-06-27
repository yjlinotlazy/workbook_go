"""Layout Engine (Milestone 6).

Converts a sequence of char cell blocks into Pages and Rows based on configuration.

Architecture:
1. pad_chars: each char block → padded to config.columns blank cells at end
2. flatten: all char blocks (per page) merged into flat sequence
3. pad_rows: fill incomplete last row with blanks
4. cells_to_rows: flat list → Row objects with geometry
5. build: ties it all together, handling page boundaries
"""

from chinese_chars.models import Cell, Config, Page, Row, Workbook, CellGeometry


# Standard millimeter equivalents for common print margins
def _inch_to_mm(inches: float) -> float:
    return inches * 25.4


class LayoutEngine:
    """Arranges practice cells into pages according to page size and grid rules.

    Coordinates are generated in millimeters (mm). FPDF (the PDF backend)
    defaults to millimeters, so these geometry values map 1:1 directly
    onto the renderer's canvas without clipping or scaling issues.

    Input contract: list[list[Cell]] where each inner list is one character's
    cells (ref + strokes), produced by generator.generate_content().
    Output: tuple[Page, ...] — fully laid out with geometry.
    """

    def __init__(self, config: Config) -> None:
        self.config = config

        # Paper dimensions in millimeters (FPDF native standard)
        if config.paper_size == "us_letter":
            self.paper_w = 215.9   # 8.5 inches
            self.paper_h = 279.4   # 11.0 inches
        else:
            self.paper_w = 210.0   # A4 width
            self.paper_h = 297.0   # A4 height

        # Standard layout margins (e.g., 0.5 inch or 13mm)
        self.margin = _inch_to_mm(0.5)

        # Calculate grid cell size dynamically so Tian Ge boxes remain perfectly square
        step_w = (self.paper_w - (2 * self.margin)) / self.config.columns
        row_h = step_w

        # How many full rows fit on the page given dynamic cell size and margins
        available_height = self.paper_h - (2 * self.margin)
        self.rows_per_page = int(available_height / row_h)
        self.cell_size_mm = step_w

    def pad_chars(self, char_blocks: list[list[Cell]]) -> list[list[Cell]]:
        """Pad each character block to config.columns length with blank cells.

        Each inner list (one character's cells) gets extended with blanks until
        it reaches exactly self.config.columns items. This ensures every character
        occupies full grid columns on the page.

        Note: each char is padded independently — no accumulation.
        """
        blank_cell = Cell(kind="blank", character_data=None, stroke_index=None)

        for cells in char_blocks:
            n = len(cells)
            if n < self.config.columns:
                for _ in range(self.config.columns - n):
                    cells.append(blank_cell)
        return char_blocks

    def flatten(self, char_blocks: list[list[Cell]]) -> list[Cell]:
        """Flatten a sequence of character blocks into a single cell list."""
        flat: list[Cell] = []
        for block in char_blocks:
            flat.extend(block)
        return flat

    def cells_to_rows(self, flat_cells: list[Cell], page_start_row: int = 0) -> tuple[Row, ...]:
        """Turn a flat list of cells into Row objects with geometry attached.

        Slices `flat_cells` into chunks of self.config.columns, attaches cell
        coordinates (mm) to each CellGeometry, and returns a tuple of Row.

        Args:
            flat_cells: all cells for one page, in writing order
            page_start_row: global row offset (for multi-page workbooks)
        """
        cols = self.config.columns
        step_w = self.cell_size_mm
        gap = 2  # mm gap between adjacent Tian Ge boxes

        rows: list[Row] = []
        row_idx = page_start_row  # start from page_offset for correct coord

        for chunk_start in range(0, len(flat_cells), cols):
            batch = flat_cells[chunk_start : chunk_start + cols]
            if len(batch) < cols:
                break  # partial row — should be handled by padding before calling this

            row_cells: list[Cell] = []

            for col_idx, raw_cell in enumerate(batch):
                x = self.margin + (col_idx) * step_w
                y = self.margin + (row_idx) * (step_w + gap)

                new_geo = CellGeometry(
                    x=x,
                    y=y,
                    w=step_w - 4,   # 2mm padding on each side for Tian Ge box
                    h=step_w - 4,
                )

                row_cells.append(Cell(
                    kind=raw_cell.kind,
                    character_data=raw_cell.character_data,
                    stroke_index=raw_cell.stroke_index,
                    geometry=new_geo,
                ))
            rows.append(Row(index=row_idx, cells=tuple(row_cells)))
            row_idx += 1

        return tuple(rows)

    def _pad_to_full_page(self, flat_cells: list[Cell]) -> list[Cell]:
        """Pad flat cell list to fill the entire page grid (full last rows)."""
        cells_per_page = self.config.columns * self.rows_per_page
        if len(flat_cells) >= cells_per_page:
            return flat_cells

        remaining = cells_per_page - len(flat_cells)
        cols = self.config.columns
        for _ in range(remaining):
            flat_cells.append(Cell(kind="blank", character_data=None, stroke_index=None))
        return flat_cells

    def build(self, char_blocks: list[list[Cell]]) -> tuple[Page, ...]:
        """Generate full page sequence from character cell blocks.

        Flow per page:
          1. Select chars for this page (rows_per_page chars)
          2. pad_chars → each char block padded to config.columns blanks
          3. flatten → single flat list for the page
          4. _pad_to_full_page → fill incomplete last rows with blanks
          5. cells_to_rows → Row objects with mm coordinates

        Args:
            char_blocks: list[list[Cell]] — one inner list per character
                        (from generator.generate_content)
        """
        if not char_blocks:
            return ()

        cols = self.config.columns
        rows_per_page = self.rows_per_page
        pages: list[Page] = []

        for page_idx, start in enumerate(range(0, len(char_blocks), rows_per_page)):
            # Step 1: Select all character blocks for this logical page
            page_char_blocks = char_blocks[start : start + rows_per_page]

            # Step 2 & 3: Pad each char block → flatten
            padded = self.pad_chars(page_char_blocks)
            flat = self.flatten(padded)

            # Step 4: Fill incomplete last rows with blank cells
            flat_padded = self._pad_to_full_page(flat)

            # Step 5: Convert to Row objects with geometry
            global_row_offset = page_idx * rows_per_page
            current_page_rows = self.cells_to_rows(flat_padded, global_row_offset)

            pages.append(Page(
                number=page_idx + 1,
                rows=tuple(current_page_rows),
                width_cells=cols
            ))

        return tuple(pages)


def layout_cells(config: Config, char_blocks: list[list[Cell]]) -> Workbook:
    """High-level API to convert character blocks into a structured Workbook.

    Input: list[list[Cell]] where each inner list = one character's
           ref+strokes (from generator.generate_content).

    Flow:
      - Pad each character block to columns blanks per pad_chars()
      - Group chars by pages_per_row → flatten into page-level cells
      - cells_to_rows() → attach mm coordinates → construct Page objects
    """
    engine = LayoutEngine(config)
    pages = engine.build(char_blocks)

    return Workbook(
        title=config.chars,
        config=config,
        pages=pages  # tuple[Page, ...] with full geometry
    )
