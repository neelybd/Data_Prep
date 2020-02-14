# *********************************************************************************************************************
# Import Statement
from file_handling import *
from selection import *
# *********************************************************************************************************************

print("Function: Data Prep")
print("Release: 0.0.1")
print("Date: 2020-02-14")
print("Author: Brian Neely and David Liau")
print()
print()
print(".")
print()
print()

# Common data types
file_types = (("Comma Separated Values", "*.csv"), ("Text", "*.txt"), ("All", "*.*"))

# Select Data Files
files_in = select_multiple_files("Select Data Files", file_types)
