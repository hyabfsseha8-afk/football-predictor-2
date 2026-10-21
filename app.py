import streamlit as st
import pandas as pd
import requests

# 1. Custom Styling 
st.markdown("""
    <style>
    .main { background-color: #f5f7f8; }
    h1 { color: #1e3d59; }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Football Predictor Data Hub")

# 2. API Setup - PASTE YOUR COPIED KEY DIRECTLY INSIDE THESE QUOTES
API_KEY = "83d3eaf8bc79498f91098bf16828d7ea"  
API_URL = "https://api.football-data.org/v4/competitions/PL/standings"
HEADERS = {"X-Auth-Token": API_KEY}

# 3. Fetch live data safely
# REMOVED THE CACHE DECORATOR TEMPORARILY TO FORCE STREAMLIT TO LIVE-REFRESH THE NEW KEY
def load_football_data():
    # If you forgot to swap it, show an error
    if API_KEY == "PASTE_YOUR_ACTUAL_API_KEY_HERE" or API_KEY == "":
        st.error("⚠️ The code is still seeing the placeholder text. Please paste your actual letters/numbers key into the quotes on line 16.")
        return None

    try:
        response = requests.get(API_URL, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            # The API layout returns standings as a list of dictionaries
            # We must target the first block in the list to extract the team rows
            standings_list = data['standings'][0]['table']
            df = pd.json_normalize(standings_list)
            
            cleaned_df = df[[
                'position', 
                'team.name', 
                'playedGames', 
                'won', 
                'draw', 
                'lost', 
                'goalsFor', 
                'goalsAgainst', 
                'goalDifference', 
                'points'
            ]]
            return cleaned_df
        elif response.status_code == 403:
            st.error("🚫 API Key Error: Your API key was rejected by the server (403 Forbidden). Double-check for typos or spaces.")
            return None
        else:
            st.error(f"API Error: Received status code {response.status_code}.")
            return None
    except Exception as e:
        st.error(f"Network connection failed: {e}")
        return None

df = load_football_data()

# 4. Display the Data safely
if df is not None:
    st.write("### Current Premier League Standings")
    st.dataframe(df, use_container_width=True)
    
    st.write("### Predictor Metric Summary")
    col1, col2, col3 = st.columns(3)
    
    # Structural row fetching using pandas .iloc
    top_team_name = df.iloc[0]['team.name']
    top_team_pts = df.iloc[0]['points']
    
    col1.metric("Top Team", str(top_team_name), f"{top_team_pts} pts")
    col2.metric("Total Teams Tracked", len(df))
    col3.metric("Avg Games Played", int(df['playedGames'].mean()))
