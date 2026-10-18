# Landing page maintenance

- When changing the report's division into sections, update the landing page's
  links, headings, and short descriptions to match. Keep the separately reviewable
  `landing-preview.html` in sync too.

# PDF maintenance

- Whenever factual content changes in the notes, re-render the complete PDF with
  `python3 scripts/build_report_pdf.py`, inspect the affected pages, and commit
  `downloads/fractional-dosing-of-vaccines.pdf` alongside the source changes.

# Image quality

- Compress images modestly, with no discernible loss of quality. Preserve
  transparency and smooth gradients; do not enforce a fixed file-size limit
  at the expense of readability or appearance. Keep the original sources.
