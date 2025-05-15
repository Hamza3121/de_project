
import os
import json
import pandas as pd

root_folder = "clean_data"
all_matches = []

# Loading json files from clean_data and adding all matches data to a single list
for json_file in os.listdir(root_folder):
    json_file_path = os.path.join(root_folder, json_file)

    with open(json_file_path, 'r', encoding='utf-8') as f:
        matches = json.load(f)
        all_matches.extend(matches)

# Exporting data to csv
df = pd.DataFrame(all_matches)
df.to_csv("final_data.csv", index=False)

print("final_data.csv has been created.")
