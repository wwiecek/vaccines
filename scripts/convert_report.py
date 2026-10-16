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

from prepare_notes import prepare_notes

SOURCE = Path("Shallow investigation into vaccine optimisation (draft).docx")

# The boundaries are Pandoc's heading IDs in the DOCX, not line numbers. Each
# source note is rendered separately so its tables and footnotes remain local.
PAGES = [
    ("notes/02-summary.qmd", "executive-summary", "introducing-four-case-studies"),
    ("notes/09-case-studies.qmd", "introducing-four-case-studies", "biology-of-optimal-dosing"),
    ("notes/03-biology.qmd", "biology-of-optimal-dosing", "vaccine-development-perspective"),
    ("notes/04-vaccine-development.qmd", "vaccine-development-perspective", "practical-aspects-of-changing-dose-syringes-vials-and-intradermal-delivery"),
    ("notes/05-practical-implementation.qmd", "practical-aspects-of-changing-dose-syringes-vials-and-intradermal-delivery", "how-large-are-health-benefits-from-optimisation"),
    ("notes/06-population-benefits.qmd", "how-large-are-health-benefits-from-optimisation", "examples-of-how-optimisation-decisions-are-made"),
    ("notes/07-decision-making.qmd", "examples-of-how-optimisation-decisions-are-made", "finding-targets-for-optimisation-disease-specific-summaries"),
    ("notes/08-vaccines.qmd", "finding-targets-for-optimisation-disease-specific-summaries", "conclusions-and-next-steps"),
    ("notes/14-research-agenda.qmd", "conclusions-and-next-steps", "four-potential-projects-that-could-be-done-right-now"),
    ("notes/research-agenda-projects.qmd", "four-potential-projects-that-could-be-done-right-now", "what-i-still-dont-understand"),
    ("notes/research-agenda-knowledge-gaps.qmd", "what-i-still-dont-understand", "what-to-do-next"),
    ("notes/research-agenda-future-pathways.qmd", "what-to-do-next", "five-reasons-to-be-negative-about-these-proposals"),
    ("notes/research-agenda-reservations.qmd", "five-reasons-to-be-negative-about-these-proposals", "case-study-fractional-dosing-of-covid-vaccines"),
    ("notes/10-covid.qmd", "case-study-fractional-dosing-of-covid-vaccines", "case-study-mpox-vaccine"),
    ("notes/11-mpox.qmd", "case-study-mpox-vaccine", "case-study-inactivated-polio-vaccine"),
    ("notes/12-polio.qmd", "case-study-inactivated-polio-vaccine", "case-study-yellow-fever"),
    ("notes/13-yellow-fever.qmd", "case-study-yellow-fever", None),
]

RELATED = {
    "notes/02-summary.qmd": ["notes/09-case-studies.qmd", "notes/14-research-agenda.qmd"],
    "notes/09-case-studies.qmd": ["notes/10-covid.qmd", "notes/11-mpox.qmd", "notes/12-polio.qmd", "notes/13-yellow-fever.qmd"],
    "notes/03-biology.qmd": ["notes/04-vaccine-development.qmd", "notes/08-vaccines.qmd"],
    "notes/04-vaccine-development.qmd": ["notes/03-biology.qmd", "notes/research-agenda-projects.qmd"],
    "notes/05-practical-implementation.qmd": ["notes/11-mpox.qmd", "notes/13-yellow-fever.qmd"],
    "notes/06-population-benefits.qmd": ["notes/07-decision-making.qmd", "notes/10-covid.qmd"],
    "notes/07-decision-making.qmd": ["notes/06-population-benefits.qmd", "notes/10-covid.qmd"],
    "notes/08-vaccines.qmd": ["notes/09-case-studies.qmd", "notes/research-agenda-projects.qmd"],
    "notes/14-research-agenda.qmd": ["notes/research-agenda-projects.qmd", "notes/research-agenda-knowledge-gaps.qmd", "notes/research-agenda-future-pathways.qmd", "notes/research-agenda-reservations.qmd"],
    "notes/10-covid.qmd": ["notes/07-decision-making.qmd", "notes/06-population-benefits.qmd"],
    "notes/11-mpox.qmd": ["notes/05-practical-implementation.qmd", "notes/08-vaccines.qmd"],
    "notes/12-polio.qmd": ["notes/08-vaccines.qmd", "notes/05-practical-implementation.qmd"],
    "notes/13-yellow-fever.qmd": ["notes/06-population-benefits.qmd", "notes/08-vaccines.qmd"],
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
            filename = Path(name).name
            replacement = {"image1.png": "syringes.png",
                           "image3.png": "layers.png"}.get(filename)
            if (replacement and Path("assets", replacement).is_file() and
                    Path("assets", filename).is_file()):
                continue
            Path("assets", filename).write_bytes(archive.read(name))

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
        "pandoc", "-f", "json", "-t", "markdown-auto_identifiers",
        "--wrap=auto", "--columns=80", "--reference-location=block"
    ], input=json.dumps({**doc, "blocks": page_blocks}).encode()).decode()
    rendered = re.sub(r"\[([^\[\]]+)\]\{\.underline\}", r"\1", rendered)
    # Google Docs supplied these placeholder targets without real URLs.
    rendered = re.sub(r"\[([^\[\]]+)\]\(about:blank\)", r"\1", rendered)
    if path == "notes/07-decision-making.qmd":
        rendered = re.sub(r"(?m)^References$", "## References {#references-7}", rendered)
    if path in RELATED:
        links = [f"- [{titles[p]}]({os.path.relpath(p, Path(path).parent)})"
                 for p in RELATED[path]]
        references = re.search(r"(?m)^(#{2,3}) References(?: .*)?$", rendered)
        level = references[1] if references else "##"
        reading = f"{level} Further reading\n\n" + "\n".join(links) + "\n\n"
        if references:
            rendered = (rendered[:references.start()] + reading +
                        rendered[references.start():])
        else:
            rendered += "\n" + reading
    page_title = titles.get(path, "About")
    rendered = f"---\npagetitle: {json.dumps(page_title, ensure_ascii=False)}\n---\n\n" + rendered
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered, encoding="utf-8")


for path, start, end in PAGES:
    render_page(path, blocks[positions[start]:positions[end] if end else None])

# The report's introductory author and method notes precede its old TOC.
render_page("notes/01-about.qmd", [{"t": "Header", "c": [1, ["about", [], []],
    [{"t": "Str", "c": "About"}]]}] + blocks[:positions["table-of-contents"]])

# Keep the published note structure and notices after regeneration.
prepare_notes()
