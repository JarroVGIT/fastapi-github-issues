import os
import shutil
from glob import glob

files_to_copy = []

# the string we want to find in the text files.
search_string = "searchstring"

copy_to_folder = "SO/filename_and_content_search/copy_folder/"

print(os.getcwd())
# Files are in folder {current_working_directory}/SO/filename_and_content_search/folder/
# I want all files with a '4' in the filename:
for name in glob("SO/filename_and_content_search/folder/*[4]*.txt"):
    with open(name, "r") as file:
        # read all content from a file using read()
        content = file.read()
        # check if string present or not
        if search_string in content:
            files_to_copy.append(name)

for file in files_to_copy:
    # Note the split, we just want the file name (the part after the last '/')
    shutil.copy2(file, copy_to_folder + file.split("/")[-1])
