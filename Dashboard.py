import streamlit as st
from dotenv import load_dotenv

load_dotenv()

pages = {
    "Home": [
        st.Page("pages/home/home.py", title="API Playground", icon="🏠"),
    ],
    "Fogo Cruzado API": [
        st.Page("pages/fogo_cruzado/fogo_cruzado.py", title="Fogo Cruzado", icon="🔫"),
    ],
    "Yahoo Finance API": [
        st.Page("pages/yahoo_finance/yahoo_finance.py", title="Yahoo Finance", icon="💸")
    ]
}

pg = st.navigation(pages)
pg.run()

# streamlit run Dashboard.py