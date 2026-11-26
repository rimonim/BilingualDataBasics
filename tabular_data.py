#### Polars (and a bit of pandas)

# Python has no {tidyverse}, but it has a growing ecosystem for tabular data.
# Ideally this data is kept tidy, so that each variable is a column, each
# observation is a row, and each value is stored in a separate "cell".
#
# pandas is the classic package, designed to feel like R's data frames.
# Polars is a newer package - more like the {tidyverse},
# but is not compatible with all packages that expect pandas DataFrames.
#
# We will focus on Polars, with notes on pandas along the way (usually they have the same syntax)
# for more information, see https://docs.pola.rs/user-guide/getting-started/

import pandas as pd
import polars as pl

# Import --------------------------------------------------------------

## Tabular data ---------------------------------------

# The most basic file format for data storage is CSV (comma-separated values)
# CSV files are plain text and easy to share between programs.

# Polars has functions that parse the text into proper types:
help(pl.read_csv)
# All the Polars readers start with read_*:
[f for f in dir(pl) if f.startswith("read_")]
# (pandas has the same idea: pd.read_csv(), pd.read_excel(), ...)

# Other formats of tabular data include:
# pl.read_excel()     # for Excel files (xls, xlsx) (needs fastexcel)
# pl.read_parquet()   # for Parquet files
# pd.read_spss()      # for SPSS files (pandas only, needs pyreadstat)
# pd.read_sas()       # for SAS files (pandas only)
# (Google Sheets: the gspread library)
# ...and more. See https://docs.pola.rs/api/python/stable/reference/io.html

# Let's import a CSV file as an example. I'll be VERY explicit about the column
# types, but typically Polars will do a good job of guessing the column types
# correctly.

# Polars has two types of categorical variables: an "Enum" has fixed levels, and
# a "Categorical" discovers its levels from the data.
dta_deaf_numer_sinfo = pl.read_csv(
    "data/deaf_numer_sinfo.csv",
    schema_overrides={
        "sID": pl.Categorical,
        "Group": pl.Enum(["NH", "Deaf"]),
        "sex": pl.Enum(["m", "f"]),
        "age": pl.Int64,
    },
)
dta_deaf_numer_sinfo.glimpse() # "peek" at the structure
dta_deaf_numer_sinfo.schema # just the column types
# (pandas: pd.read_csv(..., dtype={"sID": "category", ...}), and .info())

# Polars has no SPSS reader; we can read with pandas and convert:
dta_deaf_numer = pl.from_pandas(pd.read_spss("data/deaf_numer.sav"))
dta_deaf_numer.glimpse()

# Partial data from https://doi.org/10.1111/cogs.12880

## Big data ------------------------------------------
# What is big data?
# Typically refers to datasets too large to fit in memory.
# Your RAM size in GB is given by the next line:
import psutil
psutil.virtual_memory().total / 1024**3 # in GB
# However, even smaller datasets can be too big for RAM since reading data into
# memory usually requires extra space for processing (about 2x or more).

# (Polars was designed with big data in mind - see pl.scan_csv())
# We will cover handling big data in a separate lesson.

## Unstructured / Non tabular data -----------------------

# Data can also be stored in unstructured formats.
# For example, JSON files:
import json
with open("data/info.json") as f:
    info = json.load(f)
info
# This does not return a data frame, but a dict - tidying this up can be a pain
# in the @$$, and is called "rectangling". Polars has a helper that flattens
# nested dicts into columns (so does pandas: pd.json_normalize()):
pl.json_normalize(info)

# Other popular formats include yaml, toml (human readable formats), and xml:
# yaml.safe_load()               # (needs PyYAML)
import tomllib
help(tomllib.load)               # toml (built into Python)
import xml.etree.ElementTree as ET
help(ET.parse)                   # xml (built into Python)


# The DataFrame -----------------------------------------------------

# A DataFrame is a table-like structure. Importer functions return a DataFrame,
# but we can also create one ourselves (from a dict of columns, a list of rows...)
pl.DataFrame({"x": [1, 2, 3], "y": ["a", "b", "c"]})
pl.DataFrame([{"x": 1, "y": "a"}, {"x": 2, "y": "b"}, {"x": 3, "y": "c"}])
pl.DataFrame([[1, "a"], [2, "b"], [3, "c"]], orient="row") # no names :(

# Under the hood a DataFrame is a collection of equal-length columns, each of
# which is a pl.Series
df = pl.DataFrame({"x": [1, 2, 3], "y": ["a", "b", "c"]})
df
type(df["x"])
df.to_dict(as_series=False) # as a plain dict of lists

df.head(n=2) # get first few rows (useful when printing long dfs)
df.tail(n=2) # get last few rows
df.width # how many columns?
df.height # how many rows?
df.shape # dimensions of df
df.columns # get column names
[m for m in dir(df) if not m.startswith("_")] # see methods for DataFrames

# A Polars DataFrame is like a tibble in R - it never has row names, and prints the column types
# A pandas DataFrame is more like a base R data frame - it always has row names (the "index")
df_pd = pd.DataFrame(
    {"x": [1, 2, 3], "y": ["a", "b", "c"]},
    index=["David", "Saul", "Goliath"],
)
df_pd
df_pd.loc["Saul"] # select rows by name
pl.from_pandas(df_pd) # the index is dropped when converting to Polars
df.to_pandas() # and back to pandas

isinstance(df, pl.DataFrame)
isinstance(df_pd, pd.DataFrame)

# Note that many packages (e.g. statsmodels) were built for pandas, so
# you might need `.to_pandas()` if you encounter issues.

# We can index DataFrames by row and column in many different ways.
# Remember - Python counts from 0, and slices exclude the end!
df[0:2]
df[:, 0]
df[0:2, 0]
df[0:2, "x"]
df["x"][0:2]
# etc...
# (pandas uses df.iloc[] for positions and df.loc[] for names)

# Wrangling -----------------------------------------------------------------
# (working with tidy data frames)

# Python usually doesn't use pipes, since methods already chain from left to right
# For methods that work like this, we can think of each "." as an "and then".
# Compare these equivalent expressions:
x = pl.DataFrame({"x": [1, 5, None, 10]})
pl.DataFrame.mean(pl.DataFrame.drop_nulls(x)) # nested functions
x.drop_nulls().mean() # chained methods
x.pipe(lambda d: d.drop_nulls()).mean() # .pipe() lets you chain *any* function

# In Polars, most methods take a data frame and return a data frame.
# This means we can chain multiple manipulations.
# Wrap the whole chain in () to spread it across lines.

## Transforming -----------------------------

# The deaf_numer.sav was imported, but the columns types are not quite right.

# Polars verbs work on "expressions" - pl.col("name") refers to a column,
# like a bare column name in {dplyr}.

# For each of the following, what is the .shape of the resulting df?
dta_deaf_numer_tidy = (
    dta_deaf_numer
    .with_columns( # like mutate()
        pl.col("sID").cast(pl.Int64).cast(pl.String).cast(pl.Categorical),

        # For all columns nFingers:rt, convert them to integers:
        pl.col("nFingers", "trial", "block", "acc", "rt").cast(pl.Int64),
    )
    # Drop the first block (practice), and keep only correct responses:
    .filter(pl.col("block") > 1, pl.col("acc") == 1)
    # no need for the acc column anymore:
    .drop("acc") # like select(-acc)
    # Also these two participants are not included in the analysis because they
    # were naughty and did not follow the instructions:
    .filter(~pl.col("sID").is_in(["9", "32"]))
)

dta_deaf_numer_tidy.glimpse()

# (pandas version, for comparison - pd.col() is new in pandas 3.0, in older
#  code you'll see lambdas instead: .loc[lambda d: d["block"] > 1])
dta_deaf_numer_tidy_pd = (
    pd.read_spss("data/deaf_numer.sav")
    .assign(sID=pd.col("sID").astype(int).astype(str).astype("category"))
    .loc[(pd.col("block") > 1) & (pd.col("acc") == 1)]
    .drop(columns="acc")
)

## Joining ---------------------------------

# We now have two dfs:
dta_deaf_numer_tidy.glimpse() # single trial data
dta_deaf_numer_sinfo.glimpse() # subject info

# We can join them - joining is the process of combining columns from two data
# frames by a key: a variable that identifies rows in both tables as matching
help(pl.DataFrame.join)
# how="left" # add columns from second (right) df to first (left) df
# how="right" # add columns from first (left) df to second (right) df
# how="inner" # keep only matching rows
# how="full" # keep all rows from both dfs

dta_deaf_numer_full = dta_deaf_numer_tidy.join(
    dta_deaf_numer_sinfo, on="sID", how="left"
)
# Why choose left join here?
# (pandas: df1.merge(df2, on="sID", how="left"))

dta_deaf_numer_full.glimpse()

# There are also filtering joins:
# how="semi" # keep only matching rows from first df
# how="anti" # keep only non-matching rows from first df
dta_deaf_numer_sinfo.join(dta_deaf_numer_tidy, on="sID", how="anti") # who's missing?
# We will about joining more later when discussing SQL

# This data is ready for analysis!
import statsmodels.formula.api as smf

smf.mixedlm(
    "rt ~ Group * C(nFingers)",
    data=dta_deaf_numer_full.to_pandas(), # statsmodels needs pandas
    groups="sID", # (1 | sID)
    vc_formula={"nFingers": "0 + C(nFingers)"}, # (1 | sID:nFingers)
).fit().summary()

# plotnine is a Python version of {ggplot2} - almost the same code as in R!
# (aesthetics are written as strings, and the "+" chain needs (parentheses))
from mizani.labels import label_number
from plotnine import (
    aes,
    expand_limits,
    facet_grid,
    geom_blank,
    ggplot,
    labs,
    scale_y_continuous,
    stat_summary,
    theme_bw,
)

(
    ggplot(dta_deaf_numer_full, aes("factor(nFingers)", "rt"))
    + facet_grid(cols="Group")
    + stat_summary(aes(group="sID"), fun_data="mean_se", geom="point", color="grey")
    + stat_summary(aes(group="sID"), fun_data="mean_se", geom="line", color="grey")
    + stat_summary(fun_data="mean_se", color="red", geom="point")
    + stat_summary(fun_data="mean_se", color="red", geom="line", group=1, size=1)
    + geom_blank()
    + expand_limits(y=0)
    + theme_bw()
    + labs(x="Number of Fingers")
    + scale_y_continuous(
        name="Reaction Time [ms]",
        labels=label_number(big_mark=","),
    )
)

## Reshaping data ---------------------------

emotionalWM = pl.read_excel(
    "data/Zhang2018_emotionalWM.xlsx",
    schema_overrides={"rID": pl.String},
).with_columns(pl.col("rID", "group").cast(pl.Categorical))
# data from https://doi.org/10.3389%2Ffnbeh.2018.00065
emotionalWM.glimpse()
# Is this data tidy? (No, why?)

# Polars calls pivot_longer() "unpivot" (pandas calls it "melt"):
emotionalWM_long = (
    emotionalWM
    .with_row_index("row") # remember the original row order
    .unpivot(
        index=["row", "rID", "group"], # all other columns are unpivoted
        variable_name="name",
        value_name="mV",
    )
    # split the column names into two columns (names_sep):
    .with_columns(
        emotion=pl.col("name").str.split("_").list.get(0).cast(pl.Categorical),
        area=pl.col("name").str.split("_").list.get(1).cast(pl.Categorical),
    )
    .drop("name")
    # unpivot() stacks column by column - sort to get R's row-by-row order.
    # (Polars sorts categories alphabetically - "1", "10", "11", ... - so we
    # sort by the original row number instead of rID)
    .sort("row", maintain_order=True)
    .drop("row")
)

emotionalWM_long.head(n=18)


# We can also go back to wide format with pivot() (same name in pandas):
emotionalWM_wide = (
    emotionalWM_long
    .with_columns(name=pl.concat_str("emotion", "area", separator="_"))
    .pivot(on="name", index=["rID", "group"], values="mV")
)

emotionalWM.equals(emotionalWM_wide)


## Summarizing -------------------------------
# and other "by" manipulations

# So far, we've looked at row-preserving operations - operations that keep the
# number of data points unchanged (even when filtering rows). But we can also
# aggregate data.

dta_deaf_numer_full.select( # like summarise()
    mean_rt=pl.col("rt").mean(),
    n_trials=pl.len(),
)

# That's not very informative - we really want the mRT by subject, group, and
# condition:
dta_summ_by_id = (
    dta_deaf_numer_full
    .group_by("sID", "Group", "nFingers", maintain_order=True)
    .agg(
        mean_rt=pl.col("rt").mean(),
        n_trials=pl.len(),
    )
)
dta_summ_by_id
# Unlike {dplyr}, there is no need to ungroup() - group_by().agg() always
# returns a regular DataFrame.

# (pandas: df.groupby([...], observed=True, as_index=False).agg(mean_rt=("rt", "mean"))
#  By default pandas puts the groups in the index - a bit like forgetting to
#  ungroup() - so you'll often see .reset_index() at the end.)

# We can further summarize the data by calculating the average response time
# for each group and condition:
(
    dta_summ_by_id
    .group_by("Group", "nFingers", maintain_order=True)
    .agg(
        pl.col("mean_rt").mean().name.suffix("_mean"),
        pl.col("mean_rt").std().name.suffix("_sd"),
        pl.col("n_trials").min().name.suffix("_min"),
        pl.col("n_trials").max().name.suffix("_max"),
        n_subjects=pl.len(), # number of subjects in each group and condition
    )
)
# Note: unlike numpy, the Polars and pandas .std() divide by n-1 (like R's sd())


# Grouped operations also work without collapsing rows (like mutate(.by = )):
dta_summ_by_id.with_columns(
    grand_mean_rt2=pl.col("mean_rt").mean().over("sID")
)
# https://docs.pola.rs/user-guide/expressions/window-functions/
# (pandas: df.groupby("sID")["mean_rt"].transform("mean"))

## save--------------

# save to a `.csv` file
dta_deaf_numer_full.write_csv("data_clean.csv")
dta_deaf_numer_full.write_csv("data_clean.csv", include_bom=True) # Excel-friendly
# (pandas: df.to_csv("data_clean.csv", index=False) - without index=False,
#  the row names are written as an extra column!)

# save to a Parquet file
dta_deaf_numer_full.write_parquet("data_clean.parquet")
# pl.read_parquet() to read it back. Unlike CSV, this format preserves more
# information about the data (e.g., categories, date formats, etc), and it can
# be read by R too (arrow::read_parquet()).
# (Python also has pickle - the closest thing to .rds - but pickles only work
#  in Python and can run arbitrary code when loaded, so prefer Parquet.)

# Other formats:
# .write_excel()                  # for Excel files (needs xlsxwriter)
# pyreadstat.write_sav()          # for SPSS files (needs a pandas df)
# (Google Sheets: the gspread library)

dta_deaf_numer_full.write_json("data_clean.json") # for JSON files
# yaml.safe_dump()                # for yaml files (needs PyYAML)
# tomli_w.dump()                  # for toml files (needs tomli-w)
# .to_xml()                       # for XML files (pandas only, needs lxml)
