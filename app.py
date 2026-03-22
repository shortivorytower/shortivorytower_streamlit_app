import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Blogs", layout="wide")

# ==========================================
# Home Page
# ==========================================
st.title("Short Ivory Tower")
st.markdown("*A quant finance blog with interactive explorations.*")

st.markdown("---")

# ==========================================
# About Section
# ==========================================
st.markdown("## About")
st.markdown("""
This is a personal blog where I document my learning journey in quantitative finance.

The posts here are interactive - you can play with the parameters and see the results in real-time.
Built with [Streamlit](https://streamlit.io/).

*Note: Content here is draft/experimental. Don't take it as financial advice.*
""")

st.markdown("---")

# ==========================================
# Posts Index
# ==========================================
st.markdown("## Posts")

st.page_link(
    "pages/2026-02-01_Annualized_Return_Volatility.py",
    label="2026-02-01: How to Estimate Annualized Return and Volatility",
    icon="📊",
)

st.page_link(
    "pages/2026-03-22_Black_Scholes.py",
    label="2026-03-22: Black-Scholes Model",
    icon="📈",
)
