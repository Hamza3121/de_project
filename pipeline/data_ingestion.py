
import requests
import zipfile
import io
import os

base_url = "https://cricsheet.org/"
formats = {
    "tests": "downloads/tests_json.zip",
    "odis": "downloads/odis_json.zip",
    "t20i": "downloads/t20s_json.zip"
}

root_dir = "./raw_data"
os.makedirs(root_dir, exist_ok=True)

for format_name, format_url in formats.items():
    print(f"Downloading and extracting {format_name} data...")
    response = requests.get(f'{base_url}{format_url}')

    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            extract_path = os.path.join(root_dir, f"{format_name}_data")
            os.makedirs(extract_path, exist_ok=True)
            z.extractall(extract_path)

            # Removing README file
            readme_path = os.path.join(extract_path, "README.txt")
            if os.path.exists(readme_path):
                os.remove(readme_path)

            print(f"{format_name} data downloaded successfully\n")

    else:
        print(f"Failed to download {format_name} data...")
