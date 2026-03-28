import streamlit as st

st.set_page_config(page_title="Blogs", layout="wide")

# --- Custom Navigation ---
pages = [
    st.Page("pages/0_home.py", title="Home", icon="🏠", default=True),
    st.Page("pages/20260328_basic_statistics.py", title="2026-03-28: 基本統計學常識", icon="📊", default=False)
    #st.Page("pages/20260201_annualized_return_volatility.py", title="2026-02-01: Annualized Return & Volatility", icon="📊"),
]

nav = st.navigation(pages)
nav.run()
