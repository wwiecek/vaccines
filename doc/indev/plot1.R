# Compare observed antibody levels with responses normalised to each vaccine's
# approved dose. Render publication and web copies in doc/indev.
library(tidyverse)

d <- tribble(
  ~vaccine,      ~dose, ~nab,
  "AstraZeneca",  0.44, 0.444,
  "AstraZeneca",  1.00, 0.543,
  "J&J",          1.00, 0.471,
  "J&J",          2.00, 0.507,
  "Novavax",      1.00, 3.964,
  "Novavax",      5.00, 3.364,
  "Pfizer",       0.33, 1.023,
  "Pfizer",       0.67, 2.404,
  "Pfizer",       1.00, 2.368,
  "Moderna",      0.25, 2.132,
  "Moderna",      0.50, 3.746,
  "Moderna",      1.00, 4.111
)

panel_names <- c("Original values", "Relative to approved dose")
pal <- c(
  "Pfizer" = "#79CBE4",
  "Moderna" = "#F3B66C",
  "AstraZeneca" = "#E88DA2",
  "J&J" = "#BDD87F",
  "Novavax" = "#BCA8E8"
)

d2 <- d |>
  group_by(vaccine) |>
  mutate(response = nab / nab[dose == 1]) |>
  ungroup()

fit <- nls(
  response ~ top * dose^hill / (ec50^hill + dose^hill),
  data = d2,
  start = list(top = 1.05, ec50 = 0.3, hill = 3),
  algorithm = "port",
  lower = c(0.5, 0.01, 0.2),
  upper = c(2, 5, 10)
)

curve <- tibble(
  dose = seq(0, 5.4, length.out = 400),
  panel = panel_names[2]
)
curve$response <- predict(fit, newdata = curve)

plot_data <- bind_rows(
  transmute(d2, vaccine, dose, response = nab, panel = panel_names[1]),
  transmute(d2, vaccine, dose, response, panel = panel_names[2])
) |>
  mutate(panel = factor(panel, levels = panel_names))

point_data <- plot_data |>
  mutate(
    plot_dose = if_else(
      panel == panel_names[2] & dose == 1,
      dose + (match(vaccine, names(pal)) - 3) * 0.04,
      dose
    )
  )

plot <- ggplot(plot_data, aes(dose, response)) +
  geom_vline(xintercept = 1, colour = "#627A7D", linewidth = 0.45) +
  geom_hline(
    data = tibble(panel = factor(panel_names[2], levels = panel_names)),
    aes(yintercept = 1), colour = "#627A7D", linewidth = 0.45
  ) +
  geom_line(
    data = filter(plot_data, panel == panel_names[1]),
    aes(colour = vaccine, group = vaccine), linewidth = 1.05
  ) +
  geom_line(
    data = curve, aes(dose, response), inherit.aes = FALSE,
    colour = "#F4F2EA", linewidth = 1.15, linetype = "22"
  ) +
  geom_point(
    data = point_data, aes(x = plot_dose, colour = vaccine),
    size = 3.1, stroke = 0.6
  ) +
  geom_curve(
    data = tibble(panel = factor(panel_names[2], levels = panel_names)),
    aes(x = 1.5, y = 0.88, xend = 1.04, yend = 0.965),
    inherit.aes = FALSE,
    curvature = 0.2, colour = "#A5D8CB", linewidth = 0.55,
    arrow = grid::arrow(length = grid::unit(0.08, "in"))
  ) +
  geom_text(
    data = tibble(panel = factor(panel_names[2], levels = panel_names)),
    aes(x = 1.55, y = 0.83,
        label = "Normalised to each vaccine's\napproved-dose response"),
    inherit.aes = FALSE,
    hjust = 0, vjust = 1, colour = "#A5D8CB", size = 3.1,
    family = "DejaVu Sans", lineheight = 1.12
  ) +
  facet_wrap(~panel, scales = "free_y", nrow = 1) +
  scale_x_continuous(
    trans = scales::pseudo_log_trans(sigma = 0.2),
    breaks = c(0, 0.25, 0.5, 1, 2, 5),
    labels = c("0", "¼", "½", "1", "2", "5"),
    limits = c(0, 5.4), expand = expansion(mult = 0)
  ) +
  scale_y_continuous(
    limits = c(0, NA), breaks = scales::breaks_pretty(5),
    expand = expansion(mult = c(0, 0.04))
  ) +
  scale_colour_manual(values = pal) +
  labs(
    title = "Dose and neutralising antibody response",
    subtitle = "Observed responses across five COVID-19 vaccines",
    x = "Dose relative to approved dose",
    y = "Neutralising antibody response",
    colour = "Vaccine",
    caption = paste(
      "Approved-dose points are offset sideways to show all five.",
      "Left lines connect observed doses; dashed line is the pooled Hill fit.",
      "Dose axis uses a pseudo-log scale."
    )
  ) +
  guides(colour = guide_legend(override.aes = list(linewidth = 1.5, size = 2.7))) +
  theme_minimal(base_family = "DejaVu Sans", base_size = 11) +
  theme(
    plot.background = element_rect(fill = "#10232D", colour = NA),
    panel.background = element_rect(fill = "#19343D", colour = NA),
    panel.grid.major = element_line(colour = "#31515A", linewidth = 0.3),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_blank(),
    panel.spacing = grid::unit(0.7, "cm"),
    plot.title = element_text(
      family = "DejaVu Serif", size = 21, colour = "#F4F2EA",
      margin = margin(b = 5)
    ),
    plot.subtitle = element_text(colour = "#A5D8CB", size = 11,
                                 margin = margin(b = 17)),
    strip.text = element_text(colour = "#F4F2EA", face = "bold", size = 12,
                              margin = margin(b = 7)),
    axis.title = element_text(colour = "#DCE8E5", size = 10.5),
    axis.text = element_text(colour = "#C1D1CF", size = 9.5),
    axis.ticks = element_line(colour = "#78918F"),
    plot.caption = element_text(colour = "#AABFBC", hjust = 0, size = 8.5,
                                margin = margin(t = 16)),
    legend.position = "inside",
    legend.position.inside = c(0.985, 0.055),
    legend.justification = c(1, 0),
    legend.background = element_rect(fill = "#203943", colour = "#547078"),
    legend.margin = margin(7, 11, 7, 9),
    legend.title = element_text(colour = "#DCE8E5", face = "bold", size = 9),
    legend.text = element_text(colour = "#F4F2EA", size = 9),
    legend.key = element_rect(fill = "#203943", colour = NA),
    plot.margin = margin(22, 24, 20, 22)
  )

ggsave("doc/indev/plot1.pdf", plot, width = 13, height = 6.8,
       device = grDevices::cairo_pdf, bg = "#10232D")
ggsave("doc/indev/plot1.png", plot, width = 13, height = 6.8,
       dpi = 240, device = ragg::agg_png, bg = "#10232D")
