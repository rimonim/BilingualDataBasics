# If you need to use the same or similar code in multiple places, make it a function.
# Functions are named blocks of code that can be called from other parts of your program. 
# They can take in input objects, called "arguments" or "parameters", and return an output object.
# Calling a function is like stepping into a separate room to do something:
# The code inside the function doesn't see the code outside the function unless it needs to
# (e.g. there is a variable that is not defined inside the function) and the code outside 
# the function only sees the output (if there is one).

# Using Existing Functions -----------------------------------------------

# We have already used many built-in functions, such as isinstance(), and str().
# To see what a function does and how to use it, you can use the help() function or the ? operator
# ?isinstance
help(isinstance)

# Defining New Functions -------------------------------------------------

def snake_to_title(string, prefix = ""):
    """
    Convert a string from snake_case to Title Case
    
    Parameters:
    string (str): a string in snake_case
    prefix (str): an optional prefix to prepend to the output (default is "")
    
    Returns:
    str: The converted string.
    """ # This is a docstring. It is attached to the function and can be accessed with ?snake_to_title
    string = string.replace("_", " ")
    string = string.title()
    string = prefix + string
    return string # Python requires an explicit return statement

snake_to_title("my_variable")
snake_to_title("my_variable", prefix = "A: ")
snake_to_title("my_variable", "A: ") # no need to name the arguments if you provide them in order

# bonus question: what can't this Python function do that the R version can? 
# (hint: in R, a string is a character vector of length 1)

# functions can also take arbitrary numbers of arguments using the *args and **kwargs syntax
# this is useful for passing arguments to other functions.
# One (*) is for positional arguments, two (**) for named arguments.
def snake_to_bold_title(string, **kwargs):
    string = snake_to_title(string, **kwargs)
    string = "**" + string + "**"
    return string

snake_to_bold_title("my_variable", prefix = "This is ")

# lambda functions (one-line functions with no name)
# useful for passing a function as an argument to another function
import numpy as np
matrix_list = [np.array([[1, 2], [3, 4]]), np.array([[5, 6], [7, 8]])]
# for example, map() applies a function to each element of a list or other iterable
list(map(lambda x: x * 2, matrix_list)) # multiply each matrix by 2

# Object Methods ---------------------------------------------------------

# some object types have "methods", special functions that are associated with that object type
len([1, 2, 3]) # lists have a "len" method
[1, 2, 3].__len__() # same thing, but using the method directly
"some text".upper() # strings have an "upper" method

# Object-oriented programming or OOP uses classes and methods instead of functions. 
# Classes bundle data (attributes) and functionality (methods) together in a reusable way.
# OOP is beyond the scope of this course, but you can read more about it here: https://docs.python.org/3/tutorial/classes.html

# Testing ----------------------------------------------------------------
# IT IS VERY EASY TO WRITE CODE THAT RUNS BUT DOESN'T DO WHAT YOU WANT
## You should always test your code to make sure it does what you want.
## Write tests early and run them often.

# we recommend using the pytest package
# make a new file called test_snake_to_title.py and write tests in it:

def outputs_title_case():
    assert snake_to_title("my_variable") == "My Variable"
    assert snake_to_title("my_variable", prefix = "A: ") == "A: My Variable"
    assert snake_to_title("my_variable", "A: ") == "A: My Variable"

def works_when_input_is_not_snake_case():
    assert snake_to_title("My Variable") == "My Variable"
    assert snake_to_title("my variable") == "My Variable"
    assert snake_to_title("my-variable") == "My-Variable"
    assert snake_to_title("myVariable") == "Myvariable"

# to run the tests, run "pytest -v" in the terminal
# this finds all files that start with "test_" and runs all functions that start with "test_"

# Debugging --------------------------------------------------------------
# what do you do when your code doesn't do what you expect?

# Positron is a modified version of VS Code, which has extensive debugging tools
# Set a breakpoint by clicking in the left margin of the code editor, then "Run and Debug" in the left sidebar
# see https://code.visualstudio.com/docs/python/debugging for more information