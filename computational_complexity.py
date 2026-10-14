# Some code runs in a second, and some takes a week. 
# Some data fits on your laptop, and some doesn't.

# Measuring Time ---------------------------------------------------------

# a simple function to time
def add_up(n):
    total = 0
    for i in range(n):
        total += i
    return total


import time # comes with Python
start = time.perf_counter() # the current time in seconds (from an arbitrary starting point)
add_up(1_000_000)
time.perf_counter() - start # how long did that take?

# a single measurement is noisy
# the timeit module runs the code several times for a more reliable estimate
import timeit
timeit.timeit(lambda: add_up(1_000_000), number=10) / 10 # average seconds per run
    # or in the console type %timeit add_up(1_000_000)

# try n, then 2n, then 4n
ns = [1_000_000, 2_000_000, 4_000_000]
seconds = [timeit.timeit(lambda: add_up(n), number=3) / 3 for n in ns]
seconds # each time n doubles, the time doubles

# Big O notation --------------------------------------------------
# *Computational complexity* is how the time (or memory) a piece of 
# code takes grows as the data gets bigger.

# O(1) = "constant time": same speed with 10 elements or 10 million
participants = list(range(1_000_000))
participants[500_000] # jumping to a position is instant, no matter how long the list is

# O(n), "linear time": double the data, double the time
999_999 in participants # has to look through every element
add_up(1_000_000) # one step per number

# O(n^2), "quadratic time" (e.g. a loop inside a loop)
def has_duplicates(ids):
    for i in range(len(ids)):
        for j in range(len(ids)):
            if i != j and ids[i] == ids[j]:
                return True
    return False

import random # comes with Python
ids = random.sample(range(10**9), 4_000) # 4,000 unique random IDs between 0 and 1 billion
has_duplicates(ids) # 4,000 x 4,000 = 16 million comparisons
ns = [1_000, 2_000, 4_000]
timings = [timeit.timeit(lambda: has_duplicates(ids[:n]), number=1) for n in ns]
timings # each time n doubles, the time quadruples
(timings[2] * (1e6 / 4000)**2)/60/60 # at this rate, how long would 1 million IDs take?
    # we will see a much faster way to do this below

# O(2^n), "exponential time": time doubles for every extra element

# note: vectorization (see control_flow.py) and parallelization make code faster by a constant factor,
# often 10-100x, but they don't change the shape of the growth.
# an O(n^2) algorithm that is 100x faster is still O(n^2)

# Memory -----------------------------------------------------------------
# 1 byte = 8 bits (binary). 1 KB = 1,000 bytes, 1 MB = 1,000 KB, 1 GB = 1,000 MB, 1 TB = 1,000 GB

# computer memory from fast + small to slow + large:
#   CPU cache: a few MB, built into the processor (very fast)
#   RAM: usually 8-32 GB on a laptop (fast)
#   "disk" (SSD or hard drive): usually 0.25-2 TB (slow)
#   network (cloud storage, databases): unlimited (very slow)

# Python objects are in RAM (except for packages like numpy and pandas, which can store data on disk)
# reading a file copies it from disk into RAM. 
# if your objects don't fit in RAM, the operating system 
# starts "swapping" pieces of RAM to disk (or Python crashes)
# to see your RAM usage, open Activity Monitor (Mac) or Task Manager (Windows)

import sys
sys.getsizeof(1.5) # a Python float is an object with some extra information attached
import numpy as np
scores = np.random.rand(1_000_000) # a million random decimal numbers
scores.nbytes # numpy stores each number in exactly 8 bytes ("float64")
scores.astype(np.float32).nbytes # "float32" uses half the memory, but is less precise (about 7 digits instead of 16)
    # a Python list of a million floats takes about 4x more memory than a numpy array

# text takes more memory than numbers
from pandas import Series
likert = Series(["strongly agree", "agree", "neutral", "disagree", "strongly disagree"] * 200_000) # a million responses
likert.memory_usage(deep=True) # about 18 MB: every response is stored as its own string
likert.astype("category").memory_usage(deep=True) # much less - each label is stored once, plus integer codes

# many operations create a new object, which takes up more memory
# (but see Mutability in data_structures.py)
scores_pct = scores * 100 # a new 8 MB array: now we're using 16 MB
del scores_pct # delete objects to free up memory

# Heuristics -------------------------------------------------------------
# if your code is slow or uses too much memory, one of these might help

# 1. Vectorize! Don't use loops if you can avoid it
    # for more on vectorization, see control_flow.py

# 2. Don't grow numpy arrays and pandas DataFrames one piece at a time
# "adding" an element really means copying the whole thing into a new, bigger object: O(n^2)
# instead, make an object of the right size first, then fill it in
# Python lists leave extra room at the end, so appending to a list is ok

# 3. Use a hash table (a set or dictionary) for lookups
# a hash table converts each key directly into a memory index, which is O(1) instead of O(n)
all_ids = random.sample(range(10**9), 20_000) # all ids
excluded_ids = random.sample(all_ids, 5_000) # list of ids to exclude
excluded_set = set(excluded_ids) # the same ids as a set
timeit.timeit(lambda: [i for i in all_ids if i not in excluded_ids], number=1) # list: scans up to 5,000 IDs for each participant
timeit.timeit(lambda: [i for i in all_ids if i not in excluded_set], number=1) # set: about 1,000x faster

# remember our O(n^2) duplicate finder? With a set it's O(n)
len(set(ids)) < len(ids)

# 4. Don't recalculate the same thing over and over again. 
# Do it once and save it in a variable (and/or a file) for later use.

# 5. Use the right file format for the job (see files.py)
