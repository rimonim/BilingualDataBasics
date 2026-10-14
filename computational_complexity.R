# Some code runs in a second, and some takes a week. 
# Some data fits on your laptop, and some doesn't.

# Measuring Time ---------------------------------------------------------

# a simple function to time
add_up <- function(n) {
  total <- 0
  for (i in seq_len(n)) {
    total <- total + i
  }
  total
}

start <- Sys.time() # the current time
add_up(1e6)
Sys.time() - start # how long did that take?
system.time(add_up(1e6)) # shortcut. "elapsed" is the time that passed on the clock

# a single measurement is noisy, since your computer is doing other things at the same time
# the bench package runs the code many times for a more reliable estimate
library(bench)
mark(add_up(1e6), iterations = 10) # "median" is the typical time per run

# try n, then 2n, then 4n
ns <- c(1e6, 2e6, 4e6)
timings <- press(n = ns, mark(add_up(n))) # press() runs mark() for each value of n
timings[c("n", "median")] # each time n doubles, the time doubles

# Big O notation --------------------------------------------------
# *Computational complexity* is how the time (or memory) a piece of 
# code takes grows as the data gets bigger.

# O(1) = "constant time": same speed with 10 elements or 10 million
participants <- 1:1e6
participants[500000] # jumping to a position is instant, no matter how long the vector is

# O(n), "linear time": double the data, double the time
999999 %in% participants # has to look through every element
add_up(1e6) # one step per number

# O(n^2), "quadratic time" (e.g. a loop inside a loop)
has_duplicates <- function(ids) {
  for (i in seq_along(ids)) {
    for (j in seq_along(ids)) {
      if (i != j && ids[i] == ids[j]) return(TRUE)
    }
  }
  FALSE
}

ids <- sample(1e9, 4000) # 4,000 unique random IDs between 1 and 1 billion
has_duplicates(ids) # 4,000 x 4,000 = 16 million comparisons
timings <- press(n = c(1000, 2000, 4000), mark(has_duplicates(ids[1:n])))
timings[c("n", "median")] # each time n doubles, the time quadruples
timings$median[3] * (1e6 / 4000)^2 # at this rate, how long would 1 million IDs take?
  # we will see a much faster way to do this below

# O(2^n), "exponential time": time doubles for every extra element

# note: vectorization (see control_flow.R) and parallelization make code faster by a constant factor,
# often 10-100x, but they don't change the shape of the growth.
# an O(n^2) algorithm that is 100x faster is still O(n^2)

# Memory -----------------------------------------------------------------
# 1 byte = 8 bits (binary). 1 KB = 1,000 bytes, 1 MB = 1,000 KB, 1 GB = 1,000 MB, 1 TB = 1,000 GB

# computer memory from fast + small to slow + large:
#   CPU cache: a few MB, built into the processor (very fast)
#   RAM: usually 8-32 GB on a laptop (fast)
#   "disk" (SSD or hard drive): usually 0.25-2 TB (slow)
#   network (cloud storage, databases): unlimited (very slow)

# R objects are in RAM (except for some specialized packages)
# reading a file copies it from disk into RAM. 
# if your objects don't fit in RAM, the operating system 
# starts "swapping" pieces of RAM to disk (or R crashes)
# to see your RAM usage, open Activity Monitor (Mac) or Task Manager (Windows)


object.size(1.5) # even a single number is a vector, with some extra information attached

scores <- runif(1e6) # a million random decimal numbers
object.size(scores) # R stores each number in exactly 8 bytes ("double")
  # R has no smaller decimal type
object.size(as.list(scores)) # a list stores each number as a separate object, which takes 8x more memory

# text takes more memory than numbers
likert <- rep(c("strongly agree", "agree", "neutral", "disagree", "strongly disagree"), times = 200000) # a million responses
object.size(likert) # about 8 MB: R stores each unique string once, and each response is an 8-byte pointer to it
object.size(factor(likert)) # much less - each label is stored once, plus integer codes


# most operations create a new object, which takes up more memory
# (see Mutability in data_structures.py)
scores_pct <- scores * 100 # a new 8 MB vector: now we're using 16 MB
rm(scores_pct) # delete objects to free up memory

# Heuristics -------------------------------------------------------------
# if your code is slow or uses too much memory, one of these might help

# 1. Vectorize! Don't use loops if you can avoid it (especially in R)
  # for more on vectorization, see control_flow.R

# 2. Don't grow objects (e.g. vectors, data frames) one piece at a time
# "adding" an element really means copying the whole thing into a new, bigger object: O(n^2)
# instead, make an object of the right size first, then fill it in


# 3. (R doesn't encourage using hash tables unless they are built into a package)







# remember our O(n^2) duplicate finder? anyDuplicated() uses a hash table to do it in O(n)
anyDuplicated(ids) > 0

# 4. Don't recalculate the same thing over and over again. 
# Do it once and save it in a variable (and/or a file) for later use.

# 5. Use the right file format for the job (see files.R)
