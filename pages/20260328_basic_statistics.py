import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import johnsonsu, kurtosis, skew, tvar, tmean
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
spx = pd.read_csv("assets/pages/20260308_basic_statistics/spx_close.csv")
ccmp = pd.read_csv("assets/pages/20260308_basic_statistics/ccmp_close.csv")

# Process Data
stock1["trade_date"] = pd.to_datetime(stock1["trade_date"])
stock2["trade_date"] = pd.to_datetime(stock2["trade_date"])
spx["trade_date"] = pd.to_datetime(spx["trade_date"])
ccmp["trade_date"] = pd.to_datetime(ccmp["trade_date"])

stock1["daily_return"] = stock1["px_close"].pct_change()
stock2["daily_return"] = stock2["px_close"].pct_change()
spx["daily_return"] = spx["px_close"].pct_change()
ccmp["daily_return"] = ccmp["px_close"].pct_change()

# Create Combined Subplots
fig1 = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "Stock 1 Close Price",
        "Stock 2 Close Price",
        "S&P 500 Close",
        "NASDAQ Composite Close"
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
fig1.add_trace(
    go.Scatter(x=spx["trade_date"], y=spx["px_close"], name="S&P 500 Close"),
    row=2,
    col=1,
)
fig1.add_trace(
    go.Scatter(x=ccmp["trade_date"], y=ccmp["px_close"], name="NASDAQ Composite Close"),
    row=2,
    col=2,
)

# Update Layout for Better Appearance
fig1.update_layout(title_text=r"Daily Close Prices", showlegend=False, height=500)

fig2 = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "Stock 1 Daily Returns Histogram",
        "Stock 2 Daily Returns Histogram",
        "S&P 500 Daily Returns Histogram",
        "NASDAQ Composite Daily Returns Histogram",
    ),
)

# Add Daily Returns Histograms
stock1_daily_return = stock1["daily_return"][1:]
stock2_daily_return = stock2["daily_return"][1:]
spx_daily_return = spx["daily_return"][1:]
ccmp_daily_return = ccmp["daily_return"][1:]
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
fig2.add_trace(
    go.Histogram(x=spx_daily_return, nbinsx=50, name="S&P 500 Returns"),
    row=2,
    col=1,
)
fig2.add_trace(
    go.Histogram(x=ccmp_daily_return, nbinsx=50, name="NASDAQ Composite Returns"),
    row=2,
    col=2,
)

fig2.update_layout(height=500, title_text=r"Daily Returns Histograms", showlegend=False)

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

#### 如果要用數字嚟描述一下啲Data，可以計以下四個Moments：

##### Mean (1st Moment)
    - 平均Daily Return有幾多
##### Variance (2nd Moment)
    - 平均Daily Return同實際Data Point差幾遠，可以理解成「一般風險」。
##### Skewness (3rd Moment)
    - 啲Daily Return 會唔會平時冇乜嘢，不過每隔一排就一舖過輸身家咁(Negative Skew)？
    - 定係好似買六合彩咁九成九都嬴唔到，不過買好多好多次可能會嬴舖勁嘅(Positive Skew)？
##### Kurtosis (4th Moment)
    - 啲Data係唔係極端分散，可以理解成為「極端事件」多唔多發生。

    

""")

st.markdown(r"""

每隻股票Raw Data有252個Day Close Price $$ P_t $$，所以一共有251個Return $$ R_t $$，$$ n = 251 $$ 

通常啲 Statistics 嘅 Software 都會有個類似 Describe 嘅 Function，一Call佢就會出哂呢四粒數。

不過用呢啲 Function 最緊要係 Check 清楚 Documentation，例如Python scipy.stats.describe 就寫明冇處理 skewness 同 kurtosis 嘅 bias。


""")

screen_width = streamlit_js_eval(js_expressions="window.innerWidth", key="screen_width")
use_desktop = screen_width is not None and screen_width > 768
with st.expander("做個簡單Simulation就可以Feel 到乜嘢係Moments", expanded=False):
    if use_desktop:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            target_mean = st.slider("Mean", -0.50, 0.5, 0.02)
        with col2:
            target_variance = st.slider("Variance", 0.01, 0.09, 0.01)
        with col3:
            target_skewness = st.slider("Skewness", -2.5, 2.5, 0.1)
        with col4:
            target_kurtosis = st.slider("Excess Kurtosis", 0.01, 5.0, 0.01)
    else:  # Mobile or width not yet detected - vertical stack
        st.markdown(r"###### Parameters")
        target_mean = st.slider("Mean", -0.50, 0.5, 0.02)
        target_variance = st.slider("Variance", 0.01, 0.09, 0.01)
        target_skewness = st.slider("Skewness", -2.5, 2.5, 0.1)
        target_kurtosis = st.slider("Excess Kurtosis", 0.01, 5.0, 0.01)

    # hardcoded parameters
    samples_count = 20000
    seed = 2351397

    # estimate the parameters
    try:
        param_a, param_b, param_loc, param_scale = find_johnson_su_params_by_moments(target_mean, target_variance, target_skewness, target_kurtosis)
        np.random.seed(seed)
        sim_moments_data = johnsonsu.rvs(a=param_a, b=param_b, loc=param_loc, scale=param_scale, size=samples_count)
        theo_mean, theo_variance, theo_skewness, theo_kurtosis = johnsonsu.stats(param_a, param_b, loc=param_loc, scale=param_scale, moments='mvsk')
    except:
        sim_moments_data = np.random.normal(loc=target_mean, scale=np.sqrt(target_variance), size=samples_count)
        theo_mean = target_mean
        theo_variance = target_variance
        theo_skewness = 0.0
        theo_kurtosis = 0.0
        st.markdown(r"""
        <span style="color: red;">Solve 唔到 parameters，求其俾住Normal先</span>
        """, unsafe_allow_html=True)

    sample_mean = tmean(sim_moments_data)
    sample_variance = tvar(sim_moments_data)
    sample_skewness = skew(sim_moments_data, bias=False)
    sample_kurtosis = kurtosis(sim_moments_data, fisher=True, bias=False)

    if use_desktop:
        with col1:
            st.latex(f"\\textsf{{Sample Mean }} \\bar{{R}} \\\\ {sample_mean:.3f}")
        with col2:
            st.latex(f"\\textsf{{Sample Variance }} s \\\\ {sample_variance:.3f}")
        with col3:
            st.latex(f"\\textsf{{Sample Skewness }} G_1 \\\\ {sample_skewness:.3f}")
        with col4:
            st.latex(f"\\textsf{{Sample (Excess) Kurtosis }} G_2 \\\\ {sample_kurtosis:.3f}")
    else:
        st.latex(f"\\textsf{{Sample Mean }} \\bar{{R}} \\\\ {sample_mean:.3f}")
        st.latex(f"\\textsf{{Sample Variance }} s \\\\ {sample_variance:.3f}")
        st.latex(f"\\textsf{{Sample Skewness }} G_1 \\\\ {sample_skewness:.3f}")
        st.latex(f"\\textsf{{Sample Kurtosis }} G_2 \\\\ {sample_kurtosis:.3f}")

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
        xaxis=dict(range=[-4, 4], showgrid=True, gridwidth=1, zeroline=True),
        yaxis=dict(range=[0, 2000], showgrid=True, gridwidth=1, zeroline=True),
    )
    st.plotly_chart(sim_moments_fig, width="content")

with st.expander("Formula", expanded=False):
    st.markdown(r"""

    啲stat嘅formula 真係樣衰到呢…………唉…… 

    Concept：
    
    - 左邊Definition個 $$ R $$ 係一個 Random Variable，係一個Black Box，我地永遠都唔會知佢Exactly係點運作。
    
    - 右邊Estimator嘅 $$ R_i : i = 1, 2, 3 \ldots n $$ 係一堆 Sample Data Points，我地係用右邊嘅Formula 去估左邊嗰條數。


    |  | Definition | Estimator |
    |:---|:---|:---|
    |Mean (1st Moment)| $$ \mu = E \bigr[ R \bigl] $$ | $$ \bar{R} = \frac{\sum_{i=1}^{n} R_i}{n} $$ |
    |Variance (2nd Moment)| $$ Var(R) = \sigma^2 = E \bigr[ (R-\mu)^2 \bigl] $$ | $$ s^2 = \frac{\sum_{i=1}^{n} (R_i - \bar{R})^2}{n-1} $$ |
    |Standard Deviation / Volatility | $$ \sigma = \sqrt{Var(R)} $$ | $$ s = \sqrt{\frac{\sum_{i=1}^{n} (R_i - \bar{R})^2}{n-1}} $$ |
    |Skewness (3rd Moment)| $$ \gamma_1 = E \Bigr[ \bigr(\frac{R-\mu}{\sigma} \bigl)^3 \Bigl] $$ | $$ G_1 = \frac{n}{(n-1)(n-2)} \sum_{i=1}^{n} \left( \frac{R_i - \bar{R}}{s} \right)^3 $$ |
    |Kurtosis (4th Moment)| $$ \kappa = E \Bigr[ \bigr(\frac{R-\mu}{\sigma} \bigl)^4 \Bigl] $$ | $$ K = \frac{n(n+1)}{(n-1)(n-2)(n-3)} \sum_{i=1}^{n} \left( \frac{R_i - \bar{R}}{s} \right)^4  $$ |
    |Excess Kurtosis| $$ \gamma_2 = E \Bigr[ \bigr(\frac{R-\mu}{\sigma} \bigl)^4 \Bigl] - 3 $$ | $$ G_2 = \frac{n(n+1)}{(n-1)(n-2)(n-3)} \sum_{i=1}^{n} \left( \frac{R_i - \bar{R}}{s} \right)^4 - \frac{3(n-1)^2}{(n-2)(n-3)} $$ |
    """)

    st.markdown(r"""
    
    Note：
    
    - 好多時講Return 我地都會講Volatility (波幅)，其實即係 Standard Deviation (Variance Square Root)。
    
    - 而Mean / Variance / Volatility 我地會做一個Annualized 嘅轉換：
      - Mean 乘 $$ 252 $$ (假設一年252 個 trading days)
      - Variance 都係乘 $$ 252 $$
      - Volatility 乘 $$ \sqrt{252} $$

    - 通常喺Finance 嘅世界，一般都係講Excess Kurtosis (i.e. Kurtosis - 3)。
    
    - 因為Normal Distribution 嘅 Kurtosis 係 3，槪念係講緊究竟啲Data 肥過Normal多。Excess Kurtosis 將佢Normalize返去0，正數就代表佢肥過Normal， 不過Excess Kurtosis唔係一個Moment。

    """)

stock1_sample_mean = tmean(stock1_daily_return)
stock1_sample_variance = tvar(stock1_daily_return)
stock1_sample_volatility = np.sqrt(stock1_sample_variance)
stock1_sample_skewness = skew(stock1_daily_return, bias=False)
stock1_sample_kurtosis = kurtosis(stock1_daily_return, fisher=True, bias=False)

stock2_sample_mean = tmean(stock2_daily_return)
stock2_sample_variance = tvar(stock2_daily_return)
stock2_sample_volatility = np.sqrt(stock2_sample_variance)
stock2_sample_skewness = skew(stock2_daily_return, bias=False)
stock2_sample_kurtosis = kurtosis(stock2_daily_return, fisher=True, bias=False)

spx_sample_mean = tmean(spx_daily_return)
spx_sample_variance = tvar(spx_daily_return)
spx_sample_volatility = np.sqrt(spx_sample_variance)
spx_sample_skewness = skew(spx_daily_return, bias=False)
spx_sample_kurtosis = kurtosis(spx_daily_return, fisher=True, bias=False)

ccmp_sample_mean = tmean(ccmp_daily_return)
ccmp_sample_variance = tvar(ccmp_daily_return)
ccmp_sample_volatility = np.sqrt(ccmp_sample_variance)
ccmp_sample_skewness = skew(ccmp_daily_return, bias=False)
ccmp_sample_kurtosis = kurtosis(ccmp_daily_return, fisher=True, bias=False)

st.markdown(r"""

##### 上面嗰兩隻Stock 1 同 Stock 2 其實都係兩隻美國嘅科技龍頭股，S&P 500 代表美國般市場表現，而NASDAQ Composite 就代表科技股普遍嘅表現

我地可以計一計佢哋嘅Stats：

""")

st.markdown(f"""
    | | Stock 1 | Stock 2 | S&P 500 | NASDAQ Composite |
    |:---|---:|---:|---:|---:|
    |Mean (Annualized)| $$ {stock1_sample_mean * 252.0:.4f} $$ | $$ {stock2_sample_mean * 252.0:.4f} $$ | $$ {spx_sample_mean * 252.0:.4f} $$ | $$ {ccmp_sample_mean * 252.0:.4f} $$ |
    |Volatility (Annualized)| $$ {stock1_sample_volatility * np.sqrt(252.0):.4f} $$ | $$ {stock2_sample_volatility * np.sqrt(252.0):.4f} $$ | $$ {spx_sample_volatility * np.sqrt(252.0):.4f}  $$ | $$ {ccmp_sample_volatility * np.sqrt(252.0):.4f} $$ |
    |Skewness| $$ {stock1_sample_skewness:.4f} $$ | $$ {stock2_sample_skewness:.4f} $$ | $$ {spx_sample_skewness:.4f} $$ | $$ {ccmp_sample_skewness:.4f} $$ |
    |Excess Kurtosis| $$ {stock1_sample_kurtosis:.4f} $$ | $$ {stock2_sample_kurtosis:.4f} $$ | $$ {spx_sample_kurtosis:.4f} $$ | $$ {ccmp_sample_kurtosis:.4f} $$ |
    
""")


st.markdown(r"""

##### 數字可以試下咁樣 interpret

- 兩隻科技股雖然Annualized Return高好多（分別係49%同84%）
- 但Annualized Vol亦大得多（兩隻股票分別41%、65%，而大市S&P500得18%，NASDAQ都只係23%）。代表一日波幅可以好瘋狂，抽中一個大日仔贏好多，但輸嗰陣一樣輸勁多。Volatility 係冇正負嘅 Concept。
- Skewness全部 Positive，代表拉上補下，多咗一啲 “大贏” 嘅日子，喺2025下半年科技股狂升嘛。不過呢啲 Positive Skew唔係咁常見，因為正常市場數字一般都係接近零或Slightly Negative。
- Kurtosis全部都係極誇張，尤其S&P 500/NASDAQ（20以上），證明股市唔係平時咁穩定，好多時會出現一次過好誇張大升／大跌，大部分日子冇乜野，一爆就癲哂。


""")


st.markdown(r"""

#### 總結一下：

上面嗰幾點聽落可能好廢，其實可能就咁睇下個圖或者留意下新聞都會有個大概嘅印象，但係用Normalized 左嘅數字嚟睇就可以客觀咁比較，同埋可以用電腦大規模將幾千隻股票一次過計哂 Save 落 Database，跟住就可以有系統咁做 Optimization 同砌一啲 Strategy 出嚟。 

""")