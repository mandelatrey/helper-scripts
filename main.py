import os
import shutil

def move_files_with_keyword(keyword):
    # Get the home directory
    home_dir = os.path.expanduser('~')
    
    # Create the destination directory if it doesn't exist
    dest_dir = os.path.join(home_dir, keyword)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created directory: {dest_dir}")

    # Walk through the home directory
    for root, dirs, files in os.walk(home_dir):
        for file in files:
            if keyword in file:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_dir, file)
                
                # Move the file
                shutil.move(src_file, dest_file)
                print(f"Moved file: {src_file} to {dest_file}")

if __name__ == "__main__":
    keyword = input("Enter the keyword to search for: ")
    move_files_with_keyword(keyword)