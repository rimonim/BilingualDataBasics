# Exercises in R and/or Python

## 1. Object Types and Data Structures

```
responses = "agree, neutral, agree, strongly agree, disagree, agree"
```

1. Split the string into a sequence (a list in Python, a vector in R) of separate responses.
2. Count how many responses are `"agree"`.
3. Make a named lookup (a dict in Python, a named vector or list in R) that maps each of the five Likert labels (`"strongly disagree"` to `"strongly agree"`) to a score from 1 to 5. Use it to find the score for `"neutral"`.

## 2. Functions, Methods, and Testing

Write a function `likert_score(label, reverse = FALSE/False)` that returns the score (1 to 5) for a Likert label, using your lookup from Exercise 1. If `reverse` is true, it should return the reversed score (`"strongly agree"` → 1). Give the function a docstring or comment explaining what it does. Then write at least three tests (with `assert` in Python or `expect_equal()` in R) and run them.

## 3. Control Flow

Use a loop and your `likert_score()` function to score every response from Exercise 1. Then:

1. Add `"no opinion"` to the responses. Change your function so that an unknown label raises an error, and use `try`/`except` (Python) or `tryCatch()` (R) in the loop to record a missing value instead of crashing.
2. Do the same scoring again without writing a loop: use a comprehension, `map()`, or `sapply()`/`vapply()`.
