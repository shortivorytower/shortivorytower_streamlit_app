import base64
import streamlit as st

# ==========================================
# Home Page
# ==========================================

# Encode profile image as base64 for inline HTML
with open("assets/img/profile.png", "rb") as f:
    profile_b64 = base64.b64encode(f.read()).decode()

st.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <h1 style="margin: 0;">Short Ivory Tower</h1>
        <img src="data:image/png;base64,{profile_b64}"
             style="width: 50px; height: 50px; border-radius: 50%; margin-left: 12px; object-fit: cover;">
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("**一個數學用家 -- 活在象牙塔入面，但係個塔都幾矮。**")

st.markdown("---")

# ==========================================
# About Section
# ==========================================
st.markdown("## About")
st.markdown("""

普通香港人，屋邨長大，讀嘅都係屋邨學校。我唔係數學家，係一個數學用家。

其實而家寫乜都勁唔過 AI，而且如果想睇真人 content 都即食睇片啦，咁仲寫嚟做乜？

呢個 blog 有兩個目的：

1. 純粹係我自己嘅紀錄，寫低一路以嚟技術上嘅 know-how。

1. 畀少少希望一啲同我以前一樣、數學OK 但普通出身嘅學生 —— 你嘅出路唔一定只係做醫生或律師，或者跟住個hype去搞 AI。你apply數學喺金融上面，都可能搵到食。

香港人梗係用廣東話啦，我係專登用廣東話寫嘅！其他人種睇唔睇得明我完全唔care。

""")

st.markdown("---")

# ==========================================
# Posts Index
# ==========================================
st.markdown("## Posts")

st.page_link(
    "pages/20260201_annualized_return_volatility.py",
    label="2026-02-01: (求其試下嘢) How to Estimate Annualized Return and Volatility",
    icon="📊",
)
