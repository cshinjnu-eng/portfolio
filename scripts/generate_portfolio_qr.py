#!/usr/bin/env python3
"""Generate the portfolio website QR code used by the editorial PDF."""

from pathlib import Path

from reportlab.graphics import renderSVG
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "brand" / "portfolio-qr.svg"
URL = "https://csh.bsbsanwu.xyz"


def main() -> None:
    code = qr.QrCodeWidget(URL)
    x1, y1, x2, y2 = code.getBounds()
    size = 420
    drawing = Drawing(
        size, size, transform=[size / (x2 - x1), 0, 0, size / (y2 - y1), 0, 0]
    )
    drawing.add(code)
    renderSVG.drawToFile(drawing, str(OUTPUT))
    print(f"Built {OUTPUT}")


if __name__ == "__main__":
    main()
