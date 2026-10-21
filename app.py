import streamlit as st
import pandas as pd
import requests

# 1. Custom Styling 
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f8;
    }
    h1 {
        color: #1e3d59;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Football Predictor Data Hub")

# 2. API Setup 
# Replace the text below with your actual API key from football-data.org
API_KEY = st.secrets["83d3eaf8bc79498f91098bf16828d7ea"]
API_URL = "https://football-data.org"
HEADERS = {"X-Auth-Token": API_KEY}

# 3. Fetch live data safely with Streamlit caching
@st.cache_data(ttl=3600)
def load_football_data():
    if API_KEY == "83d3eaf8bc79498f91098bf16828d7ea" or API_KEY == "":
        st.error("Please insert your real football-data.org API token on line 20.")
        return None

    try:
        response = requests.get(API_URL, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            # Extracts the list of team stats from the API response
            standings_table = data['standings'][0]['table']
            df = pd.json_normalize(standings_table)
            
            # Filter down to the essential numeric columns
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
        else:
            st.error(f"API Error: Received status code {response.status_code}. Check your API Key limits.")
            return None
    except Exception as e:
        st.error(f"Network connection failed: {e}")
        return None

# Run the function
df = load_football_data()

# 4. Display the Data safely
if df is not None:
    st.write("### Current Premier League Standings")
    st.dataframe(df, use_container_width=True)
    
    st.write("### Predictor Metric Summary")
    col1, col2, col3 = st.columns(3)
    
    # Corrected panda row indexing using .iloc for structural safety
    top_team_name = df.iloc[0]['team.name']
    top_team_pts = df.iloc[0]['points']
    
    col1.metric("Top Team", str(top_team_name), f"{top_team_pts} pts")
    col2.metric("Total Teams Tracked", len(df))
    col3.metric("Avg Games Played", int(df['playedGames'].mean()))
