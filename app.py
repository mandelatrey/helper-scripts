from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess

app = Flask(__name__)
app.secret_key = os.urandom(24) # Required for flash messages

CREATED_PROJECTS_DIR = 'created_projects'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_project', methods=['POST'])
def create_project():
    project_type = request.form.get('project_type')
    folder_name = request.form.get('folder_name', '').strip()
    file_name_input = request.form.get('file_name', '').strip()
    language = request.form.get('language')
    create_python_env = request.form.get('create_python_env') == 'yes'
    python_env_name = request.form.get('python_env_name', 'venv').strip()
    js_project_name_input = request.form.get('js_project_name', 'my_js_app').strip()

    base_path_for_projects = os.path.join(os.getcwd(), CREATED_PROJECTS_DIR)
    os.makedirs(base_path_for_projects, exist_ok=True)
    
    project_path_final_for_vscode_msg = base_path_for_projects # Default, e.g. for single file in root of created_projects

    if language == 'python':
        project_path_for_python = base_path_for_projects
        if project_type == 'new_folder':
            if not folder_name:
                flash("Folder name is required for 'New Folder' project type.", 'danger')
                return redirect(url_for('index'))
            project_path_for_python = os.path.join(base_path_for_projects, folder_name)
        
        os.makedirs(project_path_for_python, exist_ok=True)
        project_path_final_for_vscode_msg = project_path_for_python
        flash(f"Base project directory set to: {project_path_for_python}", "info")

        actual_file_name_py = file_name_input if file_name_input else "main.py"
        python_file_path = os.path.join(project_path_for_python, actual_file_name_py)

        try:
            with open(python_file_path, 'w') as f:
                f.write("# Automatically generated Python file\n\n")
                f.write("print('Hello, Python world!')\n")
            flash(f"Successfully created Python file: {python_file_path}", 'success')
        except IOError as e:
            flash(f"Error creating Python file {python_file_path}: {e}", 'danger')
            return redirect(url_for('index'))

        if create_python_env:
            if not python_env_name:
                python_env_name = "venv" # Default if empty after strip
            env_path = os.path.join(project_path_for_python, python_env_name)
            try:
                subprocess.run(['python', '-m', 'venv', env_path], check=True, capture_output=True, text=True)
                flash(f"Python virtual environment '{python_env_name}' created at {env_path}", 'success')
            except subprocess.CalledProcessError as e:
                flash(f"Error creating Python venv: {e.stderr}", 'danger')
            except FileNotFoundError:
                flash("Error: 'python' command not found. Make sure Python is installed and in PATH.", 'danger')

    elif language == 'javascript':
        js_project_dir_name = folder_name if project_type == 'new_folder' and folder_name else js_project_name_input
        if not js_project_dir_name: # Fallback if js_project_name_input was also empty
            js_project_dir_name = 'my_js_project'
            
        js_project_path = os.path.join(base_path_for_projects, js_project_dir_name)
        os.makedirs(js_project_path, exist_ok=True)
        project_path_final_for_vscode_msg = js_project_path
        flash(f"JavaScript project directory created: {js_project_path}", "success")

        # Create index.html
        js_index_html_path = os.path.join(js_project_path, 'index.html')
        try:
            with open(js_index_html_path, 'w') as f:
                f.write('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>JS Project</title>')
                f.write('<link rel="stylesheet" href="styles.css"></head><body><h1>JS Project</h1>')
                f.write('<script src="main.js"></script></body></html>')
            flash(f"Created index.html for JS project at {js_index_html_path}", 'success')
        except IOError as e:
            flash(f"Error creating JS index.html: {e}", 'danger')

        # Create main.js
        js_main_js_path = os.path.join(js_project_path, 'main.js')
        try:
            with open(js_main_js_path, 'w') as f:
                f.write("// Automatically generated JavaScript file\n\n")
                f.write("console.log('Hello, JavaScript world from main.js!');\n")
            flash(f"Created main.js for JS project at {js_main_js_path}", 'success')
        except IOError as e:
            flash(f"Error creating JS main.js: {e}", 'danger')

        # Create styles.css
        js_styles_css_path = os.path.join(js_project_path, 'styles.css')
        try:
            with open(js_styles_css_path, 'w') as f:
                f.write("/* Basic styles */")
            flash(f"Created styles.css for JS project at {js_styles_css_path}", 'success')
        except IOError as e:
            flash(f"Error creating JS styles.css: {e}", 'danger')

        # Create package.json
        package_json_path = os.path.join(js_project_path, 'package.json')
        actual_js_project_name = os.path.basename(js_project_path) # Use the actual folder name for package name
        try:
            with open(package_json_path, 'w') as f:
                f.write('{\n')
                f.write(f'  "name": "{actual_js_project_name}",\n')
                f.write('  "version": "1.0.0",\n')
                f.write('  "main": "main.js",\n')
                f.write('  "scripts": {\n')
                f.write('    "start": "node main.js"\n')
                f.write('  },\n')
                f.write('  "keywords": [],\n')
                f.write('  "author": "",\n')
                f.write('  "license": "ISC",\n')
                f.write('  "description": ""\n')
                f.write('}\n')
            flash(f"Created package.json for JS project at {package_json_path}", 'success')
        except IOError as e:
            flash(f"Error creating package.json for JS project: {e}", 'danger')
    else:
        # Generic file creation if no language or other type selected
        # This part might need adjustment based on whether "single_file" without language should do anything
        generic_file_path = base_path_for_projects
        if project_type == 'new_folder' and folder_name:
            generic_file_path = os.path.join(base_path_for_projects, folder_name)
            os.makedirs(generic_file_path, exist_ok=True)
            project_path_final_for_vscode_msg = generic_file_path
            flash(f"Project directory created: {generic_file_path}", "success")
        elif project_type == 'new_folder' and not folder_name:
             flash("Folder name is required for 'New Folder' project type.", 'danger')
             return redirect(url_for('index'))


        if file_name_input: # Only create file if a name is given
            actual_generic_file_name = file_name_input
            full_generic_file_path = os.path.join(generic_file_path, actual_generic_file_name)
            try:
                with open(full_generic_file_path, 'w') as f:
                    f.write("# File created by Project Creator\n")
                flash(f"Successfully created file: {full_generic_file_path}", 'success')
                if project_path_final_for_vscode_msg == base_path_for_projects : # if single file in root of created_projects
                    project_path_final_for_vscode_msg = full_generic_file_path # vscode points to the file itself
            except IOError as e:
                flash(f"Error creating file {full_generic_file_path}: {e}", 'danger')
        elif project_type == 'single_file' and not file_name_input and language not in ['python', 'javascript']:
             flash("File name is required for 'Single File' of generic type.", 'warning')


    flash(f'Project operations complete. Your project is at: {os.path.abspath(project_path_final_for_vscode_msg)}. You can cd into it and run "code ." (if Visual Studio Code is installed).', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
