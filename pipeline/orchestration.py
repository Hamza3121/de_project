
import subprocess
import os
import sys
import shutil

# Set base dir to the project root (de_project/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def run_script(script_name):
    script_path = os.path.join(BASE_DIR, "pipeline", script_name)
    print(f"Running {script_path}...")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error in {script_name}:\n{result.stderr}")
        exit(1)

    print(f"Output of {script_name}:\n{result.stdout}")


def clean_temp_folders():
    folders_to_delete = ["raw_data", "clean_data"]
    streamlit_run_dir = os.getcwd()

    for folder in folders_to_delete:
        folder_path = os.path.join(streamlit_run_dir, folder)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print(f"Deleted folder: {folder_path}")
        else:
            print(f"Folder not found (skipped): {folder_path}")


# Run scripts
run_script("data_ingestion.py")
run_script("data_cleaning.py")
run_script("data_loading.py")
clean_temp_folders()
