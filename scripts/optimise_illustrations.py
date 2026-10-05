"""Create web PNGs under 200 kB from the preserved illustration originals.

Run from the project root; requires Pillow. Originals are never overwritten.
"""

from io import BytesIO
from pathlib import Path

from PIL import Image


for source, target in [("syringes.png", "image1.png"),
                       ("layers.png", "image3.png")]:
    original = Image.open(Path("assets") / source).convert("RGB")
    width = original.width
    while True:
        image = original.resize(
            (width, round(width * original.height / original.width)),
            Image.Resampling.LANCZOS)
        image = image.quantize(colors=256, method=Image.Quantize.FASTOCTREE,
                               dither=Image.Dither.NONE)
        output = BytesIO()
        image.save(output, format="PNG", optimize=True)
        if output.tell() <= 200_000:
            break
        width = int(width * .95)
    (Path("assets") / target).write_bytes(output.getvalue())
    print(f"{target}: {image.width} × {image.height}, {output.tell():,} bytes")
