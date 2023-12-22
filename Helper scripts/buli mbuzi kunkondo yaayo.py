import os
import shutil

# directory to scan
#dir_path = os.path.expanduser("~/Downloads/")
dir_path = os.path.dirname(__file__)

# iterate through all the files in the directory
for filename in os.listdir(dir_path):
    if not filename.startswith('.'):
        # get the file extension
        ext = os.path.splitext(filename)[1][1:].strip().lower()

        # skip folders and files with no extension
        if os.path.isdir(filename) or not ext:
            continue

        # create subdirectory for the extension if it doesn't exist
        sub_dir = os.path.join(dir_path, ext)
        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)

        # move the file to the subdirectory
        source_file_path = os.path.join(dir_path, filename)
        dest_file_path = os.path.join(sub_dir, filename)
        shutil.move(source_file_path, dest_file_path)
