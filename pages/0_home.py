import streamlit as st

# ==========================================
# Home Page
# ==========================================
st.title("Short Ivory Tower")
st.markdown("**數學用家 -- 活在象牙塔入面，但係佢個塔都幾矮。**")

st.markdown("---")

# ==========================================
# About Section
# ==========================================
st.markdown("## About")
st.markdown("""

我係一個好普通嘅香港人。屋邨長大，讀嘅都係普通屋邨學校。我唔係數學家，係一個數學用家。

其實而家寫乜都勁唔過 AI，而且如果想睇真人 content 都即食睇片啦，咁仲寫嚟做乜？

呢個 blog 有兩個目的：

1. 純粹係我自己嘅紀錄，寫低呢幾十年嚟喺技術上嘅 know-how。

1. 我希望可以畀一啲同我一樣、數學 OK 但出身普通嘅細路有啲希望——你嘅出路唔一定要做醫生或者律師，或者跟風去搞 AI。你一樣可以將數學應用喺香港最重要嘅另一個領域：金融。

我專登用廣東話嚟寫，因為我根本唔care外國人或者大陸人睇唔睇得明。香港人梗係用廣東話啦！

""")

st.markdown("---")

# ==========================================
# Posts Index
# ==========================================
st.markdown("## Posts")

st.page_link(
    "pages/20260201_annualized_return_volatility.py",
    label="2026-02-01: How to Estimate Annualized Return and Volatility",
    icon="📊",
)

st.page_link(
    "pages/20260322_black_scholes.py",
    label="2026-03-22: Black-Scholes Model",
    icon="📈",
)
