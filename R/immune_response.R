# Plot antibody responses relative to each vaccine's approved dose, with a
# pooled Hill curve. Save web and vector copies using the notes' light palette.
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

plot <- ggplot() +
  geom_hline(yintercept = 1, linetype = 3, colour = "#83938B") +
  geom_vline(xintercept = 1, linetype = 3, colour = "#83938B") +
  geom_line(data = curve, aes(dose, response), linewidth = 1, colour = ink) +
  geom_point(data = d2, aes(x_plot, response, colour = vaccine), size = 3) +
  geom_text_repel(
    data = d2, aes(x_plot, response, label = vaccine, colour = vaccine),
    size = 3, family = "DejaVu Sans", seed = 1, show.legend = FALSE
  ) +
  scale_x_log10(breaks = c(0.25, 0.5, 1, 2, 5)) +
  scale_colour_manual(values = pal) +
  labs(
    x = "Dose relative to approved dose",
    y = "Immune response relative to approved dose",
    colour = NULL
  ) +
  theme_minimal(base_size = 12, base_family = "DejaVu Sans") +
  theme(
    plot.background = element_rect(fill = background, colour = NA),
    panel.background = element_rect(fill = background, colour = NA),
    panel.grid.major = element_line(colour = "#C8D0C9", linewidth = 0.3),
    panel.grid.minor = element_blank(),
    text = element_text(colour = ink),
    axis.text = element_text(colour = ink),
    legend.position = "bottom",
    legend.background = element_rect(fill = background, colour = NA),
    legend.key = element_rect(fill = background, colour = NA),
    plot.margin = margin(14, 20, 12, 10)
  )

ggsave("assets/immune_response.png", plot, width = 8, height = 5,
       dpi = 180, device = ragg::agg_png, bg = background)
ggsave("assets/immune_response.pdf", plot, width = 8, height = 5,
       device = grDevices::cairo_pdf, bg = background)
