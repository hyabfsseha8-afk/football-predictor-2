import streamlit as st
import pandas as pd
import requests

# 1. Custom Styling (Fixed the previous type error!)
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
API_KEY = "83d3eaf8bc79498f91098bf16828d7ea
"
API_URL = "https://football-data.org"
HEADERS = {"X-Auth-Token": API_KEY}

# 3. Fetch live data safely with Streamlit caching
@st.cache_data(ttl=3600)  # Caches the data for 1 hour to stay under the free tier limit
def load_football_data():
    if API_KEY == "83d3eaf8bc79498f91098bf16828d7ea
":
        st.warning("⚠️ Using sample data. Please replace 'YOUR_FREE_API_KEY_HERE' with your real API token.")
        # Fixed Syntax: Added mock data elements inside the lists
        mock_data = {
            'position':,
            'team.name': ['Arsenal', 'Manchester City', 'Liverpool'],
            'playedGames':,
            'won':,
            'draw':,
            'lost':,
            'goalsFor':,
            'goalsAgainst':,
            'goalDifference':,
            'points': [58, 56, 53]
        }
        return pd.DataFrame(mock_data)

    try:
        response = requests.get(API_URL, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            # Flattens the nested table response into a clean table structure
            standings_table = data['standings'][0]['table']
            df = pd.json_normalize(standings_table)
            
            # Select and clean the essential columns for your predictor model
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
            st.error(f"Error fetching data from API (Status Code: {response.status_code})")
            return None
    except Exception as e:
        st.error(f"Network connection failed: {e}")
        return None

# Execute the function to get the data frame
df = load_football_data()

# 4. Display the Data in your App
if df is not None:
    st.write("### Current Premier League Standings")
    st.dataframe(df, use_container_width=True)
    
    # Example metric layout for your predictor UI
    st.write("### Predictor Metric Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Top Team", df.iloc[0]['team.name'], f"{df.iloc[0]['points']} pts")
    col2.metric("Total Teams Tracked", len(df))
    col3.metric("Avg Games Played", int(df['playedGames'].mean()))
