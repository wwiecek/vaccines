# Landing page maintenance

- When changing the report's division into sections, update the landing page's
  links, headings, and short descriptions to match. Keep the separately reviewable
  `landing-preview.html` in sync too.

# PDF maintenance

- Whenever factual content changes in the notes, re-render the complete PDF with
  `python3 scripts/build_report_pdf.py`, inspect the affected pages, and commit
  `downloads/fractional-dosing-of-vaccines.pdf` alongside the source changes.
