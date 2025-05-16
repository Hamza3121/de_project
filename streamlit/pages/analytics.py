
import streamlit as st
import sqlite3
import pandas as pd
import os

# Page configuration
st.set_page_config(page_title="📊 Team Stats", layout="centered")
st.title("📊 Team Win Percentages & Head-to-Head Stats")

# Connect to the SQLite database
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "final_data.db"))
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM matches", conn)
conn.close()

# -------------------- WIN PERCENTAGE --------------------
st.subheader("🏆 Overall Team Win Percentages")

# Extract all unique teams
all_teams = pd.unique(df[['team_1', 'team_2']].values.ravel())

# Total matches played by each team
matches_played = df['team_1'].value_counts() + df['team_2'].value_counts()

# Total wins by each team
wins = df['winner'].value_counts()

# Create stats DataFrame
win_stats = pd.DataFrame({
    'Matches Played': matches_played,
    'Matches Won': wins
}).fillna(0)

# Calculate win percentage
win_stats['Win %'] = (win_stats['Matches Won'] / win_stats['Matches Played']) * 100
win_stats = win_stats.sort_values('Win %', ascending=False)

# Display the DataFrame
st.dataframe(win_stats.style.format({"Win %": "{:.2f}%"}))

# -------------------- HEAD TO HEAD --------------------
st.markdown("---")
st.subheader("🤜🤛 Head-to-Head Comparison")

teams = sorted(all_teams)
team_a = st.selectbox("Select Team A", ["-- Select Team --"] + teams)
team_b = st.selectbox("Select Team B", [t for t in teams if t != team_a])

if team_a != "-- Select Team --" and team_b:
    # Filter relevant matches
    head_to_head = df[
        ((df['team_1'] == team_a) & (df['team_2'] == team_b)) |
        ((df['team_1'] == team_b) & (df['team_2'] == team_a))
    ]

    total_matches = len(head_to_head)
    wins_a = (head_to_head['winner'] == team_a).sum()
    wins_b = (head_to_head['winner'] == team_b).sum()

    st.metric(f"{team_a} Wins", wins_a)
    st.metric(f"{team_b} Wins", wins_b)
    st.metric("Total Matches", total_matches)

    # Bar chart for visualization
    st.bar_chart(pd.DataFrame({'Wins': [wins_a, wins_b]}, index=[team_a, team_b]))
