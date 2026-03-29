import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import johnsonsu, describe
from scipy.optimize import minimize
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_js_eval import streamlit_js_eval


# support functions

def find_johnson_su_params_by_moments(mean, variance, skew, kurt):
    """
    Finds Johnson SU parameters (a, b, loc, scale) that match the four input moments.
    """

    def objective(params):
        a_guess, b_guess = params
        if b_guess <= 0:
            return 1e10

        # Calculate theoretical skew and excess kurtosis for these shapes
        s, k = johnsonsu.stats(a_guess, b_guess, moments="sk")

        # Minimize the squared error of skew and kurtosis
        return (s - skew) ** 2 + (k - kurt) ** 2

    # Initial guess for a (skew) and b (kurtosis)
    # a=0, b=2 is roughly a normal-ish distribution
    optim_result = minimize(objective, x0=[0.0, 2.0], method="Nelder-Mead")

    if not optim_result.success:
        raise ValueError("Could not find parameters for the given moments.")

    result_a, result_b = optim_result.x

    # Now solve for loc and scale using the mean and variance
    # johnsonsu.stats(a, b) returns mean and var for loc=0, scale=1
    m0, v0 = johnsonsu.stats(result_a, result_b, moments="mv")

    # Scale transformation: Var(X) = scale^2 * Var(Standardized)
    result_scale = np.sqrt(variance / v0)

    # Location transformation: E[X] = loc + scale * E[Standardized]
    result_loc = mean - result_scale * m0
    return result_a, result_b, result_loc, result_scale



# page start

st.title("基本統計學常識")

# with open("load-mathjax.js", "r") as f:
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
# st.components.v1.html(fig1.to_html(include_mathjax='cdn'), height=300)

st.markdown(r"""

好多時喺Finance嘅世界係比較少直接用Price去計啲Statistics，主要原因係做唔到股票之間嘅比較。
例如一隻五蚊升咗五毫，另一隻百幾蚊升咗十蚊，個Price唔喺同一個scale係冇得比較。但係個Return $$ R_t $$ (升咗幾多percent)就可以比較喇。

<div style="border: 2px solid #ddd; border-radius: 5px; padding: 15px; background-color: #f9f9f9;">

**同埋仲有一樣非常重要嘅假設：下一日嘅 Return $$ R_{t+1} $$ 同今日嘅 Return $$ R_t $$ 係i.i.d.(Independent and Identically Distributed)，唔係就要做埋Time Series Analysis。**
- 意思係今日嘅升跌其實唔影響聽日嘅升跌，唔可以即係用今日嘅Return去估計聽日嘅Return
- 個Blackbox 入面（睇唔到）嘅特性係一直都唔會改變 

呢樣假設喺股票數據分析入面係一個經常用嘅簡化。 雖然有人會覺得好似唔Make Sense，特別係有時個市短期內某啲股票可能會有 Momentum（不停爆升/跌）或者 Mean Reversion（升跌得太多會回返落嚟同靜返）。
但喺大部分情況下，為咗處理大量嘅股票資料，假設 i.i.d. 係一個合理嘅平衡。

</div>

首先我哋要由Daily Close Price 轉做 Simple Daily Return (又稱Arithmetic Return)：

(Sidetrack：仲有其他相關嘅嘢例如Geometric Return同Log Return…)

""", unsafe_allow_html=True)

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

#### 如果用數字嚟描述一下啲Data，可以計以下四個Moments：

##### Mean (1st Moment)
    - 平均Daily Return有幾多
##### Variance (2nd Moment)
    - 平均Daily Return同實際Data Point差幾遠，可以理解成「一般風險」。
##### Skewness (3rd Moment)
    - 啲Daily Return 會唔會成日都係嬴粒糖輸間廠咁(Negative Skew)？
    - 定係好似買六合彩咁九成九都嬴唔到，不過買好多好多次可能會嬴舖勁嘅(Positive Skew)？
##### Kurtosis (4th Moment)
    - 啲Data係唔係極端分散，可以理解成為「極端事件」多唔多發生。
""")

screen_width = streamlit_js_eval(js_expressions="window.innerWidth", key="screen_width")


# with st.expander("Moments Simulation", expanded=True):
#     if screen_width and screen_width > 768:  # Desktop - use 3 columns
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             sim_S0 = st.number_input("Initial Price (S0)", value=100.0, min_value=1.0)
#             sim_mu = st.slider("Drift (mu, annual %)", -50.0, 50.0, 10.0) / 100.0
#         with col2:
#             sim_sigma = (
#                     st.slider("Volatility (sigma, annual %)", 5.0, 100.0, 25.0) / 100.0
#             )
#             sim_days = st.slider("Trading Days", 30, 504, 252)
#         with col3:
#             sim_seed = st.number_input("Random Seed", value=42, min_value=0)
#     else:  # Mobile or width not yet detected - vertical stack
#         sim_S0 = st.number_input("Initial Price (S0)", value=100.0, min_value=1.0)
#         sim_mu = st.slider("Drift (mu, annual %)", -50.0, 50.0, 10.0) / 100.0
#         sim_sigma = st.slider("Volatility (sigma, annual %)", 5.0, 100.0, 25.0) / 100.0
#         sim_days = st.slider("Trading Days", 30, 504, 252)
#         sim_seed = st.number_input("Random Seed", value=42, min_value=0)



st.markdown(r"""

每隻股票Raw Data有252個Day Close Price $$ P_t $$，所以一共有251個Return $$ R_t $$，$$ n = 251 $$ 

""")

st.latex(r"""
\begin{align*}
\textsf{Sample Mean } \bar{R} &= \frac{\sum_{i=1}^{n} R_i}{n} \\ 

\textsf{Sample Variance } s^2 &= \frac{\sum_{i=1}^{n} (R_i - \bar{R})^2}{n-1} \\

\textsf{Sample Skewness } G_1 &= \frac{n}{(n-1)(n-2)} \sum_{i=1}^{n} \left( \frac{R_i - \bar{R}}{s} \right)^3 \\

\textsf{Sample Kurtosis } G_2 &= \frac{n(n+1)}{(n-1)(n-2)(n-3)} \sum_{i=1}^{n} \left( \frac{R_i - \bar{R}}{s} \right)^4 - \frac{3(n-1)^2}{(n-2)(n-3)}

\end{align*}
""")

st.markdown(r"""

…唉……啲stat嘅formula 真係樣衰到一個點……… 

""")
