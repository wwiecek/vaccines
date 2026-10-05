"""Build the complete report PDF from the site's QMD text pages.

Run from the project root: python3 scripts/build_report_pdf.py
"""

import os
import re
import subprocess
from pathlib import Path

from report_order import pages

missing = [page for page in pages if not Path(page).is_file()]
if missing:
    raise FileNotFoundError(f"Missing report pages: {', '.join(missing)}")

headings = {}
for page in pages:
    content = Path(page).read_text(encoding="utf-8")
    match = re.search(r"^# .+ \{#([^}]+)\}", content, re.MULTILINE)
    if not match:
        raise ValueError(f"No chapter heading ID in {page}")
    headings[page] = match.group(1)

chapters = []
for number, page in enumerate(pages, 1):
    content = Path(page).read_text(encoding="utf-8")
    content = re.sub(r"\A---\n.*?\n---\n", "", content, count=1,
                     flags=re.DOTALL)

    content = content.replace(
        "{{< include ../includes/note-disclaimer.qmd >}}",
        Path("includes/note-disclaimer.qmd").read_text().strip())
    content = content.replace("::: {.note-disclaimer}", "").replace("\n:::", "")

    # Each web page has its own footnote sequence. Prefix labels before
    # concatenating pages so the PDF retains every distinct note.
    content = re.sub(r"\[\^([^\]\n]+)\]",
                     lambda match: f"[^chapter-{number}-{match.group(1)}]",
                     content)
    content = content.replace("../assets/", "assets/")
    # Use the untouched originals for print; the site loads compressed PNGs.
    for web, original in [("image1.png", "syringes.png"),
                          ("image3.png", "layers.png")]:
        if Path("assets", original).is_file():
            content = content.replace(f"assets/{web}", f"assets/{original}")

    def internal_link(match):
        target = os.path.normpath(Path(page).parent / match.group(1))
        if target not in headings:
            raise ValueError(f"Unknown report link in {page}: {match.group(1)}")
        return f"](#{match.group(2) or headings[target]})"

    content = re.sub(r"\]\(([^)#]+\.qmd)(?:#([^)]*))?\)",
                     internal_link, content)
    chapters.append(content.strip())

Path("downloads").mkdir(exist_ok=True)
subprocess.run([
    "pandoc", "-f", "markdown", "-t", "pdf",
    "--pdf-engine=xelatex", "--resource-path=.",
    "--toc", "--toc-depth=2", "--number-sections",
    "--lua-filter=scripts/pdf-format.lua",
    "--include-in-header=includes/pdf-style.tex",
    "--metadata=title:Optimal dosing of vaccines",
    "--metadata=author:Witold Więcek", "--metadata=date:Revised autumn 2026",
    "-V", "geometry:margin=25mm", "-V", "secnumdepth=3",
    "-V", "colorlinks=true", "-V", "linkcolor=ReportGreen",
    "-V", "urlcolor=ReportGreen", "-V", "fontsize=11pt",
    "-V", "mainfont=DejaVu Serif", "-V", "sansfont=DejaVu Sans",
    "-o", "downloads/fractional-dosing-of-vaccines.pdf",
], input="\\clearpage\n\n" + "\n\n".join(chapters) + "\n",
   text=True, check=True)
