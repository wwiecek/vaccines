# Vaccine optimisation report website

This is a Quarto website built from *Shallow investigation into vaccine optimisation (draft).docx*. The DOCX is the source for the report text; the QMD pages are organised as standalone notes. `index.qmd` is the hand-edited landing page; `styles.css` contains presentation rules. Report footnotes appear in the right margin beside their references.

Run `quarto render` from the repository root to build `_site/`. Run `python3 scripts/convert_report.py` to repeat the Pandoc conversion from the DOCX. The converter rewrites generated report QMD pages, so edit it or the source DOCX before rerunning it if content changes need to persist. It does not rewrite the landing page.

After a substantial edit to the report text, run `python3 scripts/build_report_pdf.py` and commit the updated `downloads/fractional-dosing-of-vaccines.pdf` alongside the QMD changes. The script assembles all report pages in the order of the original report, including the introductory note and appendix case studies. It needs Pandoc, XeLaTeX, and the DejaVu fonts. The landing page links to the PDF.

The GitHub Actions workflow rebuilds the PDF from the QMD pages before rendering and deploying `_site/` on every push to `main`. This keeps the published download current even if a local PDF rebuild was missed. In the repository's GitHub Pages settings, choose **GitHub Actions** as the publishing source. The workflow can also be started manually.

The original loose Markdown export is excluded from the render list. It remains in the working tree as a comparison copy and is not part of the site.
