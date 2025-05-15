
import os
import streamlit as st
import requests
import json
import base64


def set_background(image_path):
    abs_path = os.path.join(os.path.dirname(__file__), image_path)
    with open(abs_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: bottom;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


st.set_page_config(page_title="🏏 Match Winner Predictor", layout="centered")
set_background("bg_img.jpg")
st.title("🏏 Cricket Match Winner Predictor")

# Constants
top_teams = ['England', 'India', 'Australia', 'New Zealand', 'Pakistan', 'South Africa', 'Sri Lanka', 'West Indies']
match_types = ['Test', 'T20', 'ODI']
toss_decisions = ['bat', 'field']

# Load stadiums_by_country.json
json_path = os.path.join(os.path.dirname(__file__), "..", "stadiums_by_country.json")
with open(json_path, "r") as f:
    stadium_data = json.load(f)

# User Inputs with placeholders
team_1 = st.selectbox("Select Team 1", ["-- Select Team 1 --"] + top_teams)
team_2_options = [team for team in top_teams if team != team_1]
team_2 = st.selectbox("Select Team 2", ["-- Select Team 2 --"] + team_2_options)

match_type = st.selectbox("Match Type", ["-- Match Type --"] + match_types)

venue_country = st.selectbox("Venue Country", ["-- Venue Country --"] + list(stadium_data.keys()))
venue = st.selectbox("Venue", ["-- Venue --"] + (stadium_data.get(venue_country, []) if venue_country in stadium_data else []))

home_team = st.selectbox("Home Team", ["-- Home Team --"] + [t for t in [team_1, team_2] if t not in ["-- Select Team 1 --", "-- Select Team 2 --"]])
toss_winner = st.selectbox("Toss Winner", ["-- Toss Winner --"] + [t for t in [team_1, team_2] if t not in ["-- Select Team 1 --", "-- Select Team 2 --"]])
toss_decision = st.selectbox("Toss Decision", ["-- Toss Decision --"] + toss_decisions)

# Check if all fields are valid (i.e. not placeholder)
fields_filled = all([
    team_1 not in ["-- Select Team 1 --"],
    team_2 not in ["-- Select Team 2 --"],
    match_type not in ["-- Match Type --"],
    venue_country not in ["-- Venue Country --"],
    venue not in ["-- Venue --"],
    home_team not in ["-- Home Team --"],
    toss_winner not in ["-- Toss Winner --"],
    toss_decision not in ["-- Toss Decision --"]
])

# Prediction
if fields_filled:
    if st.button("Predict Winner"):
        input_payload = {
            "team_1": team_1,
            "team_2": team_2,
            "toss_winner": toss_winner,
            "toss_decision": toss_decision,
            "venue": venue,
            "match_type": match_type,
            "home_team": home_team
        }

        try:
            response = requests.post("https://de-project-5p9z.onrender.com/predict", json=input_payload)
            result = response.json()
            st.success(f"🏆 Predicted Winner: **{result['predicted_winner']}**")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
else:
    st.warning("Please select all fields to enable prediction.")
