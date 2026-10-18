# Maintenance

Run commands from the repository root. Edit the report in `notes/*.qmd`.

After factual changes, rebuild the complete PDF, inspect the affected pages,
and commit it with the notes:

```sh
python3 scripts/build_report_pdf.py
quarto render
```

The PDF build needs Pandoc, XeLaTeX and DejaVu fonts. It writes
`downloads/fractional-dosing-of-vaccines.pdf`; Quarto writes the site to `_site/`.
GitHub Actions runs both builds and deploys on pushes to `main`.

`report_order.py` defines the PDF order and next-section links. When changing
sections, also update the landing page and `landing-preview.html`.

`convert_report.py` imports the original DOCX and overwrites the QMD notes.
Use it only for a deliberate re-import, not a routine build: later edits to
notes would be lost. It also runs `prepare_notes.py`, which rewrites notices,
subtitles, redirects and next-section links. Review those changes before
keeping them, especially on notes with a custom disclaimer.

`optimise_illustrations.py` regenerates `assets/image1.png` and `image3.png`
from the preserved originals (`syringes.png` and `layers.png`). It needs Pillow.
Plot scripts and font conventions are documented in `R/README.md`.
