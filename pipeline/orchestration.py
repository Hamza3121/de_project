
import subprocess
import os
import sys


def run_script(script_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, script_name)

    print(f"Running {script_path}...")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error in {script_name}:\n{result.stderr}")
        exit(1)

    print(f"Output of {script_name}:\n{result.stdout}")


# Directly calling scripts
run_script("data_ingestion.py")
run_script("data_cleaning.py")
run_script("data_loading.py")
