# In Python (and R too), everything is an object: numbers, text, lists, functions, and even libraries
# objects have a type
type(10) # the type of the number 10 is "int"
type("hello") # the type of the string "hello" is "str"

# Object Assignment -----------------------------------------------------
# usually we give objects names so we can refer to them later
# in Python, we use the assignment operator "="
x = 10 # assign the number 10 to the object named "x"
x # print the value of x
x + 5 # add 5 to the value of x = 15
x # x is still 10, because we didn't change it
x += 5 # this is shorthand for x = x + 5
x # now x is 15

# Atomic Data Types ------------------------------------------------------

# Decimal numbers are called "float" in Python, and "numeric" in R
# they are "floating point" numbers, since the decimal point can "float" to any position in the number
default_float = float()
age = 23.0
(age * 365 + 1.001) / 365
2.3e-4 # scientific notation for 0.00023
float('nan') # "not a number" - missing value for floating point numbers
isinstance(age, float) # check if age is a float

# Integers are called "int" in Python, and "integer" in R
default_int = int()
23
0
    # Python has no dedicated missing value for integers

# True/False values are called "bool" in Python, and "logical" in R
default_bool = bool()
True
False
    # Python has no dedicated missing value for booleans

# Text values are called "str" in Python, and "character" in R
default_str = str()
"Hello goodbye"
""
multiline_string = """This is a string
that spans multiple lines"""
    # Python has no dedicated missing value for strings

# String manipulation
multiline_string + "\nhere is another line" # concatenate
f"I am {age} years old" # f-strings are one of many ways to dynamically format strings in Python
# base Python has powerful string manipulation - no need for libraries like stringr in R
"hi " * 3 # repeat a string
"span" in multiline_string # check if a string is in another string
multiline_string[0:4] # a slice of the string, from index 0 to 3
multiline_string.title() # convert to title case
multiline_string.lower() # convert to lowercase
multiline_string.replace("string", "text") # replace a substring with another substring
multiline_string.split("\n") # split a string into a list of strings, using the newline character as the delimiter
multiline_string.count(" ") # count the number of spaces in the string
    # for more, see the Python documentation: https://docs.python.org/3/library/stdtypes.html#string-methods
    # for advanced string manipulation, see the re module for regular expressions: https://docs.python.org/3/library/re.html

# Complex numbers are called "complex" in Python and R
default_complex = complex()
1 + 2j
complex('nan') # missing value for complex numbers

# Raw bytes are called "bytes" in Python, and "raw" in R
default_bytes = bytes()
    # you wouldn't normally create raw bytes directly, 
    # but you can convert other types to raw bytes

# Empty values are called "NoneType" in Python, and "NULL" in R
None
    # None is the absence of a value - an empty object. 
    # It is different from NaN, which a placeholder for a missing number.

# Basic Data Structures ------------------------------------------------------

# (Python has no single-type sequence like R's vector)


# a flexible ordered sequence is called a "tuple" in Python and a "list" in R
# a tuple can contain any type of object, including other tuples
# Python also has another flexible ordered sequence called a "list"
# the difference is that a list is mutable (it can be changed after it is created, see Mutability below)

default_tuple = tuple()
mixed_tuple = ((2,1),'B') # tuples use parentheses (or no parentheses at all)
    # you can't name the elements of a tuple in Python

default_list = list()
integer_list = [3,1,3,5,6,143,2,3]
mixed_list = [[2,1],'B'] # lists use square brackets

# indexing lists and tuples
mixed_list[0] # first element of the list
mixed_list[0][1] # second element of the first element of the list
integer_list[-6::2] # from the 6th element from the end to the end, stepping by 2
'B' in mixed_list # check if 'B' is in the list
'C' not in mixed_list # check if 'C' is not in the list
mixed_list + ['D', 'E'] # concatenate two lists
mixed_tuple.count(2) # count the number of times 2 appears in the tuple

# unpacking lists and tuples
a, b = mixed_tuple # unpack the tuple into two variables
a, b = b, a # swap the values of a and b
a, *_ = mixed_list # unpack the first element of the list into a, and the rest into _

# manipulating lists
mixed_list.append('C') # add 'C' to the end of the list
mixed_list.insert(1, 'A') # insert 'A' at index 1
mixed_list.pop() # remove and return the last element of the list
mixed_list.remove('B') # remove 'B' from the list
sorted(integer_list) # return a new sorted list (does not change the original)
integer_list.sort() # sort the list in place
integer_list # the list is now sorted
list(zip([1,2,3], ['A','B','C'])) # combine two lists into a list of tuples
    # for more, see the Python documentation: https://docs.python.org/3/tutorial/datastructures.html

# a flexible, unordered, named set of values is called a "dictionary" or "dict" in Python and an "environment" in R
# this is a hash table, which maps "keys" (names) to "values" so that they can be looked up quickly
# keys can be any immutable type (numbers, strings, tuples). values can be any type
default_dict = dict()
my_dict = {"A": 1, "B": 2, (2,3): "a tuple"} # dictionaries use curly braces
my_dict["A"] # look up the value of A
my_dict["C"] = 3 # add a new key-value pair to the dictionary
del my_dict["B"] # remove the key-value pair with key "B"
my_dict.keys() # a list of the keys in the dictionary
my_dict.values() # a list of the values in the dictionary
list(my_dict.items()) # a list of the key-value pairs in the dictionary (as tuples)
my_dict.get("D", "other") # get the value of D, or return "other" if A is not in the dictionary

# a dictionary without values is called a "set" in Python
default_set = set()
my_set = {1, 2, 3}
my_set.add(4) # add 4 to the set
my_set.remove(2) # remove 2 from the set
my_set.union({5, 6}) # return a new set that is the union of my_set and {5, 6}
my_set.intersection({3, 4, 5}) # return a new set that is the intersection of my_set and {3, 4, 5}
my_set.difference({1, 3}) # return a new set that is the difference of my_set and {1, 3}

# Shortcuts --------------------------------------------------------------

list(range(10)) # a sequence of integers from 0 to 9
tuple(range(3, 10)) # a sequence of integers from 3 to 9
list(range(10, 0, -1)) # a sequence of integers from 10 to 1
list(range(0, 10, 2)) # a sequence of even integers from 0 to 8

# Type Coercion ----------------------------------------------------------

1 + 1.03 # an integer and a numeric are coerced to numeric
int(1.5) # convert a float to an integer (truncates the decimal)
float(1) # convert an integer to a float
float("10") # convert a string to a float
str(1) # convert an integer to a string
bool(1) # convert an integer to a boolean (0 is False, everything else is True)

# Mutability -------------------------------------------------------------

# Python distinguishes between mutable and immutable objects: 
# decimal numbers, integers, booleans, strings, and tuples are immutable, 
# while lists and dictionaries are mutable.
# (R has no mutable objects except environments, although some mutability is used behind the scenes for performance reasons. )

a = [3,2] # a is a list, which is mutable
b = a # b is now a reference to the same list as a
a.append(1) # add 1 to the end of the list
a # a is now [3,2,1]
b # b is also [3,2,1], because it refers to the same list

# Other Common Data Structures -------------------------------------------

# arrays and matrices are called "ndarray" in the numpy library, and "array" and "matrix" in R
import numpy as np
empty_array = np.array([]) # arrays can have any number of dimensions
empty_matrix = np.matrix([]) # matrices are 2-dimensional arrays
identity_matrix = np.eye(3) # a 3x3 identity matrix
np.array([['Alligator', 'Bat'],['Ardvark', 'Bear']]) # arrays can contain any type of data, but all elements must be the same type
# (numpy does have a "object" dtype that can contain mixed types, but it is not recommended if speed or memory usage is important)
random_matrix = np.random.rand(3,3) # a 3x3 matrix of random numbers between 0 and 1
random_array = np.random.rand(3,3,3) # a 3x3x3 array of random numbers between 0 and 1
random_matrix[0,:] # the first row of the matrix
random_matrix[:,0] # the first column of the matrix
random_matrix[2,3] # the element in the second row and third column of the matrix
random_array[0,0,0] # the element in the first row, first column, and first "depth" of the array
    # for more, see numerical_data.py

# in the pandas library, a 1-dimensional array with index names is called a "Series"
from pandas import Series
default_series = Series() 
named_column = Series([2, 3, 12], index=["couple", "few", "dozen"], name="amounts") 
named_column["couple"] # look up the element with index "couple"
named_column.index # the index of the Series (an array)
named_column.values # the values of the Series (an array)
named_column.name # Series can have a name (unlike vectors in R)

# a rectangular bundle of named columns is called a "DataFrame" in pandas, and a "data.frame" in R
from pandas import DataFrame
default_dataframe = DataFrame()
shapes = DataFrame({"shape": ["circle", "square", "triangle"], "sides": [0, 4, 3]})
shapes.sides # each column is a Series, which can be accessed by name
shapes["sides"] # same thing
    # we will have much more to say about DataFrames in tabular_data.py

# a categorical variable is called a "category" in the pandas library, and a "factor" in R












# a date + time is called a "datetime" in Python, and a "POSIXct" in R
from datetime import datetime # the datetime module comes with Python. The pandas library has its own datetime module, which is more powerful
birthtime = datetime(1990, 1, 1, 12, 0, 0) # January 1, 1990 at noon
birthtime.date() # the date part of the datetime
birthtime.time() # the time part of the datetime
birthtime.year # the year (an integer)
birthtime.month # the month (an integer)
birthtime.day # the day (an integer)
birthtime.hour # the hour (an integer)
birthtime.minute # the minute (an integer)
birthtime.second # the second (an integer)
birthtime.weekday() # the day of the week (0=Monday, 6=Sunday)
birthtime.astimezone() # convert the datetime to the local timezone
birthtime.timestamp() # convert the datetime to a Unix timestamp (seconds since 1970-01-01 00:00:00 UTC)
birthtime.strftime("%Y-%m-%d %H:%M:%S") # format the datetime as a string
datetime.strptime("1990-01-01 12:00:00", "%Y-%m-%d %H:%M:%S") # parse a string into a datetime
age = datetime.now() - birthtime # the difference between two datetimes is a timedelta object
age.days / 365.25 # convert the timedelta to years (approximately)
    # for more, see the time series chapter in Python for Data Analysis: https://wesmckinney.com/book/time-series
