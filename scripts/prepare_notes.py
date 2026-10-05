"""Merge the research agenda, preserve its old URLs, and add dated note notices.

Run after DOCX conversion, or directly from the project root.
"""

import json
import re
from pathlib import Path

from report_order import pages


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
    "overview/biology.qmd": "Why can a lower dose prove just as effective?",
    "overview/vaccine-development.qmd":
        "How do we determine the optimal dose during trials?",
    "overview/practical-implementation.qmd":
        "Syringes, vials and intradermal delivery",
    "overview/population-benefits.qmd":
        "What models say about the potential to save lives",
    "overview/decision-making.qmd":
        "Why changing doses is difficult, even during outbreaks",
}


def prepare_notes():
    agenda = Path("research-agenda/index.qmd")
    if Path("research-agenda/projects.qmd").exists():
        parts = []
        for slug in ["index", *AGENDA_SECTIONS]:
            content = Path(f"research-agenda/{slug}.qmd").read_text()
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
            Path(f"research-agenda/{slug}.qmd").unlink()

    for slug, anchor in AGENDA_SECTIONS.items():
        Path(f"research-agenda/{slug}.html").write_text(f'''<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="robots" content="noindex">
  <meta http-equiv="refresh" content="0; url=index.html#{anchor}">
  <title>Research agenda</title>
</head>
<body>
  <p>This section is now part of the <a href="index.html#{anchor}">research agenda</a>.</p>
  <script>location.replace('index.html' + (location.hash || '#{anchor}'));</script>
</body>
</html>
''')

    for page in [*Path("overview").glob("*.qmd"),
                 *Path("case-studies").glob("*.qmd"),
                 *Path("vaccines").glob("*.qmd"),
                 *Path("research-agenda").glob("*.qmd"),
                 *Path("about").glob("*.qmd")]:
        content = page.read_text()
        for old, new in NOTE_TITLES.items():
            content = content.replace(old, new)
        content = re.sub(r"Table(?: [12])?: ?", "", content)
        for title in ["immune memory and optimisation goals",
                      "factors that make a vaccine worth optimising"]:
            content = content.replace(title, title[0].upper() + title[1:])
        subtitle = NOTE_SUBTITLES.get(str(page))
        if subtitle and "{.note-subtitle}" not in content:
            content = re.sub(r"(?m)^(# .+)$",
                             r"\1\n\n*[" + subtitle + "]{.note-subtitle}*",
                             content, count=1)
        if page == Path("vaccines/index.qmd"):
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
                rf"research-agenda/{slug}\.qmd(?:#([^)]*))?",
                lambda m: f"research-agenda/index.qmd#{m[1] or anchor}",
                content)
        notice = "{{< include ../includes/note-disclaimer.qmd >}}"
        if notice not in content:
            content = re.sub(r"(?m)^(# .+)$", r"\1\n\n" + notice,
                             content, count=1)
        if (page == Path("about/index.qmd") and
                "product of independent research" not in content):
            content += ("\nThis document is a product of independent research and "
                        "does not represent the views of Open Philanthropy "
                        "(now Coefficient Giving) or the Center for Global "
                        "Development.\n")
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
