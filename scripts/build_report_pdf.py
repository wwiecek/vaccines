"""Build the complete report PDF from the site's QMD text pages.

Run from the project root: python3 scripts/build_report_pdf.py
"""

import os
import re
import subprocess
from pathlib import Path


# This is the chapter order in the original report Markdown. Keep the four
# case studies at the end, after the research agenda.
pages = [
    "about/index.qmd",
    "overview/index.qmd",
    "case-studies/index.qmd",
    "overview/biology.qmd",
    "overview/vaccine-development.qmd",
    "overview/practical-implementation.qmd",
    "overview/population-benefits.qmd",
    "overview/decision-making.qmd",
    "vaccines/index.qmd",
    "research-agenda/index.qmd",
    "research-agenda/projects.qmd",
    "research-agenda/knowledge-gaps.qmd",
    "research-agenda/future-pathways.qmd",
    "research-agenda/reservations.qmd",
    "case-studies/covid.qmd",
    "case-studies/mpox.qmd",
    "case-studies/polio.qmd",
    "case-studies/yellow-fever.qmd",
]

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

    # Each web page has its own footnote sequence. Prefix labels before
    # concatenating pages so the PDF retains every distinct note.
    content = re.sub(r"\[\^([^\]\n]+)\]",
                     lambda match: f"[^chapter-{number}-{match.group(1)}]",
                     content)
    content = content.replace("../assets/", "assets/")

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
    "--toc", "--toc-depth=2", "--metadata=title:Fractional dosing of vaccines",
    "--metadata=author:Witold Więcek", "--metadata=date:June 2024",
    "-V", "geometry:margin=25mm", "-V", "fontsize=11pt",
    "-V", "mainfont=DejaVu Serif", "-V", "sansfont=DejaVu Sans",
    "-o", "downloads/fractional-dosing-of-vaccines.pdf",
], input="\n\n".join(chapters) + "\n", text=True, check=True)
