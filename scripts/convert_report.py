"""Convert the source DOCX into the site's standalone Quarto notes.

Run from the repository root: python3 scripts/convert_report.py
"""

import copy
import json
import os
import re
import subprocess
import zipfile
from pathlib import Path


SOURCE = Path("Shallow investigation into vaccine optimisation (draft).docx")

# The boundaries are Pandoc's heading IDs in the DOCX, not line numbers. Each
# source note is rendered separately so its tables and footnotes remain local.
PAGES = [
    ("overview/index.qmd", "executive-summary", "introducing-four-case-studies"),
    ("case-studies/index.qmd", "introducing-four-case-studies", "biology-of-optimal-dosing"),
    ("overview/biology.qmd", "biology-of-optimal-dosing", "vaccine-development-perspective"),
    ("overview/vaccine-development.qmd", "vaccine-development-perspective", "practical-aspects-of-changing-dose-syringes-vials-and-intradermal-delivery"),
    ("overview/practical-implementation.qmd", "practical-aspects-of-changing-dose-syringes-vials-and-intradermal-delivery", "how-large-are-health-benefits-from-optimisation"),
    ("overview/population-benefits.qmd", "how-large-are-health-benefits-from-optimisation", "examples-of-how-optimisation-decisions-are-made"),
    ("overview/decision-making.qmd", "examples-of-how-optimisation-decisions-are-made", "finding-targets-for-optimisation-disease-specific-summaries"),
    ("vaccines/index.qmd", "finding-targets-for-optimisation-disease-specific-summaries", "conclusions-and-next-steps"),
    ("research-agenda/index.qmd", "conclusions-and-next-steps", "four-potential-projects-that-could-be-done-right-now"),
    ("research-agenda/projects.qmd", "four-potential-projects-that-could-be-done-right-now", "what-i-still-dont-understand"),
    ("research-agenda/knowledge-gaps.qmd", "what-i-still-dont-understand", "what-to-do-next"),
    ("research-agenda/future-pathways.qmd", "what-to-do-next", "five-reasons-to-be-negative-about-these-proposals"),
    ("research-agenda/reservations.qmd", "five-reasons-to-be-negative-about-these-proposals", "case-study-fractional-dosing-of-covid-vaccines"),
    ("case-studies/covid.qmd", "case-study-fractional-dosing-of-covid-vaccines", "case-study-mpox-vaccine"),
    ("case-studies/mpox.qmd", "case-study-mpox-vaccine", "case-study-inactivated-polio-vaccine"),
    ("case-studies/polio.qmd", "case-study-inactivated-polio-vaccine", "case-study-yellow-fever"),
    ("case-studies/yellow-fever.qmd", "case-study-yellow-fever", None),
]

RELATED = {
    "overview/index.qmd": ["case-studies/index.qmd", "research-agenda/index.qmd"],
    "case-studies/index.qmd": ["case-studies/covid.qmd", "case-studies/mpox.qmd", "case-studies/polio.qmd", "case-studies/yellow-fever.qmd"],
    "overview/biology.qmd": ["overview/vaccine-development.qmd", "vaccines/index.qmd"],
    "overview/vaccine-development.qmd": ["overview/biology.qmd", "research-agenda/projects.qmd"],
    "overview/practical-implementation.qmd": ["case-studies/mpox.qmd", "case-studies/yellow-fever.qmd"],
    "overview/population-benefits.qmd": ["overview/decision-making.qmd", "case-studies/covid.qmd"],
    "overview/decision-making.qmd": ["overview/population-benefits.qmd", "case-studies/covid.qmd"],
    "vaccines/index.qmd": ["case-studies/index.qmd", "research-agenda/projects.qmd"],
    "research-agenda/index.qmd": ["research-agenda/projects.qmd", "research-agenda/knowledge-gaps.qmd", "research-agenda/future-pathways.qmd", "research-agenda/reservations.qmd"],
    "case-studies/covid.qmd": ["overview/decision-making.qmd", "overview/population-benefits.qmd"],
    "case-studies/mpox.qmd": ["overview/practical-implementation.qmd", "vaccines/index.qmd"],
    "case-studies/polio.qmd": ["vaccines/index.qmd", "overview/practical-implementation.qmd"],
    "case-studies/yellow-fever.qmd": ["overview/population-benefits.qmd", "vaccines/index.qmd"],
}


def walk(node, callback):
    if isinstance(node, dict):
        callback(node)
        for value in node.values():
            walk(value, callback)
    elif isinstance(node, list):
        for value in node:
            walk(value, callback)


def is_heading(block):
    return block["t"] == "Header"


def heading_id(block):
    return block["c"][1][0]


doc = json.loads(subprocess.check_output([
    "pandoc", "-f", "docx", "-t", "json", str(SOURCE)
]))
blocks = doc["blocks"]
positions = {heading_id(b): i for i, b in enumerate(blocks) if is_heading(b)}

with zipfile.ZipFile(SOURCE) as archive:
    Path("assets").mkdir(exist_ok=True)
    for name in archive.namelist():
        if name.startswith("word/media/"):
            Path("assets", Path(name).name).write_bytes(archive.read(name))

titles = {}
for path, start, _ in PAGES:
    header = blocks[positions[start]]
    titles[path] = subprocess.check_output([
        "pandoc", "-f", "json", "-t", "plain"
    ], input=json.dumps({**doc, "blocks": [header]}).encode()).decode().strip()

heading_pages = {}
for path, start, end in PAGES:
    for block in blocks[positions[start]:positions[end] if end else None]:
        if is_heading(block):
            heading_pages[heading_id(block)] = path

# The DOCX contains three Google Docs fragment IDs that refer to real notes.
legacy_fragments = {
    "2wwbldi": "case-study-inactivated-polio-vaccine",
    "46r0co2": "practical-aspects-of-changing-dose-syringes-vials-and-intradermal-delivery",
    "1ljsd9k": "examples-of-how-optimisation-decisions-are-made",
}
heading_pages.update({
    old: heading_pages[new] for old, new in legacy_fragments.items()
})


def render_page(path, page_blocks):
    page_blocks = copy.deepcopy(page_blocks)
    page_blocks = [b for b in page_blocks if not (
        is_heading(b) and heading_id(b).startswith("section")
        and b["c"][2] in ([], [{"t": "LineBreak"}])
    )]
    # The DOCX has a few blank heading paragraphs. Keep every prose block.
    page_blocks = [b for b in page_blocks if not (
        is_heading(b) and not any(x.get("t") == "Str" for x in b["c"][2])
    )]
    first_level = page_blocks[0]["c"][0] if page_blocks and is_heading(page_blocks[0]) else 1
    later_levels = [b["c"][0] for b in page_blocks[1:] if is_heading(b)]
    heading_shift = min(later_levels) - 2 if later_levels and min(later_levels) > 2 else 0

    def edit(node):
        if node.get("t") == "Header":
            level = node["c"][0]
            node["c"][0] = 1 if level == first_level else max(2, level - heading_shift)
        elif node.get("t") == "Image":
            src = node["c"][2][0]
            if src.startswith("media/"):
                node["c"][2][0] = os.path.relpath(
                    Path("assets") / Path(src).name, Path(path).parent)
        elif node.get("t") == "Link":
            target = node["c"][2][0]
            if target == "https://www.fda.gov/media/160785/download%5D":
                node["c"][2][0] = "https://www.fda.gov/media/160785/download"
            if target.startswith("#"):
                ident = legacy_fragments.get(target[1:], target[1:])
                if ident in heading_pages:
                    dest = heading_pages[ident]
                    relative = os.path.relpath(dest, Path(path).parent)
                    node["c"][2][0] = ("#" + ident if dest == path else relative + "#" + ident)
            # Underlines around links came from Google Docs formatting.
            label = node["c"][1]
            if len(label) == 1 and label[0]["t"] == "Underline":
                node["c"][1] = label[0]["c"]

    walk(page_blocks, edit)
    rendered = subprocess.check_output([
        "pandoc", "-f", "json", "-t", "markdown-auto_identifiers", "--wrap=none"
    ], input=json.dumps({**doc, "blocks": page_blocks}).encode()).decode()
    rendered = re.sub(r"\[([^\[\]]+)\]\{\.underline\}", r"\1", rendered)
    # Google Docs supplied these placeholder targets without real URLs.
    rendered = re.sub(r"\[([^\[\]]+)\]\(about:blank\)", r"\1", rendered)
    if path == "overview/decision-making.qmd":
        rendered = re.sub(r"(?m)^References$", "## References {#references-7}", rendered)
    if path in RELATED:
        links = [f"- [{titles[p]}]({os.path.relpath(p, Path(path).parent)})"
                 for p in RELATED[path]]
        rendered += "\n## Further reading\n\n" + "\n".join(links) + "\n"
    page_title = titles.get(path, "About")
    rendered = f"---\npagetitle: {json.dumps(page_title, ensure_ascii=False)}\n---\n\n" + rendered
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered, encoding="utf-8")


for path, start, end in PAGES:
    render_page(path, blocks[positions[start]:positions[end] if end else None])

# The report's introductory author and method notes precede its old TOC.
render_page("about/index.qmd", [{"t": "Header", "c": [1, ["about", [], []],
    [{"t": "Str", "c": "About"}]]}] + blocks[:positions["table-of-contents"]])
