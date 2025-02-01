#!/bin/bash

#create a folder
create_folder() {
    read -p 'Enter name of the new folder : ' folder_name
    cd
    cd "desktop/repos"
    mkdir "$folder_name"
    cd "$folder_name"
}

#create  new file
create_file() {
    while true; do
        read -p 'Enter the name of your new file: ' filename
        if [[ '$filename' == *.* ]]; then
            touch '$filename'
            echo 'file '$filename' has been created'
            break
        else
            echo 'invalid filename '$filename'. Please add ext or file type'
        fi
    done
}

#set up python environment
setup_python_env() {
    read -p "Wanna create a python env y/n : " create_env
    if [[ "$create_env" == "y" ]]; then
        read -p 'What should we call your env? : ' env_name
        python3 -m venv "$env_name"
        echo "Success. $env_name created. Opening VS Code window"
        cd $env_name
    else
        touch main.py
        
    fi
}

#creating javascript workflow
create_js_project() {
    read -p "whats your project called: " javascript_project
    mkdir "$javascript_project"
    cd "$javascript_project"
    touch index.html main.js styles.css
    echo "created project '$javascript_project'"
}

#main script
read -p "Do you wanna create a new folder in repos (y/n): " folder_choice

echo "You entered '$folder_choice' for YES"

if [[ "$folder_choice" == "y" ]]; then
    create_folder
else
    create_file
fi

read -p "Choose your language. Enter 1 for Python, 2 for Javascript: " language

if [[ "$language" == "1" ]]; then
    setup_python_env
elif [[ "$language" == "2" ]]; then
    create_js_project
else
    echo "Unsupported language. exiting"
    exit 1
fi

code .