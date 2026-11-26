#### The {tidyverse}

# The {tidyverse} is a collection of R packages designed around tidy data
# principles, where data is stored in a data.frame() where each variable is a
# column and each observation is a row, and each value is stored in a separate
# "cell". It provides a consistent framework for data manipulation and
# visualization, and analysis, with all {tidyverse} packages working  seamlessly
# together, allowing for a streamlined workflow that emphasizes readability and
# reproducibility.

library(tidyverse)
# We will review the core packages of the {tidyverse} as well as some additional
# useful packages.

# Just a reminder of where we are: https://r4ds.hadley.nz/whole-game.html

# Import --------------------------------------------------------------

## Tabular data ---------------------------------------

# The most basic file format for data storage is CSV (comma-separated values)
# CSV files are plain text and easy to share between programs.

# R comes with base functions for importing data, such as:
?read.csv()
# Even more:
help.search("^read", fields = "name", package = c("base", "utils"))

# The {tidyverse} provides a more consistent (i.e., often safer) set of
# functions for importing data. The main package for this is {readr} that
# provides functions that parallel the base R functions:
?read_csv()
# These functions are designed to be automatically handle common data types by
# parsing the text stored in these files them correctly.

# Other formats of tabular data include:

# Other notable packages for importing data:
?readxl::read_excel() # for Excel files (xls, xlsx)
?googlesheets4::read_sheet() # for Google Sheets
?arrow::read_parquet() # for Parquet files
?haven::read_sav() # for SPSS files
?haven::read_sas() # for SAS files
# ...and more. See https://www.tidyverse.org/packages/#import

# Let's import a CSV file as an example. I'll be VERY explicit about the column
# types, but typically {readr} will do a good job of guessing the column types
# correctly. If you want to see what it guessed, you can use the `spec()`
# function to see the column types it guessed.

dta_deaf_numer_sinfo <- read_csv(
  "data/deaf_numer_sinfo.csv",
  col_types = cols(
    sID = col_factor(),
    Group = col_factor(levels = c("NH", "Deaf")),
    sex = col_factor(levels = c("m", "f")),
    age = col_integer()
  )
)
glimpse(dta_deaf_numer_sinfo) # "peak" at the structure
str(dta_deaf_numer_sinfo) # base R way (more general)

dta_deaf_numer <- haven::read_sav("data/deaf_numer.sav")
glimpse(dta_deaf_numer)

# Partial data from https://doi.org/10.1111/cogs.12880

## Big data ------------------------------------------
# What is big data?
# Typically refers to datasets too large to fit in memory.
# Your RAM size in GB is given by the next line:
ps::ps_system_memory()$total / 1024^3 # in GB
# However, even smaller datasets can be too big for RAM since reading data into
# memory usually requires extra space for processing (about 2x or more).

# We will cover handling big data in a separate lesson.

## Unstructured / Non tabular data -----------------------

# Data can also be stored in unstructured formats.
# For example, JSON files:
jsonlite::read_json("data/info.json")
# This does not return a data frame, but a list - tidying this up can be a pain
# in the @$$, and is called "rectangling":
# https://tidyr.tidyverse.org/articles/rectangle.html

# Other popular formats include yaml, toml (human readable formats), and xml:
?yaml12::read_yaml()
?toml::read_toml()
?xml2::read_xml()


# The data.frame() -----------------------------------------------------

# A data frame is a table-like structure in R. Importer functions return a data
# frame, but we can also create one ourselves with data.frame() (or coerce
# objects to data frames with as.data.frame)
data.frame(x = 1:3, y = c("a", "b", "c"))
as.data.frame(list(x = 1:3, y = c("a", "b", "c")))
as.data.frame(matrix(c("1", "2", "3", "a", "b", "c"), ncol = 2)) # :(

# Under the hood a data frame is a list of equal-length vectors, with optional
# row names.
(df <- data.frame(
  x = 1:3,
  y = c("a", "b", "c"),

  row.names = c("David", "Saul", "Goliath")
))
str(df)
unclass(df)
is.list(df)
View(df) # view it in R's viewer.

head(df, n = 2) # get first few rows (useful when printing long dfs)
tail(df, n = 2) # get last few rows
ncol(df) # how many columns?
nrow(df) # how many rows?
dim(df) # dimensions of df
colnames(df) # get column names
rownames(df) # get row names
methods(class = "data.frame") # see methods for data frames

# Note that tidyverse packages (and maybe others) prefer using tibbles (a modern
# version of data frames) - they are a special class of data frame that never
# have row names, and they print nicely in the console.
as_tibble(df) # no row names, nicer printing
dta_deaf_numer_sinfo
as.data.frame(dta_deaf_numer_sinfo)

is_tibble(dta_deaf_numer_sinfo)
is.data.frame(dta_deaf_numer_sinfo)
class(dta_deaf_numer_sinfo)

tibble()
# Some people think tibbles are better than data frames, it *usually* doesn't
# matter. But - note that some packages don't play nicely with tibbles, so you
# might want to convert them to data frames using `as.data.frame()` if you
# encounter issues.

# We can index data frames by row and column in many different ways:
df[1:2, ]
df[, 1, drop = FALSE]
df[1:2, 1, drop = FALSE]
df[1:2, "x"]
df[c("David", "Saul"), "x"]
df$x[1:2]
# etc...

# Wrangling -----------------------------------------------------------------
# (working with tidy data frames)

# We will be using the pipe operator (|>) (similar to the older %>% pipe).
# This allows us to chain together operations, where:
#     x |> f(y, z) is equivalent to f(x, y, z).
# We can think of it as a "and them" operator.
# The pipe operator allows us to write code that is more readable and
# easier to understand. Compare these equivalent expressions:
substitute({
  mean(na.omit(x), trim = 0.1)
  x |> na.omit() |> mean(trim = 0.1)
  0.1 |> mean(na.omit(x), trim = _)

  0.1 |> mean(x = na.omit(x)) # less safe
})

# This is particularly useful with may {tidyverse} functions which take a data
# frame as the first input, and return a data frame. This mean we can *chain*
#  multiple manipulations with human-readable code while avoiding creating
# intermediate variables that are not needed for the final analysis, which can
# clutter the workspace.

## Transforming -----------------------------

# The deaf_numer.sav was imported, but the columns types are not quite right.

# For each of the following, what is the dim() of the resulting df?
dta_deaf_numer_tidy <- dta_deaf_numer |>
  mutate(
    sID = factor(sID),

    # For all columns nFingers:rt, convert them to integers:
    across(nFingers:rt, .fns = as.integer)
  ) |>
  # Drop the first block (practice), and keep only correct responses:
  filter(block > 1, acc == 1) |>
  # no need for the acc column anymore:
  select(-acc) |>
  # Also these two participants are not included in the analysis because they
  # were naughty and did not follow the instructions:
  filter(sID %notin% c("9", "32"))

glimpse(dta_deaf_numer_tidy)

## Joining ---------------------------------

# We now have two dfs:
glimpse(dta_deaf_numer_tidy) # single trial data
glimpse(dta_deaf_numer_sinfo) # subject info

# We can join them - joining is the process of combining columns from two data
# frames by a key: a variable that identifies rows in both tables as matching
?left_join # add columns from second (right) df to first (left) df
?right_join # add columns from first (left) df to second (right) df
?inner_join # keep only matching rows
?full_join # keep all rows from both dfs

dta_deaf_numer_full <- dta_deaf_numer_tidy |>
  left_join(dta_deaf_numer_sinfo, by = "sID")
# Why choose left join here?

glimpse(dta_deaf_numer_full)

# There are also filtering joins:
?semi_join # keep only matching rows from first df
?anti_join # keep only non-matching rows from first df
# We will about joining more later when discussing SQL

# Let's take a look at the data:
glimpse(dta_deaf_numer_full)

# This data is read for analysis!
lme4::lmer(
  rt ~ Group * factor(nFingers) + (1 | sID) + (1 | sID:nFingers),
  data = dta_deaf_numer_full
) |>
  parameters::model_parameters()

ggplot(dta_deaf_numer_full, aes(factor(nFingers), rt)) +
  facet_grid(cols = vars(Group)) +
  stat_summary(aes(group = sID), geom = "point", color = "grey") +
  stat_summary(aes(group = sID), geom = "line", color = "grey") +
  stat_summary(color = "red", geom = "point") +
  stat_summary(color = "red", geom = "line", group = 1, linewidth = 1) +
  geom_blank() +
  expand_limits(y = 0) +
  theme_bw() +
  labs(x = "Number of Fingers") +
  scale_y_continuous(
    "Reaction Time [ms]",
    labels = scales::label_number(big.mark = ",")
  )


## Reshaping data ---------------------------

emotionalWM <- readxl::read_excel("data/Zhang2018_emotionalWM.xlsx") |>
  mutate(
    rID = factor(rID),
    group = factor(group)
  )
# data from https://doi.org/10.3389%2Ffnbeh.2018.00065
glimpse(emotionalWM)
# Is this data tidy? (No, why?)

emotionalWM_long <- emotionalWM |>
  pivot_longer(
    cols = positive_average:negative_O2,
    names_sep = "_",
    names_to = c("emotion", "area"),
    values_to = "mV",
    # If you want to convert the name-columns to factors (or you can do it later
    # in a mutate()):
    names_transform = list(
      emotion = factor,
      area = factor
    )
  )

head(emotionalWM_long, n = 18)


# We can also go back to wide format with pivot_wider():
emotionalWM_wide <- emotionalWM_long |>
  pivot_wider(
    names_from = c("emotion", "area"),
    values_from = "mV",
    names_sep = "_"
  )

all.equal(emotionalWM, emotionalWM_wide)


## Summarizing -------------------------------
# and other "by" manipulations

# So far, we've looked at row-preserving operations - operations that the number
# of data points unchanged (even when filtering rows). But we can also aggregate
# data.

dta_deaf_numer_full |>
  summarise(
    mean_rt = mean(rt),
    n_trials = n()
  )

# That's not very informative - we really want the mRT by subject, group, and
# condition:
(dta_summ_by_id <- dta_deaf_numer_full |>
  summarise(
    mean_rt = mean(rt),
    n_trials = n(),

    .by = c(sID, Group, nFingers)
  ))


# We can also use the older group_by() for this:
dta_deaf_numer_full |>
  group_by(sID, Group, nFingers) |>
  summarise(
    mean_rt = mean(rt),
    n_trials = n()
  ) |>
  ungroup() # good practice to ungroup after completing a grouped operation!!

# We can further summarize the data by calculating the average response time
# for each group and condition:
dta_summ_by_id |>
  summarise(
    across(mean_rt, .fns = list(mean = mean, sd = sd)),
    across(n_trials, .fns = list(min = min, max = max)),
    n_subjects = n(), # number of subjects in each group and condition

    .by = c(Group, nFingers)
  )


# Most {dplyr} verbs work with grouped data:
dta_summ_by_id |>
  mutate(
    grand_mean_rt2 = mean(mean_rt),
    .by = sID
  )
# https://dplyr.tidyverse.org/reference/dplyr_by.html

## save--------------

# save to a `.csv` file
write.csv(dta_deaf_numer_full, "data_clean.csv")
write_excel_csv(dta_deaf_numer_full, "data_clean.csv")

# save to an R data file
saveRDS(dta_deaf_numer_full, "data_clean.rds")
# readRDS() into object This format is R-specific, but it preserves more
# information about the data (e.g., factor levels, date formats, etc).

# Other formats:
?openxlsx::write.xlsx() # for Excel files (xlsx)
?googlesheets4::write_sheet() # for Google Sheets
?arrow::write_parquet() # for Parquet files
?haven::write_sav() # for SPSS files
?haven::write_sas() # for SAS files


jsonlite::write_json(
  dta_deaf_numer_full,
  "data_clean.json",
  dataframe = "columns"
) # for JSON files
?yaml12::write_yaml() # for yaml files
?toml::write_toml() # for toml files
?xml2::write_xml() # for XML files
