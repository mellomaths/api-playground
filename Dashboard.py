import streamlit as st
from dotenv import load_dotenv

load_dotenv()

pages = {
    "Fogo Cruzado API": [
        st.Page("pages/fogo_cruzado/fogo_cruzado.py", title="Fogo Cruzado API", icon="🔫"),
    ],
}

pg = st.navigation(pages)
pg.run()

# streamlit run dashboard.py