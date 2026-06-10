# svg2pptx

A pip-installable Python tool that converts SVG files to PowerPoint (PPTX) presentations.

## Installation

```bash
pip install svg2pptx
```

## Usage

### Command line

```bash
svg2pptx input.svg
# → creates input.pptx

svg2pptx2 input.svg output.pptx
# → creates output.pptx
```

### Python API

```python
from svg2pptx import svg_to_pptx

svg_to_pptx("diagram.svg")               # creates diagram.pptx
svg_to_pptx("diagram.svg", "slide.pptx") # custom output path
```

## How it works

1. Reads the SVG using [svglib](https://github.com/deeplook/svglib) (BSD-licensed).
2. Renders it to a PNG via [ReportLab](https://www.reportlab.com/).
3. Embeds the PNG in a single-slide PPTX whose dimensions match the SVG, using [python-pptx](https://python-pptx.readthedocs.io/).

## License

BSD-3-Clause
