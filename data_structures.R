# In R (and Python too), everything is an object: numbers, text, lists, functions, and even packages
# objects have a class
class(10) # the class of the number 10 is "numeric"
class("hello") # the class of the string "hello" is "character"

# Object Assignment -----------------------------------------------------
# usually we give objects names so we can refer to them later
# in R, we use the assignment operator "<-". You can also use "=", but it is considered bad style.
x <- 10 # assign the number 10 to the object named "x"
x # print the value of x
x + 5 # add 5 to the value of x = 15
x # x is still 10, because we didn't change it
x <- x + 5 # assign the value of x + 5 to x
x # now x is 15

# Atomic Data Types ------------------------------------------------------

# Decimal numbers are called "numeric" in R, and "float" in Python
# they are "floating point" numbers, since the decimal point can "float" to any position in the number
default_numeric <- numeric()
age <- 23
(age * 365 + 1.001) / 365
2.3e-4 # scientific notation for 0.00023
NA_real_ # "not available" - missing value for decimal numbers
is.numeric(age) # check if age is a numeric

# Integers are called "integer" in R, and "int" in Python
default_integer <- integer()
23L
0L
NA_integer_ # missing value for integers

# True/False values are called "logical" in R, and "bool" in Python
default_logical <- logical()
TRUE
FALSE
NA_logical_

# Text values are called "character" in R, and "str" in Python
default_character <- character()
'Hello goodbye'
""
multiline_string <- "This is a string
that spans multiple lines"
NA_character_

  # String manipulation
  paste0(multiline_string, "\nhere is another line")
  paste0("I am ", age, " years old")
  library(stringr) # for advanced string manipulation in R (included in tidyverse)
  str_dup("hi ", 3) # repeat a string multiple times
  str_detect(multiline_string, "span") # check if a string is in another string
  str_sub(multiline_string, 1, 4) # a slice of the string, from index 1 to 4
  str_to_title(multiline_string) # convert to title case
  str_to_lower(multiline_string) # convert to lowercase
  str_replace_all(multiline_string, " ", "|") # replace all spaces with "|"
  str_split_1(multiline_string, "\n") # split a string into a vector of strings, using the newline character as the delimiter
  str_count(multiline_string, " ") # count the number of spaces in the string
  # for more, see the stringr cheatsheet: https://rstudio.github.io/cheatsheets/html/strings.html


# Complex numbers are called "complex" in R and Python
default_complex <- complex()
1 + 2i
NA_complex_

# Raw bytes are called "raw" in R, and "bytes" in Python
default_raw <- raw()
  # you wouldn't normally create raw bytes directly, 
  # but you can convert other objects to raw bytes

# Empty values are called "NULL" in R, and "None" in Python
NULL
  # NULL is the absence of a value - an empty object. 
  # It is different from NA, which is a placeholder for a missing value.

# Basic Data Structures --------------------------------------------------

# a simple ordered sequence is called a "vector" in R
# a vector can only contain one atomic type of data (numeric, integer, logical, character, or complex). In fact, a single number, string, etc. is a vector of length 1.
# (Python has no single-type sequence like this)
default_vector <- vector()
twoone <- c(2,1) # 'c' stands for "combine" or "concatenate"
c('A','B')
c(A=TRUE, B=FALSE) # you can name the elements of a vector

  # indexing and manipulating vectors
  twoone[1] # first element of the vector
  twoone[c(2,1)] # a vector of the second and first elements of the vector
  "A" %in% c('A','B') # check if "A" is in the vector
  twoone[twoone > 1] # a vector of the elements of the vector that are greater than 1
  sort(twoone) # sort the vector in ascending order

# a flexible ordered sequence is called a "list" in R and in Python
# a list can contain any type of object, including other lists
default_list <- list()
mixed_list <- list(c(2,1), 'B')
named_list <- list(A=c(TRUE,TRUE)) # you can name the elements of a list

  # indexing lists
  mixed_list[1] # first element of the list (list of length 1)
  mixed_list[[1]] # first element of the list (just the element itself)
  mixed_list[[1]][2] # second element of the first element of the list
  named_list[["A"]] # the value of A
  named_list$A # also the value of A






# a flexible unordered sequence is called an "environment" in R, and a "dictionary" or "dict" in Python
# this is a hash table, which maps "keys" (names) to "values" so that they can be looked up quickly
# in R we almost never use environments directly, but they are available because R uses them to keep track of objects in memory
my_env <- new.env()
my_env$A <- 1
my_env$B <- 2
my_env$A # look up the value of A
my_env[["B"]] # look up the value of B







# R has no built-in set data structure, but you can use a vector to represent a set
union(c(1,2,3), c(2,3,4)) # the union of two sets
intersect(c(1,2,3), c(2,3,4)) # the intersection of two sets
setdiff(c(1,2,3), c(2,3,4)) # the difference of two sets
setequal(c(1,2,3), c(3,2,1)) # check if two sets are equal







# Shortcuts --------------------------------------------------------------

2:10 # a vector of the numbers 1 through 10
3:1 # a vector of the numbers 3 through 1
seq_len(23) # a vector of the numbers 1 through 23
seq(1, 10, by=2) # a vector of the numbers 1 through 10, counting by 2
LETTERS # a built-in vector of the uppercase letters of the alphabet
letters # a built-in vector of the lowercase letters of the alphabet
pi

# Type Coercion ----------------------------------------------------------

1L + 1.03 # an integer and a numeric are coerced to numeric
as.integer(1.5) # convert a numeric to an integer (truncates the decimal)
as.numeric(1L) # convert an integer to a numeric
as.numeric("10") # convert a string to a number
as.character(1:10) # convert a number to a string
as.logical(c(1,0)) # convert a number to a logical value (1 = TRUE, 0 = FALSE)

# Mutability -------------------------------------------------------------

# R has no mutable objects except environments 
# (although some mutability is used behind the scenes for performance reasons).
# So you never have to worry about accidentally changing an object when you pass it to a function, when you assign it to a new variable, etc.








# Other Common Data Structures -------------------------------------------

# arrays are called "array" and "matrix" in R, and "ndarray" in the numpy Python library
# arrays are just vectors with a "dim" attribute that specifies the dimensions of the array or matrix
default_array <- array() # arrays can have any number of dimensions, but matrices are always 2-dimensional
default_matrix <- matrix() # matrices are 2-dimensional arrays
identity_matrix <- diag(3) # a 3x3 identity matrix
matrix(c('Alligator','Ardvark','Bat','Bear'), nrow=2) # matrices can contain any atomic type of data, but all elements must be the same type
random_matrix <- matrix(rnorm(9), nrow=3) # a 3x3 matrix of random numbers from a normal distribution
random_array <- array(rnorm(27), dim=c(3,3,3)) # a 3x3x3 array of random numbers from a normal distribution
random_matrix[1,] # the first row of the matrix
random_matrix[,1] # the first column of the matrix
random_matrix[2,3] # the element in the second row and third column of the matrix
random_array[1,1,1] # the element in the first row, first column, and first "depth" of the array
  # for more, see numerical_data.R


# R doen't need an equivalent of the pandas Series, since vectors can have index names


named_vector <- c(couple=2, few=3, dozen=12) # a vector with index names
named_vector["couple"] # look up the element with index "couple"
names(named_vector) # the index names of the vector (a character vector)



# a rectangular bundle of named columns is called a "data.frame" in R, and a "DataFrame" in the pandas Python library
default_data_frame <- data.frame()
shapes <- data.frame(shape=c('circle','square','triangle'), sides=c(0,4,3))
shapes$sides # each column is a vector, which can be accessed by name
shapes[['sides']] # same thing
unclass(shapes) # a data.frame is just a list of vectors with a "row.names" attribute
  # we will have much more to say about data.frames in tabular_data.R

# a categorical variable is called a "factor" in R, and a "category" in the pandas Python library
# internally, a factor is just a vector of integers with a mapping from the integers to the levels of the factor
default_factor <- factor()
alphabet_factor <- factor(c('B','B','A','C'), levels=c('A','B','C'))
levels(alphabet_factor) # the levels of the factor (a character vector)
as.integer(alphabet_factor) # the underlying integer representation of the factor
alphabet_factor <- ordered(alphabet_factor) # mark the factor as ordered (i.e. ordinal)
library(forcats) # for advanced factor manipulation in R (included in tidyverse)
fct_reorder(alphabet_factor, c('C','B','A')) # reorder the levels of the factor
fct_recode(alphabet_factor, one='A', two='B') # recode the levels of the factor
fct_collapse(alphabet_factor, AB=c('A','B')) # collapse levels of the factor
fct_lump_min(alphabet_factor, 2) # lump the least frequent levels into a single level

# a date+time is called "POSIXct" in R, and a "datetime" in Python
library(lubridate) # for advanced date-time manipulation in R (included in tidyverse)
birthtime <- ymd_hms("1990-01-01 12:00:00") # January 1, 1990 at noon
date(birthtime) # the date part of the date-time
# R has no built-in time-only type (use the hms package if needed)
year(birthtime) # the year (an integer)
month(birthtime) # the month (an integer)
day(birthtime) # the day (an integer)
hour(birthtime) # the hour (an integer)
minute(birthtime) # the minute (an integer)
second(birthtime) # the second (an integer)
wday(birthtime) # the day of the week (an integer, 1 = Sunday)
wday(birthtime, label=TRUE) # the day of the week (an ordered factor)
with_tz(birthtime, tzone=Sys.timezone()) # convert the datetime to the local timezone
as.numeric(birthtime) # convert the datetime to a Unix timestamp (seconds since 1970-01-01 00:00:00 UTC)
stamp("March 2, 2000")(birthtime) # format the datetime as a string, matching the format of the example
ymd_hms("1990-01-01 12:00:00", tz="America/New_York") # parse a string into a datetime
age <- difftime(now(), birthtime, units="days") # the difference between two datetimes is a "difftime" object
age <- as.period(age) # convert the difftime to a "period" object (from the lubridate package)
day(age) / 365.25 # convert the period to years (approximately)
  # for more, see the lubridate cheatsheet: https://rstudio.github.io/cheatsheets/html/lubridate.html
