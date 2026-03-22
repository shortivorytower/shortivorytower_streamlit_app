import streamlit as st
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- 頁面設定 ---
st.set_page_config(page_title="Quant Finance Track Record", layout="wide")

# ==========================================
# 核心數學邏輯: Black-Scholes Call Formula
# ==========================================
def black_scholes_call(S0, K, T, r, sigma):
    """
    計算 Black-Scholes Call Option 價格
    """
    if T == 0:
        return max(0, S0 - K)
    
    # 計算 d1 和 d2
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # 計算 Call 價格
    call_price = (S0 * norm.cdf(d1)) - (K * np.exp(-r * T) * norm.cdf(d2))
    return call_price, d1, d2

# ==========================================
# UI 介面 - 標題與文章內容
# ==========================================
st.title("只係試下嘢：Black-Scholes ")
st.write("### ... whatever... testing only")
st.markdown("""
試吓用 Interactive 嘅方法留低啲紀錄。普通市民識嘅係『分散投資』，
但係數學話畀我哋聽『風險點樣定價』。

今日我哋嚟看最經典嘅 Black-Scholes Formula。它假設股票價格服從
***幾何布朗運動 (Geometric Brownian Motion)***。
""")

# 寫公式 (用 LaTeX)
st.latex(r"C(S_0, T) = S_0 N(d_1) - Ke^{-rT} N(d_2)")
st.latex(r"d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}")

st.markdown("""
<br>

## 互動式計算：你自己調校參數

在左側或上方調整參數，睇吓 Call Option 價格點樣變。

""", unsafe_allow_html=True)

# ==========================================
# UI 介面 - Sidebar 參數控制
# ==========================================
st.sidebar.header("模型輸入參數")
input_S0 = st.sidebar.slider("當前股價 (S0)", 50.0, 150.0, 100.0)
input_K = st.sidebar.slider("行使價 (K)", 50.0, 150.0, 105.0)
input_T = st.sidebar.slider("到期時間 (T, 年)", 0.01, 5.0, 1.0)
input_r = st.sidebar.slider("無風險利率 (r, %)", 0.0, 15.0, 5.0) / 100.0
input_sigma = st.sidebar.slider("波動率 (sigma, %)", 5.0, 100.0, 30.0) / 100.0

# --- 計算結果 ---
call_price, d1, d2 = black_scholes_call(input_S0, input_K, input_T, input_r, input_sigma)

# --- 顯示主要結果 ---
col1, col2, col3 = st.columns(3)
col1.metric("Call Option 價格", f"${call_price:.2f}")
col2.metric("d1", f"{d1:.4f}")
col3.metric("d2", f"{d2:.4f}")

# ==========================================
# 視覺化：Call Price 對 Volatility 的影響
# ==========================================
st.markdown("---")
st.markdown("### 深度分析：Vega (波動率敏感度)")
st.write("Black-Scholes 模型最正嘅地方係佢話你聽：『時間』同『波動』都係有價值的。")

# 模擬不同波動率
vol_range = np.linspace(0.05, 1.0, 50)
prices_vs_vol = [black_scholes_call(input_S0, input_K, input_T, input_r, v)[0] for v in vol_range]

fig = go.Figure()
fig.add_trace(go.Scatter(x=vol_range * 100, y=prices_vs_vol, mode='lines', name='Call Price'))
fig.update_layout(
    title=f"Call 價格 vs. 波動率 (當前 K={input_K}, T={input_T})",
    xaxis_title="波動率 (%)",
    yaxis_title="Option 價格 ($)"
)
st.plotly_chart(fig, use_container_width=True)


# ==========================================
# 高級功能：瀏覽統計 與 GitHub 留言
# ==========================================
st.markdown("---")
col_info1, col_info2 = st.columns([1, 2])

with col_info1:
    st.write("#### 讀者足跡")
    # 這裡加入 Google Analytics (GA) 的 HTML Snippet。
    # 請替換成你自己的 GA Tracking ID。
    ga_html = """
    <script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'YOUR-GA-ID');
    </script>
    """
    # 我們雖然看不到 GA 後台的 View Count，但你可以嵌入一個簡單的計數器 SVG (Moe-Counter)
    st.markdown("![Views](https://moe-counter.glitch.me/get/@your_github_username_quant_blog?theme=rule34)")

with col_info2:
    st.write("#### 公開討論 (GitHub Discussions)")
    st.write("如果有數學推導錯誤，或者有咩想傾，歡迎留言（需 GitHub 帳號）。")
    
    # ==========================================
    # Giscus 留言嵌入 (把下面的內容替換成你從 giscus.app 獲得的 HTML)
    # ==========================================
    giscus_html = """
    <script src="https://giscus.app/client.js"
            data-repo="your_github_username/quant-math-notes"
            data-repo-id="YOUR_REPO_ID"
            data-category="Announcements"
            data-category-id="YOUR_CATEGORY_ID"
            data-mapping="pathname"
            data-strict="0"
            data-reactions-enabled="1"
            data-emit-metadata="0"
            data-input-position="bottom"
            data-theme="light"
            data-lang="zh-TW"
            crossorigin="anonymous"
            async>
    </script>
    """
    # 使用 streamlit components 嵌入 Giscus
    components.html(giscus_html, height=600, scrolling=True)
