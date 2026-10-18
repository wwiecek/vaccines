Run plot scripts from the project root. `immune_response.R` saves the two-panel
antibody-response figure in `assets/`: SVG for the website, PDF for the report,
and a PNG copy. The plot is generated at 1048 × 600 CSS pixels (96 dpi), with
no subsequent stretching or raster resizing. The input data are in the script.
The left panel retains responses relative to convalescent serum, while the
right divides each vaccine's response by its response at the approved dose.

For future plots, use Georgia (the notes' body font) for axis labels, tick
labels, panel headings and legends. Small annotations may use a sans serif
font. Georgia must be installed and visible to the graphics devices. Use the
notes' light background (`#F4F2EA`) and reuse colours for the same quantities
across panels.
