from sys import prefix

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.title("基本統計學常識")

#with open("load-mathjax.js", "r") as f:
#    js = f.read()
#    st.components.v1.html(f"<script>{js}</script>", height=0)

st.markdown(r"""
我諗左好耐究竟第一篇寫乜好，最後都揀咗一啲好basic統計學嘅嘢，因為我覺得呢啲真係fundamental。

關於統計學，我仲記得以前我個中學老師教我哋計下Mean、Standard Deviation (SD) 呢啲嘢，

- 例如：度下全班男仔身高幾多cm，跟住計下Mean；又計下SD咁。

咁跟住呢？？ 都係交完功課考試合格就算數，完全冇講過計嚟做乜。或者我個老師真係覺得度高磅重好實用、好有趣掛？

#### 用家見解

統計學真係一門好Q深奧嘅嘢嚟，不過high level 我都想講下少少用家嘅見解，我認為

- 統計學係用數學嚟Model一個Blackbox，而呢個Blackbox我地永遠都唔知裏面係點樣嘅。

    - 一般做法係搵啲Data Point整個Model出嚟，推測下關於個Blackbox嘅特點。

    - 至於推測有幾勁，咁就睇下個Model同Data Quality有幾好喇。
""")

st.markdown(r"""
#### 一般用法

其實喺Finance上面最Common嘅用法，就係用嚟Measure下啲股票每日嘅回報率Daily Return特性。

呢樣嘢Exactly就係上面講嘅Blackbox：我地可以估下嚟緊回報有幾多，有個大槪嘅Idea，但係究竟入面詳細每一樣嘢係點樣運作其實係冇可能知道哂。

作為Raw Data Point， 以下有兩隻股票嘅Daily Close Price ($$ P_t $$ : Price At Time $$ t $$)：

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
fig1.update_layout(title_text=r"Stock 1 and Stock 2 Daily Close Prices", showlegend=False, height=300)

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
fig2.update_layout(height=300, title_text=r"Stock 1 and Stock 2 Daily Returns", showlegend=False)

# Display the Combined Plot
st.plotly_chart(fig1, width="content")
#st.components.v1.html(fig1.to_html(include_mathjax='cdn'), height=300)

st.markdown(r"""

好多時喺Finance嘅世界係比較少直接用Price去計啲Statistics，主要原因係做唔到股票之間嘅比較。
例如一隻五蚊升咗五毫，另一隻百幾蚊升咗十蚊，個Price唔喺同一個scale係冇得比較。但係個Return (升咗幾多percent)就可以比較喇。

首先我哋要由Daily Close Price 轉做 Simple Daily Return (又稱Arithmetic Return)：

(Sidetrack少少，仲有Geometric Return同Log Return…)

""")

st.latex(r"""
\begin{align*}
\textsf{Simple Return } R_t &= \frac{P_t-P_{t-1}}{P_{t-1}} \\
                            &= \frac{P_t}{P_{t-1}}-1
\end{align*}
""")


st.markdown(r"""



然後將啲 Data Points ($$ R_t $$) Plot 做 Histogram 睇下個樣大槪係點。

""")


st.plotly_chart(fig2, width="content")

with st.expander("Data Points"):
    display_df = stock1.merge(stock2, on="trade_date", how="inner", suffixes=["_stock1", "_stock2"])
    st.dataframe(display_df, width="stretch")

st.markdown(r"""

通常都會計一下四個Moments (唔知中文係乜)：

- Mean 

- Variance

- Skewness

- Kurtosis


""")