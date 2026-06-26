"""Layout Engine (Milestone 6).

Converts a flat sequence of Cells into Pages and Rows based on configuration.
Calculates geometric coordinates for the renderer in millimeters (mm), which matches
FPDF's default unit system natively. No coordinate scaling is required between
layers, ensuring Tian Ge grids and page breaks map perfectly to physical output.
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
        # `step_w` is the exact width allocated for a single column based on -c
        step_w = (self.paper_w - (2 * self.margin)) / self.config.columns

        # Grid boxes are strictly square; row height equals cell width
        row_h = step_w

        # Calculate how many full rows fit on the page given the dynamic cell size and margins
        available_height = self.paper_h - (2 * self.margin)
        self.rows_per_page = int(available_height / row_h)
        self.cell_size_mm = step_w

    def pad_chars(self, char_cells: list[list[Cell]]) -> list[list[Cell]]:
        """
        Pad characters into rows with equal length.
        [char1_cells, char2_cells] will become
        [padded_char1_cells, padded_char2_cells]
        """
        blank_cell = Cell(kind="blank", character_data=None, stroke_index=None)

        for cells in char_cells:
            n = len(cells)
            # pad n to the end of the row. If one row is not sufficient, pad to the next row
            pad_to = self.config.columns
            while pad_to - n < 0:
                pad_to += pad_to
            for i in range(pad_to - n):
                cells.append(blank_cell)
        return char_cells

    def cells_to_rows(self, cells: list[Cells]) -> list[list[Cell]]:
        """
        turn a flat list of cells into rows of cells. You might find the following
        snippet helpful:
            new_geo = CellGeometry(
                x=x_start,
                y=y_base,
                w=step_w - 4,   # 2mm padding on each side for the Tian Ge box
                h=row_h - 4
            )

            row_cells_raw.append(Cell(
                kind=raw_cell.kind,
                character_data=raw_cell.character_data,
                stroke_index=raw_cell.stroke_index,
                geometry=new_geo
            ))
        """
        pass

    def build(self, char_cells: list[list[Cell]]) -> tuple[Page, ...]:
        """Generates the full Workbook structure with geometry attached to each Cell."""
        total_cells = len(char_cells)
        if total_cells == 0:
            return ()

        cells_per_page = self.config.columns * self.rows_per_page
        pages: list[Page] = []

        queue = self.pad_chars(char_cells)

        # step_w / row_h are derived in __init__ and locked to config columns/paper size
        step_w = self.cell_size_mm
        row_h = self.cell_size_mm

        current_page_cells = []
        page_row_count = 0
        page_idx = 0
        while(queue):
            candidate = queue[-1]
            row_count = len(candidate) / self.config.columns
            # if it can fit, add to the current page
            if row_count + page_row_count <= self.rows_per_page:
                page_row_count += row_count
                current_page_cells.extend(queue.pop())
            if len(curr_page_cells) == cells_per_page:
                current_page_rows = self.cells_to_rows(current_page_cells)
                pages.append(Page(
                    number=page_idx,
                    rows=tuple(current_page_rows),
                    width_cells=self.config.columns
                ))
                page_idx += 1
                current_page_cells = []
                page_row_count = 0
        if curr_page_cells:
            current_page_rows = self.cells_to_rows(current_page_cells)
            pages.append(Page(
                number=page_idx,
                rows=tuple(current_page_rows),
                width_cells=self.config.columns
            ))
        return tuple(pages)


def layout_cells(config: Config, char_cells: list[list[Cell]]) -> Workbook:
    """High-level API to convert flat cells into a structured Workbook."""
    engine = LayoutEngine(config)
    pages = engine.build(char_cells)

    return Workbook(
        title=config.chars,
        config=config,
        pages=pages
    )
