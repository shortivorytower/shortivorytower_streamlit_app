from sys import prefix

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.title("基本統計學常識")
with open("load-mathjax.js", "r") as f:
    js = f.read()
    st.components.v1.html(f"<script>{js}</script>", height=0)

st.markdown(r"""
我諗左好耐究竟第一篇寫乜好，最後都揀咗一啲好basic嘅統計學嘢，因為我覺得呢啲真係fundamental。

關於統計學，我仲記得以前中學啲老師教我哋計Mean、Standard Deviation (SD) 呢啲嘢，

- 例如：度下全班男仔身高幾多cm，跟住計下Mean；又計下SD

咁跟住呢？？ 都係交完功課考試合格就算數，冇講過有乜用同埋點解要計呢啲嘢。又或者可能大家都覺得度高磅重好實用、大家都好有興趣掛？

#### 用家見解

統計學真係一門好Q深嘅嘢嚟，不過high level 我都想講下少少用家嘅見解，我認為

- 統計學係用數學嚟描述一啲Blackbox，一啲我地永遠都唔知絕對真實樣子係點嘅嘢。

- 一般做法係搵啲Data Point整個Model出嚟，推測下關於個Blackbox嘅特點。

- 至於推測有幾勁，就睇下個Model同Data Quality有幾好喇。
""")

st.markdown(r"""
#### 一般用法

其實喺Finance上面最Common嘅用法，就係用嚟Measure下啲股票每日嘅回報率Daily Return特性。

以下有兩隻股票嘅Daily Close Price ($$ P_t $$ : Price At Time $$ t $$)，呢啲係Raw Data Point。

""")

# Load Data
stock1 = pd.read_csv("assets/pages/20260308_basic_statistics/stock1_px_close.csv")
stock2 = pd.read_csv("assets/pages/20260308_basic_statistics/stock2_px_close.csv")

# Process Data
stock1["trade_date"] = pd.to_datetime(stock1["trade_date"])
stock2["trade_date"] = pd.to_datetime(stock2["trade_date"])
stock1["daily_return"] = stock1["px_close"].pct_change()
stock2["daily_return"] = stock2["px_close"].pct_change()

# Create Combined Subplots
fig1 = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=(
        "Stock 1 Close Price",
        "Stock 2 Close Price",
    ),
)

# Add Closing Price Line Charts
fig1.add_trace(
    go.Scatter(x=stock1["trade_date"], y=stock1["px_close"], name="Stock 1 Price"),
    row=1,
    col=1,
)
fig1.add_trace(
    go.Scatter(x=stock2["trade_date"], y=stock2["px_close"], name="Stock 2 Price"),
    row=1,
    col=2,
)

# Update Layout for Better Appearance
fig1.update_layout(height=400, title_text=r"$\textsf{Stock 1 and Stock 2 Daily Close Prices } P_t$", showlegend=False)

fig2 = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=(
        "Stock 1 Daily Returns Histogram",
        "Stock 2 Daily Returns Histogram",
    ),
)

# Add Daily Returns Histograms
fig2.add_trace(
    go.Histogram(x=stock1["daily_return"], nbinsx=50, name="Stock 1 Returns"),
    row=1,
    col=1,
)
fig2.add_trace(
    go.Histogram(x=stock2["daily_return"], nbinsx=50, name="Stock 2 Returns"),
    row=1,
    col=2,
)
fig2.update_layout(height=400, title_text=r"$\textsf{Stock 1 and Stock 2 Daily Returns } R_t$", showlegend=False)

# Display the Combined Plot
st.plotly_chart(fig1, width="content", config={'includeMathJax': True})

st.markdown(r"""

好多時喺Finance嘅世界係比較少直接用Price去計啲Statistics，主要原因係因為下一個價位$$ P_{t+1} $$ 係heavily dependent on 而家係價位 $$ P_t $$

例如今日收市係50蚊，咁聽日隻嘢個收市幾乎冇可能係5蚊或500蚊，多數都係四十幾至五十幾之間。要用統計去handle個Price就要用Time Series Analysis，不過唔好扯到太遠喇。 

首先我哋要由Daily Close Price 轉做 Daily Return，而Return又有分Simple Return(又稱Arithmetic Return)同Log Return：

""")

st.latex(r"""
\textsf{Simple Return } R_t = \frac{P_t-P_{t-1}}{P_{t-1}} = \frac{P_t}{P_{t-1}}-1
""")

st.latex(r"""
\textsf{Log Return } r_t = \ln{\frac{P_t}{P_{t-1}}}
""")

st.markdown(r"""

都係用住Simple Return $$ R_t $$先：

""")


st.plotly_chart(fig2, width="content", config={'includeMathJax': True})

with st.expander("Raw Data"):
    display_df = stock1.merge(stock2, on="trade_date", how="inner", suffixes=["_stock1", "_stock2"])
    st.dataframe(display_df, width='stretch')