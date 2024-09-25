import os
import math
import altair as alt
import streamlit as st
import pandas as pd
import time

from apps.fogo_cruzado.fogo_cruzado_api import FogoCruzadoApi, Credentials
from pages.fogo_cruzado.data import normalize_occurrences_data, build_occurrences_df


st.set_page_config(page_title="Fogo Cruzado", page_icon="🔫", layout="centered")

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
        if len(data) == 0:
            return occurrences
        
        print(len(data), has_next_page, page_count)
        occurrences += data
        page += 1
        progress += math.ceil(100 / page_count)
        progress = progress if progress < 100 else 100
        progress_bar.progress(progress)
        status_text.text(f"{progress}% Complete")
        time.sleep(0.05)
    
    return occurrences

occurrences = get_occurrences_data(selected_year, selected_state_id)
occurrences_data = normalize_occurrences_data(occurrences)
occurrences_df = build_occurrences_df(occurrences_data)

st.write(f"### {selected_year} Database for {selected_state}", occurrences_df)

st.write("### How many occurrences per month?")

df = occurrences_df.groupby(['month_number', 'month_name_abbr']).size().to_frame('occurrences')
print("==========START==========")
df = df.reset_index()
df.sort_values(by='month_number', inplace=True)
df = df.reset_index(drop=True)

st.altair_chart(alt.Chart(df).mark_bar().encode(
    x=alt.X('month_name_abbr', sort=None, title="Months", axis=alt.Axis(labelAngle=0)),
    y=alt.Y('occurrences', title="Occurrences"),
), use_container_width=True)
