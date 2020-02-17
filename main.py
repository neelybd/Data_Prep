# *********************************************************************************************************************
# Import Statement
from file_handling import *
from os import *
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

# Open each of the files, automatically guessing their encoding
data = list()
for index, i in enumerate(files_in):
    data.append(open_unknown_csv(i, ','))
+
# Save files as comma delimited and UTF16
folder_out = select_folder()

for index, i in enumerate(data):
    # Get file name
    base_name = os.path.splitext(os.path.basename(files_in[index]))[0]

    # See if original file exists in the out
    if file_exist(folder_out, base_name + '.csv'):
        index_2 = 1

        # Append index to file name
        base_name_indexed = base_name + str(index_2) + '.csv'

        # Check if the new indexed name is present
        while file_exist(folder_out, base_name_indexed):
            index_2 = index_2 + 1
            base_name_indexed = base_name + str(index_2) + '.csv'

        # Final output name
        name_out = base_name_indexed

    else:
        # Final output name
        name_out = base_name + '.csv'

    i.to_csv(folder_out, sep=',', encoding='UTF16')
