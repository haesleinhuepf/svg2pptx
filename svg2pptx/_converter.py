"""Core SVG-to-PPTX conversion logic."""

import io
from pathlib import Path

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from pptx import Presentation
from pptx.util import Emu


# EMUs per point (1 inch = 914400 EMU = 72 points)
_EMU_PER_POINT = 914400 / 72


def svg_to_pptx(svg_path, pptx_path=None):
    """Convert an SVG file to a PPTX file.

    Parameters
    ----------
    svg_path : str or Path
        Path to the source SVG file.
    pptx_path : str or Path, optional
        Destination path for the PPTX file.  Defaults to the same stem as
        *svg_path* with a ``.pptx`` extension.

    Returns
    -------
    Path
        The path of the created PPTX file.
    """
    svg_path = Path(svg_path)
    if pptx_path is None:
        pptx_path = svg_path.with_suffix(".pptx")
    pptx_path = Path(pptx_path)

    # ------------------------------------------------------------------
    # 1. Read SVG → ReportLab drawing (svglib is BSD-licensed)
    # ------------------------------------------------------------------
    drawing = svg2rlg(str(svg_path))
    if drawing is None:
        raise ValueError(f"Could not read SVG file: {svg_path}")

    width_pt = drawing.width   # points (72 pt = 1 inch)
    height_pt = drawing.height

    # ------------------------------------------------------------------
    # 2. Render drawing to PNG bytes via ReportLab
    # ------------------------------------------------------------------
    png_bytes = renderPM.drawToString(drawing, fmt="PNG")

    # ------------------------------------------------------------------
    # 3. Build PPTX with a single slide sized to match the SVG
    # ------------------------------------------------------------------
    prs = Presentation()

    slide_width = Emu(int(width_pt * _EMU_PER_POINT))
    slide_height = Emu(int(height_pt * _EMU_PER_POINT))
    prs.slide_width = slide_width
    prs.slide_height = slide_height

    blank_layout = prs.slide_layouts[6]  # index 6 is the "Blank" layout
    slide = prs.slides.add_slide(blank_layout)

    slide.shapes.add_picture(
        io.BytesIO(png_bytes),
        left=0,
        top=0,
        width=slide_width,
        height=slide_height,
    )

    prs.save(str(pptx_path))
    return pptx_path
