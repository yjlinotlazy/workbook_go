"""Layout Engine (Milestone 6 & M7 integration).

Converts a flat sequence of Cells into Pages and Rows based on configuration,
calculating geometric coordinates for the renderer. Coordinates are Top-Left
relative to page — matching FPDF's native coordinate system.
"""

from chinese_chars.models import Cell, Config, Page, Row, Workbook, CellGeometry


class LayoutEngine:
    """Arranges practice cells into pages according to page size and grid rules."""

    def __init__(self, config: Config) -> None:
        self.config = config
        # Paper sizes in points (FPDF standard)
        self.paper_w = 612.0 if config.paper_size == "us_letter" else 595.28
        self.paper_h = 792.0 if config.paper_size == "us_letter" else 841.89
        self.margin = 36  # standard 0.5 inch margin
        
        # Calculate grid size dynamically so Tian Ge boxes remain roughly square
        step_w = (self.paper_w - (2 * self.margin)) / self.config.columns
        
        # Grid boxes are square; row height equals cell width
        row_h = step_w
        self.rows_per_page = int((self.paper_h - (2 * self.margin)) / row_h)
        self.cell_size = step_w
        
    def build(self, cells: list[Cell]) -> tuple[Page, ...]:
        """Generates the full Workbook structure with geometry attached to each Cell."""
        total_cells = len(cells)
        if total_cells == 0:
            return ()

        cells_per_page = self.config.columns * self.rows_per_page
        pages: list[Page] = []
        
        # step_w / row_h are already set in __init__ to keep Tian Ge boxes square
        step_w = self.cell_size
        row_h = self.cell_size

        for i in range(0, total_cells, cells_per_page):
            page_idx = len(pages) + 1
            batch = cells[i : i + cells_per_page]
            
            current_page_rows = []
            
            for r in range(self.rows_per_page):
                row_cells_raw = []
                
                # Y grows DOWNWARD from top margin (FPDF native)
                y_base = self.margin + (r * row_h)
                
                if i + r >= total_cells:
                    break
                
                for c in range(self.config.columns):
                    global_cell_idx = i + r * self.config.columns + c
                    
                    if global_cell_idx < total_cells:
                        raw_cell = cells[global_cell_idx]
                        
                        x_start = self.margin + (c * step_w)
                        
                        new_geo = CellGeometry(
                            x=x_start,
                            y=y_base,
                            w=step_w - 4,
                            h=row_h - 4
                        )
                        
                        row_cells_raw.append(Cell(
                            kind=raw_cell.kind,
                            character_data=raw_cell.character_data,
                            stroke_index=raw_cell.stroke_index,
                            geometry=new_geo
                        ))

                if not row_cells_raw:
                    break
                    
                current_page_rows.append(Row(index=r, cells=tuple(row_cells_raw)))
            
            pages.append(Page(
                number=page_idx,
                rows=tuple(current_page_rows),
                width_cells=self.config.columns
            ))
        
        return tuple(pages)


def layout_cells(config: Config, cells: list[Cell]) -> Workbook:
    """High-level API to convert flat cells into a structured Workbook."""
    engine = LayoutEngine(config)
    pages = engine.build(cells)
    
    from chinese_chars.models import Workbook
    return Workbook(
        title=config.chars,
        config=config,
        pages=pages
    )
