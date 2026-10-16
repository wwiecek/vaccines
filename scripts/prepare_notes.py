"""Merge the research agenda, preserve its old URLs, and add dated note notices.

Run after DOCX conversion, or directly from the project root.
"""

import json
import re
from pathlib import Path

from report_order import legacy_urls, pages


AGENDA_SECTIONS = {
    "projects": "four-potential-projects-that-could-be-done-right-now",
    "knowledge-gaps": "what-i-still-dont-understand",
    "future-pathways": "what-to-do-next",
    "reservations": "five-reasons-to-be-negative-about-these-proposals",
}


NOTE_TITLES = {
    "Practical aspects of changing dose: syringes, vials, and intradermal...":
        "Practical aspects of changing dose",
    "Practical aspects of changing dose: syringes, vials, and intradermal delivery":
        "Practical aspects of changing dose",
    "How large are health benefits from optimisation?":
        "Health benefits from optimisation",
    "Examples of how optimisation decisions are made":
        "How optimisation decisions are made",
}
NOTE_SUBTITLES = {
    "notes/03-biology.qmd": "Why can a lower dose prove just as effective?",
    "notes/04-vaccine-development.qmd":
        "How do we determine the optimal dose during trials?",
    "notes/05-practical-implementation.qmd":
        "Syringes, vials and intradermal delivery",
    "notes/06-population-benefits.qmd":
        "What models say about the potential to save lives",
    "notes/07-decision-making.qmd":
        "Why changing doses is difficult, even during outbreaks",
}


def prepare_notes():
    agenda = Path("notes/14-research-agenda.qmd")
    if Path("notes/research-agenda-projects.qmd").exists():
        parts = []
        for slug in ["index", *AGENDA_SECTIONS]:
            page = (agenda if slug == "index" else
                    Path(f"notes/research-agenda-{slug}.qmd"))
            content = page.read_text()
            content = re.sub(r"\A---\n.*?\n---\n", "", content,
                             count=1, flags=re.S)
            content = re.sub(r"\n## Further reading\n.*", "", content,
                             flags=re.S)
            content = re.sub(r"(?m)^(#{1,5}) ", r"\1# ", content)
            content = re.sub(r"\[\^([^\]\n]+)\]",
                             lambda m: f"[^agenda-{slug}-{m[1]}]", content)
            parts.append(content.strip())
        agenda.write_text('---\npagetitle: "Research agenda"\n---\n\n'
                          '# Research agenda {#research-agenda}\n\n' +
                          "\n\n".join(parts) + "\n")
        for slug in AGENDA_SECTIONS:
            Path(f"notes/research-agenda-{slug}.qmd").unlink()

    Path("research-agenda").mkdir(exist_ok=True)
    for slug, anchor in AGENDA_SECTIONS.items():
        Path(f"research-agenda/{slug}.html").write_text(f'''<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="robots" content="noindex">
  <meta http-equiv="refresh" content="0; url=../notes/14-research-agenda.html#{anchor}">
  <title>Research agenda</title>
</head>
<body>
  <p>This section is now part of the <a href="../notes/14-research-agenda.html#{anchor}">research agenda</a>.</p>
  <script>location.replace('../notes/14-research-agenda.html' + (location.hash || '#{anchor}'));</script>
</body>
</html>
''')

    for page in Path("notes").glob("*.qmd"):
        content = page.read_text()
        for old, new in NOTE_TITLES.items():
            content = content.replace(old, new)
        content = re.sub(r"Table(?: [12])?: ?", "", content)
        for title in ["immune memory and optimisation goals",
                      "factors that make a vaccine worth optimising"]:
            content = content.replace(title, title[0].upper() + title[1:])
        subtitle = NOTE_SUBTITLES.get(page.as_posix())
        if subtitle and "{.note-subtitle}" not in content:
            content = re.sub(r"(?m)^(# .+)$",
                             r"\1\n\n*[" + subtitle + "]{.note-subtitle}*",
                             content, count=1)
        if page == Path("notes/08-vaccines.qmd"):
            # Converted grid-table column boundaries are inconsistent. Use a
            # pipe table so every criterion remains in its intended column.
            match = re.search(r"(?m)^\+-.*?^\+=[^\n]*\+", content, re.S)
            if match:
                rows = ["| " + " | ".join(cell.strip() for cell in line.split("|")[1:-1]) + " |"
                        for line in match[0].splitlines()
                        if line.startswith("|") and line.replace("|", "").strip()]
                rows.insert(1, "| --- | --- | --- |")
                content = content[:match.start()] + "\n".join(rows) + content[match.end():]
        for slug, anchor in AGENDA_SECTIONS.items():
            content = re.sub(
                rf"research-agenda-{slug}\.qmd(?:#([^)]*))?",
                lambda m: f"14-research-agenda.qmd#{m[1] or anchor}",
                content)
        notice = "{{< include ../includes/note-disclaimer.qmd >}}"
        if notice not in content:
            content = re.sub(r"(?m)^(# .+)$", r"\1\n\n" + notice,
                             content, count=1)
        if (page == Path("notes/01-about.qmd") and
                "## Using and citing this report" not in content):
            content += """

## Using and citing this report

Most of this report was written in 2023–2024. It is not fully up to date and
is being revised.

The report is licensed under [Creative Commons Attribution 4.0 International
(CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/), unless otherwise
indicated. Third-party material retains its original terms.

Cite as Więcek, W. (2026). Optimal dosing of vaccines.
<https://witold.xyz/vaccines/>

This document is a product of independent research and does not represent the
views of Open Philanthropy (now Coefficient Giving) or the Center for Global
Development.
"""
        alias = legacy_urls[page.as_posix()]
        if "aliases:" not in content:
            content = content.replace("---\n", f"---\naliases: [{alias}]\n", 1)
        page.write_text(content)

    # Keep the website's linear reading route in the complete report's order.
    route = []
    for page in pages:
        title = re.search(r"(?m)^# (.+?) \{#", Path(page).read_text())[1]
        route.append({"path": page.replace(".qmd", ".html"), "title": title})
    template = Path("includes/next-section-template.html").read_text()
    Path("includes/next-section.html").write_text(
        template.replace("REPORT_ORDER", json.dumps(route, ensure_ascii=False)))


if __name__ == "__main__":
    prepare_notes()
