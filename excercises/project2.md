# Project 2: Wrangling Tabular Data

A mini-project to practice working with tabular data in Python or R. 

## American Time Use Survey (ATUS)

The American Time Use Survey takes a wide sample of Americans and interviews them in great detail about what they did the day before. They have done this each year going back to 2003. They offer many different data files, but we will work with the  2003–2025 Activity summary file, which contains information about the total time each  respondent spent doing each activity on that day. 

## Instructions

1. Go to the [ATUS Data Files](https://www.bls.gov/tus/data/datafiles-0325.htm) page. Scroll down to "Multi-Year ATUS Data Files" and download the "ATUS 2003–2025 Activity summary file (zip)". Unzip the file into the `data/` folder of this project (or a new project if you prefer). 

2. It will also be useful to open "2003–2025 ATUS Coding Lexicon (PDF)"

3. Make a new script, `tidy_atus.R` or `tidy_atus.py`. This script should read in the data file (`atussum_0325.dat`) and write a tidy version of it (e.g. `atus_tidy.csv`, `atus_tidy.parquet`, or `atus_tidy.rds`) to the `data/` folder. The tidy version should be in long format, and include respondent id, year, sex, activity code, and time spent (in minutes). All other variables can be dropped. 

4. Make a new script, `analyze_atus.R` or `analyze_atus.py`. 

5. Make a tidy data frame that contains the average time spent sleeping in a day for each year and each sex.

6. Pivot your data back to wide format so that you can calculate the correlation between the time people spend sleeping in a day and the time they spend working in a day (the activity codes for sleeping and working are in the coding lexicon).

7. **Bonus**: Download the 2025 Activity Lexicon as an XLS file from https://www.bls.gov/tus/lexicons.htm, clean it up, and join it to your tidy data frame so that you have a column with the activity description.