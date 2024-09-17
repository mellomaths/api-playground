import os
import math
import streamlit as st
import pandas as pd
import time

from apps.fogo_cruzado.fogo_cruzado_api import FogoCruzadoApi, Credentials


st.set_page_config(page_title="Fogo Cruzado", page_icon="🔫")

st.write(f"# Fogo Cruzado")

st.write(
"""
Ideas for pages: 
1. Create page with parametrized query (year and state). Plot data
2. Create one page with all data from the last 5 years and compare the years.

Ideas for charts:
1. How many occurrences per month?
2. Most violent places in the state.
3. Comparison by year.
    a. which year had the most victims?
    b. the most occurrences?
4. Which places in the states have more police/security agents presence in occurrence?
5. Most common occurrences causes.
""")
    

def initial_date(year: int) -> str:
        return f'{year}-01-01'
    
def final_date(year: int) -> str:
    return f'{year+1}-01-01'

# st.write(f"## Occurrences")

credentials = {
    "email": os.getenv("FOGO_CRUZADO_API_EMAIL"),
    "password": os.getenv("FOGO_CRUZADO_API_PASSWORD"),
}
fogo = FogoCruzadoApi(credentials=Credentials(email=credentials["email"], password=credentials["password"]))

@st.cache_data
def get_states():
    mapping = {}
    states = fogo.get_states()
    for state in states:
        name = state["name"]
        state_id = state["id"]
        mapping[name] = state_id
    
    return mapping

states = get_states()
st.write("## Parameters")
col1, col2 = st.columns(2)
with col1:
    selected_year = st.selectbox("Choose a year", [2020, 2021, 2022, 2023])
with col2:
    selected_state = st.selectbox("Choose a state", states.keys())
    selected_state_id = states[selected_state]


@st.cache_data
def get_occurrences_data(year: int, state_id: str): 
    progress_bar = st.progress(0)
    status_text = st.empty()  
    
    page = 1
    occurrences = []
    has_next_page = True
    progress = 0
    while has_next_page:
        data, has_next_page, page_count = fogo.get_occurrences(state_id, initial_date(year), final_date(year), page)
        occurrences += data
        page += 1
        progress += math.ceil(100 / page_count)
        progress = progress if progress < 100 else 100
        progress_bar.progress(progress)
        status_text.text(f"{progress}% Complete")
        time.sleep(0.05)
    
    return occurrences

occurrences = get_occurrences_data(selected_year, selected_state_id)
    
data = []
for occur in occurrences:    
    try:
        locality = occur.get("locality", {})
        if locality: 
            locality = locality.get("name", None)
        
        neighborhood = occur.get("neighborhood", {})
        if neighborhood:
            neighborhood = neighborhood.get("name", None)
            
        sub_neighborhood = occur.get("subNeighborhood", {})
        if sub_neighborhood:
            sub_neighborhood = sub_neighborhood.get("name", None)
            
        context_info = occur.get("contextInfo", {})
        if context_info:
            reason = context_info.get("mainReason", {})
            if reason:
                reason = reason.get("name", None)
            
            massacre = context_info.get("massacre", False)
    
        data.append({
            'id': occur.get("id", None),
            "city": occur.get("city", {}).get("name", None),
            "locality": locality,
            "neighborhood": neighborhood,
            "sub_neighborhood": sub_neighborhood,
            "latitude": occur.get("latitude", None),
            "longitude": occur.get("longitude", None),
            "date": occur.get("date", None),
            "reason": reason,
            "massacre": massacre,
            "police_presence": occur.get("policeAction", None),
            "security_agent_presence": occur.get("agentPresence"),
            "victims": occur.get("victims", [])
        })
    except TypeError as e:
        print("Occurrence empty")
        
df = pd.DataFrame(data, columns=[
    "id", 
    "city", 
    "locality", 
    "neighborhood", 
    "sub_neighborhood", 
    "latitude", "longitude", 
    "date", "reason", 
    "massacre", "police_presence", "security_agent_presence", 
    "victims"])

st.write(f"### {selected_year} Database for {selected_state}", df)