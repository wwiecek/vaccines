"""Shared reading order for the PDF and website next-section links."""

# This is the chapter order in the original report Markdown. Keep the four
# case studies at the end, after the research agenda.
pages = [
    "notes/01-about.qmd",
    "notes/02-summary.qmd",
    "notes/09-case-studies.qmd",
    "notes/03-biology.qmd",
    "notes/04-vaccine-development.qmd",
    "notes/05-practical-implementation.qmd",
    "notes/06-population-benefits.qmd",
    "notes/07-decision-making.qmd",
    "notes/08-vaccines.qmd",
    "notes/14-research-agenda.qmd",
    "notes/10-covid.qmd",
    "notes/11-mpox.qmd",
    "notes/12-polio.qmd",
    "notes/13-yellow-fever.qmd",
]


# Former published URLs, retained as redirects by Quarto.
legacy_urls = {
    "notes/01-about.qmd": "/about/index.html",
    "notes/02-summary.qmd": "/overview/index.html",
    "notes/03-biology.qmd": "/overview/biology.html",
    "notes/04-vaccine-development.qmd": "/overview/vaccine-development.html",
    "notes/05-practical-implementation.qmd": "/overview/practical-implementation.html",
    "notes/06-population-benefits.qmd": "/overview/population-benefits.html",
    "notes/07-decision-making.qmd": "/overview/decision-making.html",
    "notes/08-vaccines.qmd": "/vaccines/index.html",
    "notes/09-case-studies.qmd": "/case-studies/index.html",
    "notes/10-covid.qmd": "/case-studies/covid.html",
    "notes/11-mpox.qmd": "/case-studies/mpox.html",
    "notes/12-polio.qmd": "/case-studies/polio.html",
    "notes/13-yellow-fever.qmd": "/case-studies/yellow-fever.html",
    "notes/14-research-agenda.qmd": "/research-agenda/index.html",
}
