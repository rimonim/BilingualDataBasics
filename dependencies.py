# A library (a.k.a. package, or 'module' if it's a single .py file) 
# is a collection of functions and/or data (sometimes including code in lower-level languages).
# To use a package:``
#   1. install it (in the terminal, usually once per project)
#   2. import it (in the code, once per session)

# uv add pandas (IN THE TERMINAL, not here) # downloads from PyPI
import pandas as pd # imports it into this session, with a short name
# it is good practice to load all packages at the top of the script
# (WARNING: the name you install is not always the name you import)
# (e.g  uv add scikit-learn  -> import sklearn)

import sys
sys.prefix # where Python looks for installed packages. Should be this project's .venv folder

# some packages come installed with Python, but you still have to import them 
# (e.g. math, statistics, random, os, sys, datetime)

# packages not on PyPI can be installed straight from GitHub (in the terminal)
# uv add git+https://github.com/pandas-dev/pandas

# Namespaces and masking -------------------------------------------------

# import keeps everything behind the package name, so nothing gets overwritten
import numpy as np
np.max([-1, 3]) # numpy's max
max(-1, 3) # Python's built-in max - no conflict

# R-style "load everything" is possible, but don't do it

# importing one specific name is fine
from pandas import DataFrame

# Versions ---------------------------------------------------------------

pd.__version__ # pandas version
sys.version # Python version
# in the terminal: uv pip list (everything installed, with versions)

# Reading documentation --------------------------------------------------

help(np.std) # in Jupyter or IPython: np.std?
# standard docstring format:
#   [function signature], Parameters, Returns, See Also, Notes, Examples


# long-form docs are online (numpy.org/doc, pandas.pydata.org/docs)

# excercise: why does R's sd() give a different answer than numpy's std()?
np.std([2, 4, 4, 4, 5, 5, 7, 9]) # 2.0
pd.Series([2, 4, 4, 4, 5, 5, 7, 9]).std() # this one matches R

# if needed, read the code itself 
# (right click function -> "Go to Definition" in Positron)
