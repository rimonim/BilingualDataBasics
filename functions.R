# If you need to use the same or similar code in multiple places, make it a function.
# Functions are named blocks of code that can be called from other parts of your program. 
# They can take in input objects, called "arguments" or "parameters", and return an output object.
# Calling a function is like stepping into a separate room to do something:
# The code inside the function doesn't see the code outside the function unless it needs to
# (e.g. there is a variable that is not defined inside the function) and the code outside 
# the function only sees the output (if there is one).

# Using Existing Functions -----------------------------------------------

# We have already used many built-in functions, such as is.numeric(), and str_replace_all()
# To see what a function does and how to use it, you can use the help() function or the ? operator
?is.numeric
help(is.numeric)

# Defining New Functions -------------------------------------------------

snake_to_title <- function(string, prefix = "") {
  # Convert a string from snake_case to Title Case
  #
  # Parameters:
  #   string: a string in snake_case
  #   prefix: an optional prefix to prepend to the output (default is "")
  #
  # Returns:
  #   The converted string.
  # (Note: R functions don't have built-in documentation unless they are in a package)
  string <- stringr::str_replace_all(string, "_", " ")
  string <- stringr::str_to_title(string)
  string <- paste0(prefix, string)
  string # no need for return(): R assumes the last line is the output
}

snake_to_title("my_variable")
snake_to_title("my_variable", prefix = "A: ")
snake_to_title("my_variable", "A: ") # no need to name the arguments if you provide them in order

# bonus question: what can this R function do that the Python version can't? 
# (hint: in R, a string is a character vector of length 1)

# functions can also take arbitrary numbers of arguments using the ... syntax
# this is useful for passing arguments to other functions. 
snake_to_bold_title <- function(string, ...) {
  string <- snake_to_title(string, ...)
  string <- paste0("**", string, "**")
  string
}

snake_to_bold_title("my_variable", prefix = "This ")

# lambda functions (one-line functions with no name)
# useful for passing a function as an argument to another function
matrix_list <- list(matrix(1:4, nrow = 2), matrix(5:8, nrow = 2))
# for example, lapply() applies a function to each element of a list or vector
lapply(matrix_list, function(x) x * 2) # multiply each matrix by 2
lapply(matrix_list, \(x) x * 2) # same thing

# Object Methods ---------------------------------------------------------

# some object types have "methods", special functions that are associated with that object type
as.data.frame.matrix(matrix(1:4, nrow = 2)) # matrices have a method to convert them to data frames
as.data.frame.character(c("a", "b", "c")) # character vectors have a different method to convert them to data frames
as.data.frame(matrix(1:4, nrow = 2)) # as.data.frame() automatically detects the object type

# Object-oriented programming or OOP uses classes and methods instead of functions. 
# When using packages, you will sometimes see syntax like object$method() or object@method(), which are OOP methods.
# OOP is beyond the scope of this course, but you can read more about it here: https://adv-r.hadley.nz/oo.html

# Testing ----------------------------------------------------------------
# IT IS VERY EASY TO WRITE CODE THAT RUNS BUT DOESN'T DO WHAT YOU WANT
## You should always test your code to make sure it does what you want.
## Write tests early and run them often.

library(testthat)

test_that("snake_to_title outputs title case", {
  expect_equal(snake_to_title("my_variable"), "My Variable")
  expect_equal(snake_to_title("my_variable_with_many_words"), "My Variable With Many Words")
  expect_equal(snake_to_title("myvariable"), "Myvariable") # even without underscores
})

test_that("snake_to_title works when input is not snake_case", {
  expect_equal(snake_to_title("My Variable"), "My Variable") # already title case
  expect_equal(snake_to_title("my variable"), "My Variable") # spaces instead of underscores
  expect_equal(snake_to_title("my-variable"), "My-Variable") # hyphens
  expect_equal(snake_to_title("myVariable"), "Myvariable") # camelCase
})

# Debugging --------------------------------------------------------------
# what do you do when your code doesn't do what you expect?

# Positron has built-in debugging tools for R
# Set a breakpoint by clicking in the left margin of the code editor, then "Run and Debug" in the left sidebar
# see https://positron.posit.co/guide-r-debugging.html for more information

# you can also use the browser() function to set a breakpoint in your code
# When the code reaches that line, it will pause.
# for individual functions, you can use debugonce(function_name) to trigger the debugger the next time that function is called