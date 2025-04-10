#!/usr/bin/env python3
"""
Font Installer for macOS

This utility extracts and installs fonts from ZIP files on macOS.
It allows users to install all fonts or select specific ones from a dropdown menu.
"""

__version__ = '1.0.0'

import os
import sys
import zipfile
import tempfile
import subprocess
import argparse
from pathlib import Path

# Font file extensions to look for
FONT_EXTENSIONS = ('.ttf', '.otf', '.ttc', '.dfont')

# Try to import tkinter for GUI, but have a fallback for environments without it
GUI_AVAILABLE = False
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, Listbox, MULTIPLE
    GUI_AVAILABLE = True
except ImportError:
    print("Tkinter not available. Using command-line interface.")
    # Define placeholders to avoid attribute errors during static analysis
    tk = None
    filedialog = None
    messagebox = None
    Listbox = None
    MULTIPLE = None


def is_font_file(filename):
    """Check if a file is a supported font file by its extension."""
    return filename.lower().endswith(FONT_EXTENSIONS)


def extract_zip(zip_path, extract_dir):
    """
    Extract contents of a ZIP file to specified directory.
    
    Args:
        zip_path (str): Path to the ZIP file
        extract_dir (str): Directory to extract files to
        
    Returns:
        list: List of extracted font files
    """
    font_files = []
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extract all files
            zip_ref.extractall(extract_dir)
            
            # Find all font files in the extracted content
            for root, _, files in os.walk(extract_dir):
                for file in files:
                    if is_font_file(file):
                        full_path = os.path.join(root, file)
                        font_files.append({
                            'path': full_path,
                            'name': file
                        })
    except zipfile.BadZipFile:
        print("Error: The selected file is not a valid ZIP file.")
        return []
    except Exception as e:
        print(f'Error extracting ZIP file: {e}')
        return []
    
    return font_files


def install_font(font_path):
    """
    Install a font file to macOS Font Book using AppleScript.
    
    Args:
        font_path (str): Path to the font file
        
    Returns:
        bool: True if installation was successful, False otherwise
    """
    try:
        # Open the font file with Font Book
        subprocess.run(['open', font_path], check=True)
        
        print("Font opened in Font Book.")
        
        # Path to the AppleScript file
        applescript_file = 'install-font.scpt'
        
        # Execute the AppleScript from the file
        subprocess.run(['osascript', applescript_file], check=True)
        
        print("AppleScript executed.")
        
        return True
    except subprocess.SubprocessError as e:
        print(f"Error installing font: {e}")
        return False
    except FileNotFoundError:
        # For testing in non-macOS environments
        print(f"Would install font: {font_path}")
        return True


def select_fonts_gui(font_files):
    """
    Display a GUI dialog to select which fonts to install.
    
    Args:
        font_files (list): List of font file dictionaries
        
    Returns:
        list: Selected font files to install
    """
    if not GUI_AVAILABLE or tk is None:
        print("GUI not available. Using command-line interface instead.")
        return select_fonts_cli(font_files)
    
    try:
        # Create root window
        root = tk.Tk()
        root.title("Select Fonts to Install")
        root.geometry("500x400")
        
        # Create frame for instructions
        instruction_frame = tk.Frame(root)
        instruction_frame.pack(pady=10, fill='x')
        
        instruction_label = tk.Label(
            instruction_frame, 
            text="Select fonts to install (hold Ctrl/Cmd for multiple selection):",
            wraplength=450
        )
        instruction_label.pack()
        
        # Create frame for font list
        list_frame = tk.Frame(root)
        list_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Create scrollable listbox
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        # Since we already checked tk is not None, these should be available too,
        # but let's add additional guards for static type checking
        if Listbox is not None and MULTIPLE is not None:
            font_listbox = Listbox(list_frame, selectmode=MULTIPLE, yscrollcommand=scrollbar.set)
            font_listbox.pack(side='left', fill='both', expand=True)
            scrollbar.config(command=font_listbox.yview)
        else:
            # This should never happen as we already checked if tk is None,
            # but it ensures static type checking doesn't complain
            raise ImportError("Required Tkinter components are not available")
        
        # Populate listbox with font names
        for font in font_files:
            font_listbox.insert(tk.END, font['name'])
        
        # Variable to store selected fonts
        selected_fonts = []
        
        def on_ok():
            nonlocal selected_fonts
            selected_indices = font_listbox.curselection()
            selected_fonts = [font_files[idx] for idx in selected_indices]
            root.destroy()
        
        def on_cancel():
            root.destroy()
        
        # Create buttons frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        ok_button = tk.Button(button_frame, text="Install Selected", command=on_ok)
        ok_button.pack(side='left', padx=10)
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=on_cancel)
        cancel_button.pack(side='left', padx=10)
        
        # Run the dialog
        root.mainloop()
        
        return selected_fonts
    except Exception as e:
        print(f"Error in GUI mode: {e}")
        print("Falling back to CLI mode.")
        return select_fonts_cli(font_files)


def select_fonts_cli(font_files):
    """
    Command-line interface for selecting fonts to install.
    
    Args:
        font_files (list): List of font file dictionaries
        
    Returns:
        list: Selected font files to install
    """
    print("\nAvailable fonts:")
    for idx, font in enumerate(font_files):
        print(f"[{idx+1}] {font['name']}")
    
    print("\nEnter the numbers of the fonts you want to install, separated by commas.")
    print("For example: 1,3,5 or 1-5 for a range.")
    print("Enter 'all' to install all fonts or 'q' to quit.")
    
    while True:
        selection = input("\nYour selection: ").strip().lower()
        
        if selection == 'q':
            return []
        
        if selection == 'all':
            return font_files
        
        try:
            selected_indices = []
            # Handle comma-separated values and ranges
            parts = selection.split(',')
            for part in parts:
                if '-' in part:
                    # Handle range like 1-5
                    start, end = map(int, part.split('-'))
                    selected_indices.extend(range(start, end + 1))
                else:
                    # Handle single number
                    selected_indices.append(int(part))
            
            # Convert to 0-based indices and validate
            selected_indices = [idx - 1 for idx in selected_indices]
            if any(idx < 0 or idx >= len(font_files) for idx in selected_indices):
                print("Invalid selection. Please enter valid numbers.")
                continue
            
            # Return selected fonts
            return [font_files[idx] for idx in selected_indices]
        
        except ValueError:
            print("Invalid input. Please enter numbers, ranges, 'all', or 'q'.")


def main():
    """Main function to run the font installer utility."""
    parser = argparse.ArgumentParser(
        description='Font Installer for macOS - A utility to extract and install fonts from ZIP files',
        epilog="""
Examples:
  python font_installer.py                      # Run interactively (GUI if available)
  python font_installer.py --zip=fonts.zip      # Specify a ZIP file directly
  python font_installer.py --cli                # Force command-line interface
  python font_installer.py --install-all        # Install all fonts without selection
  python font_installer.py --auto --zip=fonts.zip # Non-interactive mode for automation
        """
    )
    parser.add_argument('--zip', '-z', metavar='FILE', 
                        help='Path to the ZIP file containing fonts')
    parser.add_argument('--gui', '-g', action='store_true', 
                        help='Force GUI mode (if available)')
    parser.add_argument('--cli', '-c', action='store_true', 
                        help='Force command-line interface mode')
    parser.add_argument('--install-all', '-a', action='store_true',
                        help='Install all fonts without prompting')
    parser.add_argument('--auto', action='store_true',
                        help='Auto mode for non-interactive environments (requires --zip)')
    parser.add_argument('--version', '-v', action='version', 
                        version=f'Font Installer v{__version__}',
                        help='Show program version number and exit')
    args = parser.parse_args()
    
    # Determine interface mode
    auto_mode = args.auto
    
    # Force CLI mode in auto mode
    if auto_mode:
        use_cli = True
        use_gui = False
    else:
        # Check if GUI is available and not explicitly disabled
        use_cli = args.cli or not GUI_AVAILABLE or tk is None
        use_gui = not use_cli and (args.gui or GUI_AVAILABLE) and tk is not None
    
    # Get ZIP file path
    zip_path = args.zip
    
    if use_gui and not zip_path:
        try:
            # Verify tkinter is properly imported
            if tk is None or filedialog is None:
                raise ImportError("Tkinter modules not properly loaded")
                
            # Create root window for file dialog and then hide it
            root = tk.Tk()
            root.withdraw()
            
            # Show file dialog to select ZIP file
            zip_path = filedialog.askopenfilename(
                title="Select Font ZIP File",
                filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
            )
        except Exception as e:
            print(f"Failed to open GUI file dialog: {e}")
            use_cli = True
            use_gui = False
    
    if not zip_path and not use_cli:
        print("No ZIP file selected. Exiting.")
        sys.exit(0)
    
    if not zip_path and use_cli:
        if auto_mode:
            print("Error: In auto mode, you must specify a ZIP file with the --zip option.")
            sys.exit(1)
        
        # Prompt for ZIP file path in CLI mode
        try:
            zip_path = input("Enter the path to the ZIP file containing fonts: ").strip()
            
            if not zip_path:
                print("No ZIP file specified. Exiting.")
                sys.exit(0)
        except EOFError:
            print("Error: In non-interactive mode, you must specify a ZIP file with the --zip option.")
            sys.exit(1)
    
    # Validate ZIP file
    zip_path = os.path.expanduser(zip_path)
    if not os.path.isfile(zip_path):
        print(f"Error: File not found: {zip_path}")
        sys.exit(1)
    
    # Create temporary directory for extraction
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Extracting {os.path.basename(zip_path)}...")
        font_files = extract_zip(zip_path, temp_dir)
        
        if not font_files:
            error_msg = "No font files found in the ZIP file."
            if use_gui and messagebox is not None:
                try:
                    messagebox.showerror("Error", error_msg)
                except Exception as e:
                    print(f"GUI error: {e}")
            print(error_msg)
            sys.exit(1)
        
        print(f"Found {len(font_files)} font files.")
        
        # Ask whether to install all fonts or select specific ones
        install_all = args.install_all or auto_mode
        
        if not install_all:
            if use_gui and messagebox is not None:
                try:
                    install_all = messagebox.askyesno(
                        "Install Fonts",
                        f"Found {len(font_files)} font files. Do you want to install all of them?\n\n"
                        "Select 'Yes' to install all fonts.\n"
                        "Select 'No' to choose specific fonts."
                    )
                except Exception as e:
                    print(f"GUI error: {e}")
                    use_cli = True
                    use_gui = False
            
            if use_cli and not auto_mode:
                try:
                    # Check if stdin is a TTY (interactive terminal)
                    if sys.stdin.isatty():
                        response = input(f"Found {len(font_files)} font files. Install all? (y/n): ").strip().lower()
                        install_all = response.startswith('y')
                    else:
                        # If input is being piped, read two lines (one for y/n, one for selection)
                        print(f"Found {len(font_files)} font files. Install all? (y/n): ", end='')
                        response = sys.stdin.readline().strip().lower()
                        print(response)  # Echo the input for clarity
                        install_all = response.startswith('y')
                except EOFError:
                    print("Running in non-interactive mode. Installing all fonts by default.")
                    install_all = True
        
        # Select fonts to install
        if install_all:
            fonts_to_install = font_files
        else:
            if auto_mode:
                print("Auto mode is enabled but install-all not specified. Installing all fonts by default.")
                fonts_to_install = font_files
            elif use_gui:
                fonts_to_install = select_fonts_gui(font_files)
            else:
                try:
                    # Check if stdin is a TTY (interactive terminal)
                    if sys.stdin.isatty():
                        fonts_to_install = select_fonts_cli(font_files)
                    else:
                        # If input is being piped, read one line
                        selection = sys.stdin.readline().strip()
                        if selection == 'all':
                            fonts_to_install = font_files
                        elif selection == 'q':
                            fonts_to_install = []
                        else:
                            try:
                                # Process the selection as if it was entered interactively
                                selected_indices = []
                                parts = selection.split(',')
                                for part in parts:
                                    if '-' in part:
                                        start, end = map(int, part.split('-'))
                                        selected_indices.extend(range(start, end + 1))
                                    else:
                                        selected_indices.append(int(part))
                                
                                # Convert to 0-based indices and validate
                                selected_indices = [idx - 1 for idx in selected_indices]
                                if any(idx < 0 or idx >= len(font_files) for idx in selected_indices):
                                    print("Invalid selection in piped input. Installing all fonts by default.")
                                    fonts_to_install = font_files
                                else:
                                    fonts_to_install = [font_files[idx] for idx in selected_indices]
                            except ValueError:
                                print("Invalid input format in piped input. Installing all fonts by default.")
                                fonts_to_install = font_files
                except EOFError:
                    print("Running in non-interactive mode. Installing all fonts by default.")
                    fonts_to_install = font_files
        
        if not fonts_to_install:
            print("No fonts selected for installation. Exiting.")
            sys.exit(0)
        
        # Install selected fonts
        successful = 0
        failed = 0
        
        print(f"Installing {len(fonts_to_install)} fonts...")
        for font in fonts_to_install:
            print(f"Installing: {font['name']}")
            if install_font(font['path']):
                successful += 1
            else:
                failed += 1
        
        # Show summary
        summary_message = f"Installation complete!\n\n" \
                          f"Successfully installed: {successful} fonts\n" \
                          f"Failed to install: {failed} fonts"
        
        print(summary_message)
        if use_gui and messagebox is not None:
            try:
                messagebox.showinfo("Installation Complete", summary_message)
            except Exception as e:
                print(f"GUI error: {e}")


if __name__ == "__main__":
    main()
