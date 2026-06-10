"""Command-line interface for svg2pptx."""

import sys

from ._converter import svg_to_pptx


def main():
    """Entry point for the ``svg2pptx`` / ``svg2pptx2`` commands."""
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print("Usage: svg2pptx <input.svg> [output.pptx]")
        print("       svg2pptx2 <input.svg> [output.pptx]")
        sys.exit(0 if args and args[0] in ("-h", "--help") else 1)

    svg_path = args[0]
    pptx_path = args[1] if len(args) > 1 else None

    try:
        result = svg_to_pptx(svg_path, pptx_path)
        print(f"Created: {result}")
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
