# Browser-Based Project Creator

## Description

This tool provides a web-based Graphical User Interface (GUI) for creating new software projects, offering a more interactive way to achieve functionality similar to what might be found in a shell script like `create-project.sh`. It simplifies the process of scaffolding new Python or JavaScript projects, setting up appropriate folder structures, and initializing basic environments. All created projects are conveniently organized within a `created_projects` directory.

## Features

*   **Web Interface:** Easy-to-use web form for specifying project parameters.
*   **Language Support:**
    *   **Python:** Creates a Python project structure, with an option to automatically create a virtual environment (`venv`).
    *   **JavaScript:** Generates a basic JavaScript project with `index.html`, `main.js`, `styles.css`, and a `package.json`.
*   **Organized Output:** All generated projects are stored within a dedicated `created_projects` directory in the application's root.
*   **User Feedback:** Provides on-screen messages about the success or failure of operations and the path to the created project.

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    ```
    (Or download and extract the project files if not using Git).

2.  **Navigate to Project Directory:**
    ```bash
    cd <project-directory-name>
    ```

3.  **Install Dependencies:**
    It's highly recommended to create a virtual environment first.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
    Then, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Run the Flask App:**
    Ensure your virtual environment is activated.
    ```bash
    python app.py
    ```

2.  **Access in Browser:**
    Open your web browser and navigate to:
    [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## How to Use

1.  **Open the Web Interface:** Navigate to `http://127.0.0.1:5000/` in your browser.
2.  **Fill Out the Form:**
    *   **Project Type:** Choose to create a new folder for your project or just a single file within the `created_projects` directory.
    *   **Folder Name:** If creating a new folder, specify its name. This will also be used as the project name for JavaScript projects if "New Folder" is selected.
    *   **File Name:** Specify the main script file name (e.g., `script.py`, `app.js`). Defaults to `main.py` for Python if left blank.
    *   **Language:** Select either Python or JavaScript.
    *   **Python Options:**
        *   Choose whether to create a Python virtual environment.
        *   Specify a name for the virtual environment folder (defaults to `venv`).
    *   **JavaScript Options:**
        *   Specify your JavaScript project's name (used for `package.json` and the project folder if "Single File" is selected for JS).
3.  **Submit:** Click the "Create Project" button.
4.  **Check Feedback:** The page will reload, and messages will appear at the top indicating the results of the operations. The absolute path to your newly created project or file will be displayed, along with a suggestion to `cd` into the directory and run `code .` to open it in Visual Studio Code.

All generated projects will be located in the `created_projects` directory within the application's main folder.
