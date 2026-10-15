# A library (a.k.a. package) is a collection of functions and/or data,
# (sometimes including code in lower-level languages like C, Fortran, or C++)
# To use a package:
#   1. install it (in the console, usually once per computer)
#   2. load it (in the code, once per session)

# install.packages("dplyr") # downloads from CRAN
library(dplyr) # loads it into this session 
# it is good practice to load all packages at the top of the script
# (in R, the name you install is always the name you load)



.libPaths() # where R keeps installed packages

# some packages come with R and are loaded automatically (base, stats, utils, ...)
# some packages come with R but are not loaded automatically (MASS, nlme, ...)

# packages not on CRAN can be installed straight from GitHub
# pak::pak("rimonim/embedplyr")

# Namespaces and masking -------------------------------------------------

# If two packages have a function with the same name, the most recently loaded one wins.
# Look at the message you got when you loaded dplyr:
#   The following objects are masked from 'package:stats': filter, lag
filter # which filter is this? The last line says <environment: namespace:dplyr>
search() # the order R looks for names: most recently loaded first

# to be explicit, use package::function (works even without loading the package)
stats::filter(1:10, rep(1/3, 3)) # moving average
dplyr::filter(mtcars, cyl == 6) # keep rows where cyl is 6

# Versions ---------------------------------------------------------------

packageVersion("dplyr") # dplyr version
R.version.string # R version
sessionInfo() # everything loaded, with versions

# Reading documentation --------------------------------------------------

?sd # same as help(sd)
??"standard deviation" # search all installed help pages
# standard function documentation format:
#   Usage, Arguments, Details, Value, See Also, Examples

vignette(package = "dplyr") # long-form tutorials that come with a package
vignette("rowwise")

# excercise: why does R's sd() give a different answer than numpy's std()?
sd(c(2, 4, 4, 4, 5, 5, 7, 9)) # 2.13809

# if needed, read the code itself
sd
