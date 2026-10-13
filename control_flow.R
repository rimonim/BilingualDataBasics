# When planning a script, function, or analysis, consider how the data will
# flow through your code. First the big picture: the code will take in
# external data x (e.g. political posts from Reddit), do some stuff with it internally,
# and then output data y (e.g. a probability that the posts use more emotional
# language this year than last year).
# (input) -> [ internal data 1 -> 2 -> etc. ] -> (output)
# Once this is clear, you can start to think about how the data will flow through
# your code internally, changing along the way.
# Control flow is the order in which your code executes. This may skip, loop, or branch.

# if / else statements ---------------------------------------------------

library(lubridate)
date <- ymd("2025-06-02") # try changing this

if (year(date) < year(today())) {
  # what to do if the first condition is true
  year <- "last year"
} else if (year(date) == year(today())) {
  # first condition is false, but second is true
  year <- "this year"
} else {
  # first and second conditions are false
  year <- NA # invalid or irrelevant year
}
print(year)

# a short if / else statement can fit on one line
if (year(date) < 2020) "old" else "recent"

# to choose between many conditions, use switch() in R, and a "match" statement in Python
subreddit <- "politics" # try changing this
topic <- switch(subreddit,
  politics = , # an empty value falls through to the next one
  news = "current events",
  aww = "animals",
  "other" # anything else
)
topic


# while loops ------------------------------------------------------------

# a while loop repeats a block of code as long as a condition is true
# use it when you don't know how many times the code will need to run
# e.g. Bluesky's API gives us posts one page at a time, newest first (see web_apis.R for more on APIs)
# keep downloading pages until we reach posts from more than a week ago
library(httr2) # for making web requests

url <- "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed"
one_week_ago <- now("UTC") - days(7) # using lubridate
feed <- list()
cursor <- NULL # a bookmark that tells the API where the next page starts
oldest_post_time <- now("UTC")
while (oldest_post_time > one_week_ago) {
  page <- request(url) |> req_url_query(actor = "nytimes.com", limit = 100, cursor = cursor) |> req_perform() |> resp_body_json()
  feed <- c(feed, page$feed) # add this page's posts to the list
  cursor <- page$cursor
  oldest_post_time <- ymd_hms(cursor) # the cursor is the time of the last post on the page
}
length(feed) # how many posts did it take to get back a week?
  # make sure the condition eventually becomes FALSE, or the loop will run forever!

# "break" exits the loop entirely. "next" skips to the next iteration.
# e.g. download every post from an account, until we reach the last page

feed <- list()
cursor <- NULL
repeat { # this would run forever without a break, same as while (TRUE)
  response <- request(url) |> req_url_query(actor = "atproto.com", limit = 100, cursor = cursor) |> req_error(is_error = \(resp) FALSE) |> req_perform()
  if (resp_status(response) == 429) { # "too many requests" - we are going too fast for the API
    Sys.sleep(10) # wait 10 seconds
    next # skip to the next iteration and try again
  }
  page <- resp_body_json(response)
  feed <- c(feed, page$feed)
  if (is.null(page$cursor)) { # no more pages
    break 
  }
  cursor <- page$cursor
}
length(feed)

# for loops --------------------------------------------------------------

# a for loop repeats a block of code once for each element of a vector or list
# e.g. download recent posts from a list of news outlets

dir.create("data", showWarnings = FALSE) # make a folder for the files
accounts <- c("nytimes.com", "washingtonpost.com", "theguardian.com")
for (account in accounts) {
  page <- request(url) |> req_url_query(actor = account, limit = 100) |> req_perform() |> resp_body_json()
  jsonlite::write_json(page$feed, paste0("data/", account, ".json"), auto_unbox = TRUE)

  Sys.sleep(1) # wait a second between requests
}

# R has no system of iterators: loops just go over the elements of a vector or list

likert <- c("strongly disagree", "disagree", "neutral", "agree", "strongly agree")
for (i in seq_along(likert)) { # loop over the indices of the vector
  print(paste0(i, ": ", likert[i]))
}

# no generators either
# to work through something too large to fit in memory, process it in chunks
# (if you need a real generator, see the coro package)

















# R has no "zip" function
# to loop over several vectors together, loop over their indices
# or use the purrr package (included in tidyverse, see below)
likert_values <- c(0, 25, 50, 75, 100)
purrr::map2(likert, likert_values, \(x, y) paste0(x, ": ", y)) # loop over two vectors in parallel, return a list

# useful shortcuts for manipulating vectors and lists
unique(likert) # remove duplicates
tidyr::expand_grid(year = c("2024", "2025"), subreddit = c("politics", "news")) # every combination (as a data frame)
combn(likert, 2) # every pair of likert (as a matrix, with one pair per column)
append(likert, "extremely strongly agree") # add to the end, like c(likert, "extremely strongly agree")
sort(likert) # sort (alphabetically for strings)
order(likert) # the indices that would sort the vector

# try / except -----------------------------------------------------------

# sometimes code fails unexpectedly (e.g. a website is down, or a model doesn't converge)
# tryCatch() lets you handle errors without stopping the whole program
invalid_poisson_data <- data.frame(x = 1:3, y = c(1, 2, -1)) # Poisson regression can't handle negative counts
poisson_model <- tryCatch(
  glm(y ~ x, data = invalid_poisson_data, family = poisson()), # try to run this code
  error = \(e) { # if it fails, run this code (e is the error message)
    message("Poisson regression failed: ", e$message) # print the error message
    NULL
  }
)
poisson_model # NULL, because the model failed
  # try() is a simpler version of tryCatch() that just keeps going after an error

# you can raise your own errors when something is wrong
check_score <- function(score) {
  if (score < 0 || score > 1) {
    stop("score must be between 0 and 1, not ", score)
  }
  score
}
check_score(0.5)
check_score(2) # error!

# warnings tell the user that something might be wrong, but don't stop the code

warning("this is a warning")

# vectorized operations --------------------------------------------------

# loops run one line at a time, which is slow in high-level interpreted languages like R
# "vectorized" operations apply to a whole vector/array at once
# they are much faster because they run the loop in a low-level language
# in R, almost everything is vectorized (so you should almost never use for loops)

emotion_scores <- c(0.9, 0.1, 0.95, 0.2)
emotion_scores * 100 # multiply every element by 100
emotion_scores > 0.5 # compare every element to 0.5
mean(emotion_scores) # the average of all elements
ifelse(emotion_scores > 0.5, "emotional", "neutral") # vectorized if / else statement
dplyr::case_when( # vectorized series of if / else statements - similar to switch()
  emotion_scores > 0.8 ~ "very emotional", # conditions are checked in order
  emotion_scores > 0.5 ~ "emotional",
  .default = "neutral" # what to return if no conditions are true
)

# R vectors are always vectorized
c(0.9, 0.1) * 2 # multiplies each element: 1.8 0.2

# most R functions are vectorized, including string functions
nchar(likert) # how many characters are in each element?
toupper(likert) # or stringr::str_to_upper(likert)
grepl("strongly", likert) # or stringr::str_detect(likert, "strongly") 

# other iteration methods ------------------------------------------------

# R has no comprehensions like Python


# the apply family of functions apply a function to each element of a vector, list, or array
lapply(likert, nchar) # list of the lengths of each element
sapply(likert, nchar) # same, but tries to simplify the result to a vector
vapply(likert, nchar, integer(1)) # same, but you specify the output type (safer)

# the purrr package (included in tidyverse) has a more consistent version of the apply family
library(purrr)
map(likert, nchar) # always returns a list
map_int(likert, nchar) # returns an integer vector (or fails)
map2_chr(likert, likert_values, \(post, score) paste0(post, ": ", score)) # loop over two vectors in parallel
keep(likert, \(post) grepl("strongly", post)) # keep only the elements where the function returns TRUE
  # for more, see the purrr cheatsheet: https://rstudio.github.io/cheatsheets/html/purrr.html

# parallelization --------------------------------------------------------

# most computers have several "cores", which can run code at the same time
# by default, R and Python only use one. If each iteration of a loop is slow
# and doesn't depend on the others, you can split the iterations across cores
library(parallel) # comes with R
detectCores() # how many cores does this computer have?

# parallelization has overhead (starting processes, copying data between them),
# so it only helps when each task is slow
  # for more, see https://bookdown.org/rdpeng/rprogdatascience/parallel-computation.html

# also, there are many packages and different versions of parallelization, 
# many of which are specific to certain operating systems
