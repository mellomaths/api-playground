import streamlit as st

from apps.yahoo_finance.yahoo_finance_api import YahooFinanceApi


st.set_page_config(page_title="Yahoo Finance API", page_icon="💸", layout="centered")

st.write(f"# Yahoo Finance API")

yahoo_finance = YahooFinanceApi()

selected_company = st.selectbox("Choose a company symbol", yahoo_finance.available_companies)
selected_symbol = yahoo_finance.companies_symbol_mapping[selected_company]

stock_price = yahoo_finance.get_stock_price(selected_symbol)
meta_stock_price = stock_price.get("meta")

col1, col2, col3 = st.columns(3)
with col1:
    regular_market_price = meta_stock_price.get("regularMarketPrice")
    st.metric(label="Market Price", value=f"$ {regular_market_price}")
with col2:
    highest_price_today = meta_stock_price.get("regularMarketDayHigh")
    st.metric(label="Today's Highest Price", value=f"$ {highest_price_today}")
with col3:
    lowest_price_today = meta_stock_price.get("regularMarketDayLow")
    st.metric(label="Today's Lowest Price", value=f"$ {lowest_price_today}")


st.write(stock_price)
