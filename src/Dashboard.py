import streamlit as st
from dotenv import load_dotenv

load_dotenv()

pages = {
    "Home": [
        st.Page("apps/home/page.py", title="API Playground", icon="🏠", url_path="/"),
    ],
    "Fogo Cruzado API": [
        st.Page("apps/fogo_cruzado/page.py", title="Fogo Cruzado", icon="🔫", url_path="/fogo-cruzado"),
    ],
    "Yahoo Finance API": [
        st.Page("apps/yahoo_finance/page.py", title="Yahoo Finance", icon="💸", url_path='/yahoo-finance')
    ]
}

pg = st.navigation(pages)
pg.run()

# streamlit run Dashboard.py