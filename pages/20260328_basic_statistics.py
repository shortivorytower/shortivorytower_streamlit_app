import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import johnsonsu, describe
from scipy.optimize import minimize
import plotly.graph_objects as go
import plotly.express as px
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
stock1_daily_return = stock1["daily_return"][1:]
stock2_daily_return = stock2["daily_return"][1:]
fig2.add_trace(
    go.Histogram(x=stock1_daily_return, nbinsx=50, name="Stock 1 Returns"),
    row=1,
    col=1,
)
fig2.add_trace(
    go.Histogram(x=stock2_daily_return, nbinsx=50, name="Stock 2 Returns"),
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

st.markdown(r"""

每隻股票Raw Data有252個Day Close Price $$ P_t $$，所以一共有251個Return $$ R_t $$，$$ n = 251 $$ 

通常啲Statistics嘅Software都會有個類似Describe嘅Function，一Call佢就會出哂呢四粒數。

""")

#stock1_descriptive_statistics = describe(stock1_daily_return)
st.markdown(f"stock 1 stat = {describe(stock1_daily_return)}")
st.markdown(f"stock 2 stat = {describe(stock2_daily_return)}")


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

呢度有個簡單Simulation可以攞個關於Moments 嘅 Feeling

""")



screen_width = streamlit_js_eval(js_expressions="window.innerWidth", key="screen_width")
use_desktop = screen_width is not None and screen_width > 768
with st.expander("Moments Simulation", expanded=True):
    if use_desktop:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            target_mean = st.slider("Mean", -0.50, 0.5, 0.02)
        with col2:
            target_variance = st.slider("Variance", 0.01, 0.09, 0.01)
        with col3:
            target_skewness = st.slider("Skewness", -2.5, 2.5, 0.1)
        with col4:
            target_kurtosis = st.slider("Kurtosis", 0.01, 5.0, 0.01)
    else:  # Mobile or width not yet detected - vertical stack
        st.markdown(r"###### Parameters")
        target_mean = st.slider("Mean", -0.50, 0.5, 0.02)
        target_variance = st.slider("Variance", 0.01, 0.09, 0.01)
        target_skewness = st.slider("Skewness", -2.5, 2.5, 0.1)
        target_kurtosis = st.slider("Kurtosis", 0.01, 5.0, 0.01)

    # hardcoded parameters
    samples_count = 20000
    seed = 2351397
    # estimate the parameters
    param_a, param_b, param_loc, param_scale = find_johnson_su_params_by_moments(target_mean, target_variance, target_skewness, target_kurtosis)
    np.random.seed(seed)
    sim_moments_data = johnsonsu.rvs(a=param_a, b=param_b, loc=param_loc, scale=param_scale, size=samples_count)
    res = describe(sim_moments_data)
    sample_mean = res.mean
    sample_variance = res.variance
    sample_skewness = res.skewness
    sample_kurtosis = res.kurtosis
    theo_mean, theo_variance, theo_skewness, theo_kurtosis = johnsonsu.stats(param_a, param_b, loc=param_loc, scale=param_scale, moments='mvsk')
    if use_desktop:
        with col1:
            st.latex(f"\\textsf{{Sample Mean }} \\bar{{R}} = {sample_mean:.3f}")
        with col2:
            st.latex(f"\\textsf{{Sample Variance }} s = {sample_variance:.3f}")
        with col3:
            st.latex(f"\\textsf{{Sample Skewness }} G_1 = {sample_skewness:.3f}")
        with col4:
            st.latex(f"\\textsf{{Sample Kurtosis }} G_2 = {sample_kurtosis:.3f}")
    else:
        st.latex(f"\\textsf{{Sample Mean }} \\bar{{R}} = {sample_mean:.3f}")
        st.latex(f"\\textsf{{Sample Variance }} s = {sample_variance:.3f}")
        st.latex(f"\\textsf{{Sample Skewness }} G_1 = {sample_skewness:.3f}")
        st.latex(f"\\textsf{{Sample Kurtosis }} G_2 = {sample_kurtosis:.3f}")

    sim_moments_df = pd.DataFrame({'Value': sim_moments_data})

    # --- Plotly Visualization ---
    sim_moments_fig = px.histogram(
        sim_moments_df,
        x='Value',
        nbins=200,
        title=f'Generated {len(sim_moments_data)} Samples',
        template='plotly_dark',  # Optimized for high-res dark mode viewing
        labels={'Value': 'Sample Value'},
        opacity=0.75
    )

    # Highlight the Mean
    sim_moments_fig.add_vline(
        x=sample_mean,
        line_dash='dash',
        line_color='red',
        annotation_text=f'Sample Mean: {sample_mean:.2f}',
        annotation_position='top right'
    )

    # Update layout for clarity
    sim_moments_fig.update_layout(
        bargap=0.1,
        xaxis_title=f'Sample Values',
        yaxis_title='Frequency',
        showlegend=False,
        xaxis=dict(range=[-4, 4]),
        yaxis=dict(range=[0, 2000]),
    )
    st.plotly_chart(sim_moments_fig, width="content")
