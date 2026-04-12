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

st.markdown("**一個數學用家 -- 活在象牙塔入面，但係個塔都幾矮…**")

st.markdown("---")

# ==========================================
# About Section
# ==========================================
st.markdown("## About")
st.markdown("""

普通香港人，屋邨長大，讀嘅都係屋邨學校。我唔係數學家，只係一個數學用家。

其實而家已經唔興寫Blog，寫乜都勁唔過 AI，何況如果想睇真人 content 所有人都係睇片，咁仲寫嚟做乜？

關於呢個 blog 有幾樣嘢：

1. 主要係我自己嘅紀錄，寫低一路以嚟用家技術上嘅 know-how，尤其係Quantitative Finance或者電腦嘅主題，又或者一啲未諗到有乜用但係好有趣嘅嘢。

1. 寫成類似用家Tutorial 再加啲我自己嘅睇法，希望可以啟發到一啲理科成績好嘅中學生，原來做醫生律師或者跟風攪 AI 唔係唯一出路。

1. 我專登用廣東話寫，因為咁先至準確表達到我想講嘅嘢。呢個係一個香港人嘅Identity，喺綱上留低一啲有意義嘅Digital Footprint。


""")

st.markdown("---")

# ==========================================
# Posts Index
# ==========================================
st.markdown("## Posts")

st.page_link("pages/20260328_basic_statistics.py",label="2026-03-28: 基本統計學常識",icon="📊")
