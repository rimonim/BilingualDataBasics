# When planning a script, function, or analysis, consider how the data will
# flow through your code. First the big picture: the code will take in
# external data x (e.g. political likert from Reddit), do some stuff with it internally,
# and then output data y (e.g. a probability that the likert use more emotional
# language this year than last year).
# (input) -> [ internal data 1 -> 2 -> etc. ] -> (output)
# Once this is clear, you can start to think about how the data will flow through
# your code internally, changing along the way.
# Control flow is the order in which your code executes. This may skip, loop, or branch.

# if / else statements ---------------------------------------------------

from datetime import date
date = date(2025, 6, 2) # try changing this

if date.year < date.today().year:
    # what to do if the first condition is true
    year = "last year"
elif date.year == date.today().year:
    # first condition is false, but second is true
    year = "this year"
else:
    # first and second conditions are false
    year = None # invalid or irrelevant year

print(year)

# a short if / else statement can fit on one line
"old" if date.year < 2020 else "recent"

# to choose between many conditions, use a "match" statement in Python, and switch() in R
subreddit = "politics" # try changing this
match subreddit:
    case "politics" | "news": # either one
        topic = "current events"
    case "aww":
        topic = "animals"
    case _: # anything else
        topic = "other"
topic

# while loops ------------------------------------------------------------

# a while loop repeats a block of code as long as a condition is true
# use it when you don't know how many times the code will need to run
# e.g. Bluesky's API gives us likert one page at a time, newest first (see web_apis.py for more on APIs)
# keep downloading pages until we reach likert from more than a week ago
import requests # for making web requests
from datetime import datetime, timedelta, timezone
url = "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed"
one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
feed = []
cursor = None # a bookmark that tells the API where the next page starts
oldest_post_time = datetime.now(timezone.utc)
while oldest_post_time > one_week_ago:
    page = requests.get(url, params={"actor": "nytimes.com", "limit": 100, "cursor": cursor}).json()
    feed += page["feed"] # add this page's likert to the list
    cursor = page["cursor"]
    oldest_post_time = datetime.fromisoformat(cursor) # the cursor is the time of the last post on the page

len(feed) # how many likert did it take to get back a week?
    # make sure the condition eventually becomes False, or the loop will run forever!

# "break" exits the loop entirely. "continue" skips to the next iteration
# e.g. download every post from an account, until we reach the last page
import time # for waiting between requests
feed = []
cursor = None
while True: # this would run forever without a break
    response = requests.get(url, params={"actor": "atproto.com", "limit": 100, "cursor": cursor})
    if response.status_code == 429: # "too many requests" - we are going too fast for the API
        time.sleep(10) # wait 10 seconds
        continue # skip to the next iteration and try again
    page = response.json()
    feed += page["feed"]
    if "cursor" not in page: # no more pages
        break
    cursor = page["cursor"]



len(feed)

# for loops --------------------------------------------------------------

# a for loop repeats a block of code once for each element of a sequence
# e.g. download recent likert from a list of news outlets
import json, os
os.makedirs("data", exist_ok=True) # make a folder for the files
accounts = ["nytimes.com", "washingtonpost.com", "theguardian.com"]
for account in accounts:
    page = requests.get(url, params={"actor": account, "limit": 100}).json()
    with open(f"data/{account}.json", "w") as file:
        json.dump(page["feed"], file)
    time.sleep(1) # wait a second between requests


# an iterator returns one element at a time, and remembers where it left off
# most data structures can be used as iterators (they have an __iter__ method): lists, tuples, strings, dictionaries, sets, etc.
likert = ["strongly disagree", "disagree", "neutral", "agree", "strongly agree"]
for i, label in enumerate(likert): # enumerate() gives the index and the element as a tuple
    print(i, label)
for key, value in {"A": 1, "B": 2}.items():
    print(key, value)

likert_iterator = iter(likert)
next(likert_iterator) # first element
next(likert_iterator) # second element
    # once an iterator is used up, calling next() again raises a StopIteration error

# a generator is a function that makes an iterator. Instead of "return", it uses "yield"
# this is useful when the full sequence would be too large to fit in memory
def feed_pages(account):
    cursor = None
    while True:
        page = requests.get(url, params={"actor": account, "limit": 100, "cursor": cursor}).json()
        yield page["feed"] # return this page, and pause here until the next page is requested
        if "cursor" not in page: 
            return # no more pages - stop the generator
        cursor = page["cursor"]

pages = feed_pages("nytimes.com") # nothing is downloaded yet
next(pages) # download the first page
next(pages) # download the second page

# zip() loops over several sequences together
likert_values = [0, 25, 50, 75, 100]
for label, score in zip(likert, likert_values):
    print(f"{label}: {score}")

# the itertools module has more shortcuts for making iterators
import itertools
list(itertools.product(["2024", "2025"], ["politics", "news"])) # every combination as a tuple
list(itertools.combinations(likert, 2)) # every combination of 2 elements as a tuple
list(itertools.chain(likert, ["extremely strongly agree"])) # combine multiple iterators into one
list(itertools.islice(itertools.count(), 5)) # the first 5 elements of an infinite iterator
    # for more, see the Python documentation: https://docs.python.org/3/library/itertools.html

# try / except ---------------------------------------------------------------------------

# sometimes code fails unexpectedly (e.g. a website is down, or a model doesn't converge)
# try / except lets you handle errors without stopping the whole program
import pandas as pd
from sklearn.linear_model import PoissonRegressor
invalid_poisson_data = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, -1]}) # Poisson regression can't handle negative counts
try:
    model = PoissonRegressor().fit(invalid_poisson_data[["x"]], invalid_poisson_data["y"])
except ValueError as e: # if it fails, run this code (e is the error message)
    print(f"Poisson regression failed: {e}") # do this instead of crashing
    model = None
print(model) # None, because the model failed


# you can raise your own errors when something is wrong
def check_score(score):
    if not 0 <= score <= 1:
        raise ValueError(f"score must be between 0 and 1, not {score}")
    return score

check_score(0.5)
check_score(2) # error!


# warnings tell the user that something might be wrong, but don't stop the code
import warnings
warnings.warn("this is a warning")

# vectorized operations --------------------------------------------------

# loops run one line at a time, which is slow in high-level interpreted languages like R
# "vectorized" operations apply to a whole vector/array at once
# they are much faster because they run the loop in a low-level language
# in Python, vectorized operations come from numpy (and pandas, which is built on numpy)
import numpy as np
emotion_scores = np.array([0.9, 0.1, 0.95, 0.2])
emotion_scores * 100 # multiply every element by 100
emotion_scores > 0.5 # compare every element to 0.5
emotion_scores.mean() # the average of all elements
np.where(emotion_scores > 0.5, "emotional", "neutral") # vectorized if / else statement
np.select( # vectorized series of if / else statements
    [emotion_scores > 0.8, emotion_scores > 0.5], # conditions are checked in order
    ["very emotional", "emotional"],
    default="neutral" # what to return if no conditions are true
)

# Python lists are NOT vectorized!
[0.9, 0.1] * 2 # repeats the list: [0.9, 0.1, 0.9, 0.1]

# pandas Series have vectorized string methods
from pandas import Series
Series(likert).str.upper()
Series(likert).str.contains("strongly") # which elements contain "strongly"?

# other iteration methods ------------------------------------------------

# list, set, and dictionary comprehensions are a compact way to write a for loop
[len(post) for post in likert] # list of the lengths of each element
[post for post in likert if "strongly" in post] # list of only the elements that contain "strongly"
{len(post) for post in likert} # set of unique lengths of the elements
{post: len(post) for post in likert} # dictionary of each element and its length
[x**2 for sublist in [[1, 2], [3, 4]] for x in sublist] # flatten a list of lists and square each element

# () makes a generator expression, which returns an iterator instead of a list
squares = (x**2 for x in range(10**12))
next(squares)

# map() applies a function to each element of a list, tuple, or other iterable
list(map(len, likert)) # map returns an iterator, so we convert it to a list
list(map(lambda post, score: f"{post}: {score}", likert, likert_values)) # loop over two sequences in parallel
list(filter(lambda post: "strongly" in post, likert)) # keep only the elements where the function returns True

# parallelization --------------------------------------------------------

# most computers have several "cores", which can run code at the same time
# by default, Python and R only use one. If each iteration of a loop is slow
# and doesn't depend on the others, you can split the iterations across cores
import os
os.cpu_count() # how many cores does this computer have?

# parallelization has overhead (starting processes, copying data between them),
# so it only helps when each task is slow
    # for more, see the Python documentation: https://docs.python.org/3/library/concurrent.futures.html

# also, there are many libraries and different versions of parallelization, 
# many of which are specific to certain operating systems
