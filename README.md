# Vaccine optimisation report website

This is a Quarto website built from [`doc/Shallow investigation into vaccine optimisation (draft).docx`](doc/Shallow%20investigation%20into%20vaccine%20optimisation%20%28draft%29.docx). The DOCX is the source for the report text; the QMD pages are organised as standalone notes in `notes/`. Their two-digit filename prefixes follow the navigation bar, including the case-study menu order. Prose uses hard line breaks at about 80 columns; footnote definitions follow their citing paragraph (or complete list), and further-reading links precede references. `index.qmd` is the hand-edited landing page; `styles.css` contains presentation rules. `landing-preview.html` retains the separately reviewable version of the landing page. The top menus link to report chapters, while "On this page" links to headings within an article. `includes/footnote-placement.html` aligns margin footnotes with their references on wide screens; on narrow screens, the notes follow their paragraphs. Margin notes are shown in full up to ten lines unless they would crowd the next note or a wide table or figure. Tables and figures can extend into the right margin on desktop; notes are positioned around them.

`landing-visual-options.html` is a self-contained comparison of five optional landing-page accents. Buttons 1–5 switch the visual, the placement selector moves it between columns, and the motion button pauses the looping curves. The visuals are schematic design studies. The live landing page now uses a text-free, square version of option 5 on desktop; it is hidden on mobile and honours reduced-motion preferences. `includes/landing-accent.html` draws and animates that curve.

Run `quarto render` from the repository root to build `_site/`. Run `python3 scripts/convert_report.py` to repeat the Pandoc conversion from the DOCX. The converter runs `scripts/prepare_notes.py` to merge the research agenda and add the shared dated notice in `includes/note-disclaimer.qmd`. Former note URLs are retained through Quarto aliases. The four former agenda URLs redirect to sections of `notes/14-research-agenda.qmd`. The converter rewrites generated report QMD pages, so edit it or the source DOCX before rerunning it if content changes need to persist. It does not rewrite the landing page.

After any factual edit to the notes, run `python3 scripts/build_report_pdf.py` and commit the updated `downloads/fractional-dosing-of-vaccines.pdf` alongside the QMD changes. The script assembles all report pages in the order of the original report, including the introductory note and appendix case studies. It needs Pandoc, XeLaTeX, and the DejaVu fonts. The landing page links to the PDF. The PDF has numbered sections, a new page for each major section, distinct reference styling, and linked numbered cross-references. Website-only further-reading lists are omitted. `scripts/pdf-format.lua` and `includes/pdf-style.tex` control these PDF-specific choices.

`scripts/report_order.py` defines the shared reading order. Run `python3 scripts/prepare_notes.py` after changing that order or a page title to regenerate `includes/next-section.html`; the website uses it for the next-section links. These links do not appear in the PDF. `includes/note-attribution.html` adds the shared author and funding notice below each web note.

The GitHub Actions workflow rebuilds the PDF from the QMD pages before rendering and deploying `_site/` on every push to `main`. This keeps the published download current even if a local PDF rebuild was missed. In the repository's GitHub Pages settings, choose **GitHub Actions** as the publishing source. The workflow can also be started manually.

The original Markdown export in `doc/` is excluded from the render list. It is retained as a comparison copy and is not part of the site.

The upgraded implementation illustrations are preserved at full resolution in
`assets/syringes.png` and `assets/layers.png`. The website uses `assets/image1.png`
and `assets/image3.png`, each below 200 kB. Run
`python3 scripts/optimise_illustrations.py` (requires Pillow) after replacing an
original to regenerate these web versions. DOCX conversion preserves these
replacements; the PDF uses the full-resolution originals.

## Licence

© 2026 Witold Więcek. Unless otherwise indicated, original material in this
repository is licensed under [Creative Commons Attribution 4.0 International
(CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). The full licence is
in [LICENSE](LICENSE). Third-party material retains its original terms.

The site favicon is `assets/favicon.ico` (16, 32 and 48 px), derived from
`assets/favicon_large.png`. `assets/favicon.png` is the 32 px PNG version.

Individual notes offer a saved light/dark preference through the navbar's
"Toggle theme" button; the homepage keeps its fixed palette. Native
`color-scheme` metadata follows the active theme so Dark Reader can recognise
it. Dark Reader checks this when a page loads; if it is already active when
you change themes, reload once to let it detect the native theme.
The first biology illustration uses its full-resolution transparent PNG to
preserve smooth shading. The Yang illustration uses a compressed transparent
PNG; its full-resolution source is retained alongside it in `assets/`.
