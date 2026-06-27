"""Renderer (Milestone 7).

Converts the structured Workbook data into PDF pages using FPDFv2.
Draws Tian Ge grids, stroke paths, and reference characters.
Coordinates are Top-Left aligned — matching FPDF's native system.
"""

from fpdf import FPDF
from .models import Cell, CharacterData

# Maps our internal paper-size name → FPDF add_page() format string
_PDF_PAGE_FORMAT = {
    "us_letter": "letter",
    "a4": "a4",
}


W_RANGE= 700*2.0
H_RANGE = 500*2.3


class PdfRenderer:
    """Generates a PDF workbook with handwriting practice grids."""

    def __init__(self) -> None:
        self.pdf = FPDF()

        # Attempt to load a CJK-capable font. These are common Linux locations.
        font_paths = {
            "Noto": "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
            "Uming": "/usr/share/fonts/TTF/uming.ttc",
            "Ukai": "/usr/share/fonts/TTF/ukai.ttc"
        }
        for fname, fp in font_paths.items():
            try:
                self.pdf.add_font(fname, fname=fp)
            except FileNotFoundError:
                print("Fail to add", fname)

    def render(self, workbook) -> bytes:
        """Convert the entire workbook into a PDF byte stream."""

        # Convert internal paper size name → FPDF add_page format string
        fpdf_fmt = _PDF_PAGE_FORMAT.get(
            workbook.config.paper_size,
            "letter"  # fallback
        )

        for page in workbook.pages:

            self.pdf.add_page(format=fpdf_fmt)
            self.pdf.set_text_color(0, 0, 0)



            for row in page.rows:
                for cell_obj in row.cells:
                    if not hasattr(cell_obj, 'geometry') or cell_obj.geometry is None:
                        print("invalid cell")
                        continue

                    g = cell_obj.geometry

                    # --- Draw Tian Ge Grid (Outer Box) ---
                    self.pdf.set_draw_color(200, 50, 50)
                    self.pdf.set_line_width(0.4)

                    self.pdf.rect(g.x, g.y, g.w, g.h)

                    # --- Draw Inner Cross-hairs (Dashed) ---
                    self.pdf.set_draw_color(255, 100, 100)
                    self.pdf.set_line_width(0.3)

                    mid_x = g.x + (g.w / 2)
                    mid_y = g.y + (g.h / 2)

                    # Apply dash pattern
                    self.pdf.set_dash_pattern(dash=4, gap=8)
                    self.pdf.line(mid_x, g.y, mid_x, g.y + g.h)
                    self.pdf.line(g.x, mid_y, g.x + g.w, mid_y)

                    # Reset dash pattern to solid
                    self.pdf.set_dash_pattern()

                    # --- Draw Progressive Strokes (Gray overlay) ---
                    if cell_obj.kind.startswith('stroke-') and cell_obj.character_data:
                        cd = cell_obj.character_data
                        if cd.strokes:
                            min_x = min(p.x for stroke in cd.strokes for p in stroke.points)
                            min_y = min(p.y for stroke in cd.strokes for p in stroke.points)
                            max_x = max(p.x for stroke in cd.strokes for p in stroke.points)
                            max_y = max(p.y for stroke in cd.strokes for p in stroke.points)

                        self.pdf.set_draw_color(150, 150, 150) # Light gray
                        self.pdf.set_line_width(0.6)

                        for stroke in cd.strokes:
                            prev_x_pdf = None
                            prev_y_pdf = None

                            for p in stroke.points:
                                # Source coords (Bottom-Left origin) → PDF coords (Top-Left origin):
                                # X unchanged, Y flipped.
                                nx = g.x + ((p.x - min_x) / W_RANGE) * g.w + g.w * 0.2
                                ny = g.y + ((max_y - p.y) / H_RANGE) * g.h + g.h * 0.2

                                if prev_x_pdf is not None:
                                    self.pdf.line(prev_x_pdf, prev_y_pdf, nx, ny)

                                prev_x_pdf = nx
                                prev_y_pdf = ny

                    # --- Draw Reference Character (Black) ---
                    elif cell_obj.kind == 'reference':
                        char = cell_obj.character_data.char if cell_obj.character_data else ""
                        if char:
                            # Dynamically scale font size to match current grid density
                            dyn_font_size = int(g.h * 2)
                            self.pdf.set_font("Ukai", size=dyn_font_size)

                            cx = g.x + (g.w / 7)
                            # FPDF Y is baseline position; adjust for font height so char centers in box
                            cy = g.y + (g.h * 0.5) + (dyn_font_size / 6)
                            self.pdf.text(cx, cy, char)

        return self.pdf.output()
