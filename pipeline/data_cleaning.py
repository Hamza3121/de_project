
import os
import json
import random

clean_dir = "./clean_data"
os.makedirs(clean_dir, exist_ok=True)

root_folder = 'raw_data'
top_teams = ['England', 'India', 'Australia', 'New Zealand', 'Pakistan', 'South Africa', 'Sri Lanka', 'West Indies']
sub_folders = ['odis_data', 't20i_data', 'tests_data']

weather_conditions = ['Sunny', 'Humid', 'Cold']
weather_by_country = {
    "India": "Humid",
    "Pakistan": "Sunny",
    "England": "Cold",
    "Australia": "Sunny",
    "New Zealand": "Cold",
    "South Africa": "Sunny",
    "Sri Lanka": "Humid",
    "West Indies": "Humid"
}
weather_map = {
    "Sunny": "bat_first",
    "Humid": "field_first",
    "Cold": "field_first"
}

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
venue_map_path = os.path.join(BASE_DIR, "venue_map_dict.json")
stadium_country_map_path = os.path.join(BASE_DIR, "stadiums_by_country.json")

# Load venue_map_dict.json
with open(venue_map_path, 'r', encoding='utf-8') as f:
    venue_map = json.load(f)

# Load stadiums_by_country.json
with open(stadium_country_map_path, 'r') as f:
    stadium_country_map = json.load(f)

# Create reverse map: venue -> country
venue_to_country = {}
for country, stadiums in stadium_country_map.items():
    for stadium in stadiums:
        venue_to_country[stadium] = country

# Looping over all the json files of different format to only get match data
for sub_folder in sub_folders:
    folder_path = os.path.join(root_folder, sub_folder)

    combined_data = []

    for json_file in os.listdir(folder_path):
        json_file_path = os.path.join(folder_path, json_file)

        with open(json_file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                teams = data['info']['teams']
                # teams = sorted(data['info']['teams'])

                if teams[0] in top_teams and teams[1] in top_teams:

                    # Getting home team name
                    venue_name = venue_map.get(data['info']['venue'], data['info']['venue'])
                    venue_country = venue_to_country.get(venue_name, teams[0])

                    # Getting winner team
                    outcome = data['info'].get('outcome', {})
                    if 'winner' in outcome:
                        winner = outcome['winner']
                    else:
                        if venue_country == 'UAE':
                            home_team = teams[0]
                        elif venue_country == 'Bangladesh':
                            home_team = teams[1]
                        else:
                            winner = venue_country

                    # Adding home team
                    if venue_country == 'UAE':
                        home_team = teams[0]
                    elif venue_country == 'Bangladesh':
                        home_team = teams[1]
                    else:
                        home_team = venue_country

                    # Weather
                    weather = weather_by_country.get(home_team)
                    weather_favour = weather_map.get(weather)

                    # Toss
                    toss_decision = data['info']['toss']['decision']
                    toss_aligned = int(weather_favour == f"{toss_decision}_first")

                    # Creating match data object
                    match_data = {
                        'match_type': data['info']['match_type'],
                        'team_1': teams[0],
                        'team_2': teams[1],
                        'venue': venue_name,
                        'home_team': home_team,
                        'toss_winner': data['info']['toss']['winner'],
                        'toss_decision': toss_decision,
                        'weather': weather,
                        'weather_favour': weather_favour,
                        'toss_aligned_with_weather': toss_aligned,
                        'winner': winner
                    }
                    combined_data.append(match_data)

            except json.JSONDecodeError:
                print("json_file_path --->", json_file_path)

    # Adding the clean data to relative match file
    output_file = os.path.join(clean_dir, f"{sub_folder}_cleaned.json")
    with open(output_file, 'w', encoding='utf-8') as out_f:
        json.dump(combined_data, out_f, indent=2)

    print(f"Saved cleaned data to: {output_file}\n")


