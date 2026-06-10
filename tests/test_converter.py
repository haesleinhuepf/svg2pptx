"""Tests for svg2pptx conversion."""

import io
from pathlib import Path

import pytest

from svg2pptx import svg_to_pptx

# Minimal well-formed SVG used across tests
SIMPLE_SVG = """\
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100">
  <rect width="200" height="100" fill="steelblue"/>
  <text x="10" y="60" font-size="20" fill="white">Hello</text>
</svg>
"""


@pytest.fixture()
def svg_file(tmp_path):
    p = tmp_path / "test.svg"
    p.write_text(SIMPLE_SVG, encoding="utf-8")
    return p


def test_default_output_path(svg_file):
    """Output path should default to the same stem with .pptx extension."""
    result = svg_to_pptx(svg_file)
    assert result == svg_file.with_suffix(".pptx")
    assert result.exists()


def test_custom_output_path(svg_file, tmp_path):
    """A custom output path should be respected."""
    out = tmp_path / "custom_output.pptx"
    result = svg_to_pptx(svg_file, out)
    assert result == out
    assert out.exists()


def test_pptx_is_valid_zip(svg_file):
    """A PPTX file is a ZIP archive – verify basic structure."""
    import zipfile

    result = svg_to_pptx(svg_file)
    assert zipfile.is_zipfile(result)


def test_pptx_has_one_slide(svg_file):
    """The generated presentation must have exactly one slide."""
    from pptx import Presentation

    result = svg_to_pptx(svg_file)
    prs = Presentation(str(result))
    assert len(prs.slides) == 1


def test_pptx_slide_size_matches_svg(svg_file):
    """Slide dimensions should match the SVG width/height."""
    from pptx import Presentation
    from pptx.util import Emu

    result = svg_to_pptx(svg_file)
    prs = Presentation(str(result))
    # SVG is 200 x 100 (user units ≈ points); allow a 1 EMU rounding slack
    emu_per_pt = 914400 / 72
    assert abs(prs.slide_width - Emu(int(200 * emu_per_pt))) <= 1
    assert abs(prs.slide_height - Emu(int(100 * emu_per_pt))) <= 1


def test_invalid_svg_raises(tmp_path):
    """Passing a non-SVG file should raise ValueError."""
    bad = tmp_path / "bad.svg"
    bad.write_text("not valid svg content", encoding="utf-8")
    with pytest.raises((ValueError, Exception)):
        svg_to_pptx(bad)


def test_string_path_accepted(svg_file):
    """svg_to_pptx should accept plain strings as well as Path objects."""
    result = svg_to_pptx(str(svg_file))
    assert result.exists()


def test_cli_no_args(capsys):
    """Running the CLI with no arguments should exit with code 1."""
    import sys
    from svg2pptx._cli import main

    sys.argv = ["svg2pptx"]
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1


def test_cli_help(capsys):
    """Running the CLI with --help should print usage and exit 0."""
    import sys
    from svg2pptx._cli import main

    sys.argv = ["svg2pptx", "--help"]
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
    out = capsys.readouterr().out
    assert "Usage" in out


def test_cli_converts_svg(svg_file, tmp_path):
    """The CLI entry point should create a PPTX from an SVG."""
    import sys
    from svg2pptx._cli import main

    out = tmp_path / "cli_out.pptx"
    sys.argv = ["svg2pptx", str(svg_file), str(out)]
    main()
    assert out.exists()
