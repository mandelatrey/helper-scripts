import os
import zipfile
import shutil
from pathlib import Path

# Import tkinter for the file dialog
import tkinter as tk
from tkinter import filedialog

def install_fonts(zip_path):
    """
    Extracts and installs fonts from a ZIP file into the system font directory on macOS.
    """
    # Define font directories
    home = str(Path.home())
    font_dir = os.path.join(home, 'Library', 'Fonts')  # User font directory
    temp_extract_dir = os.path.join(home, 'Downloads', 'extracted_fonts')
    
    # Ensure the temp directory is empty
    if os.path.exists(temp_extract_dir):
        shutil.rmtree(temp_extract_dir)
    os.makedirs(temp_extract_dir)
    
    # Extract the ZIP file
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_extract_dir)
        print(f"Extracted fonts to {temp_extract_dir}")
    except zipfile.BadZipFile:
        print("Error: Invalid ZIP file.")
        return
    
    # Identify font files
    font_extensions = ('.ttf', '.otf', '.dfont')
    font_files = [f for f in os.listdir(temp_extract_dir) if f.endswith(font_extensions)]
    
    if not font_files:
        print("No valid font files found in the ZIP.")
        return
    
    # Install fonts
    for font in font_files:
        font_path = os.path.join(temp_extract_dir, font)
        shutil.move(font_path, os.path.join(font_dir, font))
        print(f"Installed: {font}")
    
    # Cleanup
    shutil.rmtree(temp_extract_dir)
    print("Font installation complete!")

if __name__ == "__main__":
    # Initialize tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open file dialog to select the ZIP file
    zip_file_path = filedialog.askopenfilename(
        title="Select Font ZIP File",
        filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
    )

    if zip_file_path:
        print(f"Selected ZIP path: {zip_file_path}")
        install_fonts(zip_file_path)
    else:
        print("No ZIP file selected.")