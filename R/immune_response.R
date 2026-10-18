# Compare antibody responses before and after normalising to the approved
# dose. Save web and vector copies using the notes' light palette and font.
library(tidyverse)
library(ggrepel)

d <- tribble(
  ~vaccine,      ~dose, ~nab,  ~label,
  "AstraZeneca",  0.44, 0.444, "0.44x dose",
  "AstraZeneca",  1.00, 0.543, "1x dose",
  "J&J",          1.00, 0.471, "1x dose",
  "J&J",          2.00, 0.507, "2x dose",
  "Novavax",      1.00, 3.964, "1x dose",
  "Novavax",      5.00, 3.364, "5x dose",
  "Pfizer",       0.33, 1.023, "10 ug",
  "Pfizer",       0.67, 2.404, "20 ug",
  "Pfizer",       1.00, 2.368, "30 ug",
  "Moderna",      0.25, 2.132, "25 ug",
  "Moderna",      0.50, 3.746, "50 ug",
  "Moderna",      1.00, 4.111, "100 ug"
)

pal <- c(
  "Pfizer" = "#246A91",
  "Moderna" = "#6394AC",
  "AstraZeneca" = "#AA5A35",
  "J&J" = "#9A7A2E",
  "Novavax" = "#087B72"
)
background <- "#F4F2EA"
ink <- "#203137"
plot_font <- "Georgia"
plot_width <- 1048
plot_height <- 600
plot_dpi <- 96

d2 <- d |>
  group_by(vaccine) |>
  mutate(response = nab / nab[dose == 1]) |>
  ungroup()

# Small horizontal offsets so coincident points remain visible.
offsets <- c(
  "AstraZeneca" = -0.06,
  "J&J" = -0.03,
  "Novavax" = 0,
  "Pfizer" = 0.03,
  "Moderna" = 0.06
)
d2 <- d2 |>
  mutate(x_plot = dose * exp(offsets[vaccine]))

fit <- nls(
  response ~ top * dose^hill / (ec50^hill + dose^hill),
  data = d2,
  start = list(top = 1.05, ec50 = 0.3, hill = 3),
  algorithm = "port",
  lower = c(0.5, 0.01, 0.2),
  upper = c(2, 5, 10)
)

curve <- tibble(dose = exp(seq(log(0.2), log(6), length.out = 300)))
curve$response <- predict(fit, newdata = curve)

# Keep the measured and normalised responses on separate y scales.
plot_data <- bind_rows(
  d |> mutate(panel = "Relative to convalescent serum", response = nab,
              x_plot = dose),
  d2 |> mutate(panel = "Relative to approved dose")
) |>
  mutate(panel = factor(panel, levels = c(
    "Relative to convalescent serum", "Relative to approved dose"
  )))
curve <- curve |>
  mutate(panel = factor("Relative to approved dose",
                        levels = levels(plot_data$panel)))

plot <- ggplot(plot_data, aes(x_plot, response, colour = vaccine)) +
  geom_vline(xintercept = 1, linetype = 3, colour = "#83938B") +
  geom_hline(
    data = distinct(curve, panel) |> mutate(response = 1),
    aes(yintercept = response), linetype = 3, colour = "#83938B"
  ) +
  geom_line(
    data = filter(plot_data, panel == "Relative to convalescent serum"),
    aes(group = vaccine), linewidth = 0.7
  ) +
  geom_line(
    data = curve, aes(dose, response), inherit.aes = FALSE,
    linewidth = 1, colour = ink
  ) +
  geom_point(size = 3) +
  geom_text_repel(
    data = filter(plot_data, panel == "Relative to approved dose", dose != 1),
    aes(label = vaccine), size = 3, family = "DejaVu Sans", seed = 1,
    show.legend = FALSE
  ) +
  facet_wrap(~ panel, nrow = 1, scales = "free_y") +
  expand_limits(y = 0) +
  scale_x_log10(breaks = c(0.25, 0.5, 1, 2, 5)) +
  scale_colour_manual(values = pal) +
  labs(
    x = "Dose relative to approved dose",
    y = "Neutralising antibody response",
    colour = NULL
  ) +
  theme_minimal(base_size = 13, base_family = plot_font) +
  theme(
    plot.background = element_rect(fill = background, colour = NA),
    panel.background = element_rect(fill = background, colour = NA),
    panel.grid.major = element_line(colour = "#C8D0C9", linewidth = 0.3),
    panel.grid.minor = element_blank(),
    text = element_text(colour = ink),
    axis.text = element_text(colour = ink),
    strip.text = element_text(colour = ink, size = 13),
    panel.spacing = unit(1.5, "lines"),
    legend.position = "bottom",
    legend.background = element_rect(fill = background, colour = NA),
    legend.key = element_rect(fill = background, colour = NA),
    plot.margin = margin(14, 20, 12, 10)
  )

# Generate at the intended web dimensions; the SVG stays crisp on all screens.
ggsave("assets/immune_response.svg", plot,
       width = plot_width / plot_dpi, height = plot_height / plot_dpi,
       device = svglite::svglite, bg = background)
ggsave("assets/immune_response.png", plot,
       width = plot_width, height = plot_height, units = "px", dpi = plot_dpi,
       device = ragg::agg_png, bg = background)
ggsave("assets/immune_response.pdf", plot,
       width = plot_width / plot_dpi, height = plot_height / plot_dpi,
       device = grDevices::cairo_pdf, bg = background)
