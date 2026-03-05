# R Profile for VS Code - Configure output display

# Disable pagination of output
options(pager = "cat")

# Set console width to prevent wrapping
options(width = 120)

# Set max print width for data frames
options(max.print = 10000)

# Configure digits display
options(digits = 7)

# Show all rows and columns in tibble/data frame
options(pillar.print_max = Inf)
options(pillar.print_min = Inf)

# Improve output display for tidyverse
if (interactive()) {
  cat("R", R.version$major, ".", R.version$minor, " running in VS Code\n", sep = "")
}
