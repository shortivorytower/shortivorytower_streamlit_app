import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_js_eval import streamlit_js_eval

# ==========================================
# Helper Functions
# ==========================================


def generate_gbm_prices(S0, mu, sigma, days, seed=42):
    """
    Generate simulated stock prices using Geometric Brownian Motion.
    """
    np.random.seed(seed)
    dt = 1 / 252  # daily step
    prices = [S0]
    for _ in range(days - 1):
        dW = np.random.normal(0, np.sqrt(dt))
        S_new = prices[-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * dW)
        prices.append(S_new)
    return np.array(prices)


def compute_simple_returns(prices):
    """Simple returns: (P_t - P_{t-1}) / P_{t-1}"""
    return np.diff(prices) / prices[:-1]


def compute_log_returns(prices):
    """Log returns: ln(P_t / P_{t-1})"""
    return np.log(prices[1:] / prices[:-1])


def annualized_return_arithmetic(daily_returns):
    """Arithmetic mean annualized: mean(r) * 252"""
    return np.mean(daily_returns) * 252


def annualized_return_geometric(daily_returns):
    """Geometric mean annualized: (prod(1+r))^(252/n) - 1"""
    n = len(daily_returns)
    total_return = np.prod(1 + daily_returns)
    return total_return ** (252 / n) - 1


def annualized_volatility(daily_returns):
    """Annualized volatility: std(r) * sqrt(252)"""
    return np.std(daily_returns, ddof=1) * np.sqrt(252)


# ==========================================
# UI - Title
# ==========================================
st.title("How to Estimate Annualized Return and Volatility")
st.write(
    "### (DRAFT TESTING Streamlit capabilities only) Using Single Stock Daily Close Prices"
)

# ==========================================
# Article: What is a Return?
# ==========================================
st.markdown("""
## What is a "Return"?

When we talk about stock returns, there are two common ways to measure them:

### 1. Simple Return (Arithmetic Return)

The simple return measures the percentage change in price:
""")

st.latex(r"r_t = \frac{P_t - P_{t-1}}{P_{t-1}} = \frac{P_t}{P_{t-1}} - 1")

st.markdown("""
### 2. Log Return (Continuously Compounded Return)

The log return uses the natural logarithm:
""")

st.latex(r"r_t^{log} = \ln\left(\frac{P_t}{P_{t-1}}\right) = \ln(P_t) - \ln(P_{t-1})")

st.markdown("""
**Why use log returns?**
- Log returns are additive over time (simple returns are not)
- They are symmetric: a +10% log return followed by -10% brings you back to start
- They are commonly used in quantitative finance models (e.g., Black-Scholes assumes log-normal prices)

---

## Annualized Return

Daily returns are small numbers. To make them comparable, we annualize them (assuming ~252 trading days per year).

### Method 1: Arithmetic Mean

Simply multiply the average daily return by 252:
""")

st.latex(r"\text{Annualized Return}_{arith} = \bar{r} \times 252")

st.markdown("""
This is simple but **overstates** returns when volatility is high.

### Method 2: Geometric Mean (Compound Return)

This accounts for compounding:
""")

st.latex(
    r"\text{Annualized Return}_{geom} = \left( \prod_{i=1}^{n} (1 + r_i) \right)^{252/n} - 1"
)

st.markdown("""
The geometric mean is generally more accurate for actual investment performance.

---

## Annualized Volatility

Volatility measures the dispersion of returns. We annualize it by multiplying by the square root of 252:
""")

st.latex(r"\sigma_{annual} = \sigma_{daily} \times \sqrt{252}")

st.markdown("""
**Why square root?**

Under the assumption that daily returns are independent and identically distributed (i.i.d.), variance scales linearly with time:
""")

st.latex(r"\text{Var}(R_{annual}) = 252 \times \text{Var}(R_{daily})")
st.latex(r"\sigma_{annual} = \sqrt{252} \times \sigma_{daily}")

st.markdown("""
### Simple vs Log Returns for Volatility

- Using **simple returns**: `std(simple returns) * sqrt(252)`
- Using **log returns**: `std(log returns) * sqrt(252)`

For typical stock volatilities (< 50% annual), the difference is small. Log returns are more commonly used in academic literature and derivatives pricing.

---

## Interactive Example

Adjust the simulation parameters below to see how annualized return and volatility change.
""")

# ==========================================
# Simulation Parameters
# ==========================================
screen_width = streamlit_js_eval(js_expressions="window.innerWidth", key="screen_width")

with st.expander("Simulation Parameters", expanded=True):
    if screen_width and screen_width > 768:  # Desktop - use 3 columns
        col1, col2, col3 = st.columns(3)
        with col1:
            sim_S0 = st.number_input("Initial Price (S0)", value=100.0, min_value=1.0)
            sim_mu = st.slider("Drift (mu, annual %)", -50.0, 50.0, 10.0) / 100.0
        with col2:
            sim_sigma = (
                st.slider("Volatility (sigma, annual %)", 5.0, 100.0, 25.0) / 100.0
            )
            sim_days = st.slider("Trading Days", 30, 504, 252)
        with col3:
            sim_seed = st.number_input("Random Seed", value=42, min_value=0)
    else:  # Mobile or width not yet detected - vertical stack
        sim_S0 = st.number_input("Initial Price (S0)", value=100.0, min_value=1.0)
        sim_mu = st.slider("Drift (mu, annual %)", -50.0, 50.0, 10.0) / 100.0
        sim_sigma = st.slider("Volatility (sigma, annual %)", 5.0, 100.0, 25.0) / 100.0
        sim_days = st.slider("Trading Days", 30, 504, 252)
        sim_seed = st.number_input("Random Seed", value=42, min_value=0)

# Generate sample data
prices = generate_gbm_prices(sim_S0, sim_mu, sim_sigma, sim_days, seed=int(sim_seed))
dates = pd.date_range(start="2025-01-02", periods=sim_days, freq="B")
df = pd.DataFrame({"Date": dates, "Close": prices})

# Compute returns
simple_returns = compute_simple_returns(prices)
log_returns = compute_log_returns(prices)

# Compute metrics
ann_ret_arith_simple = annualized_return_arithmetic(simple_returns)
ann_ret_geom_simple = annualized_return_geometric(simple_returns)
ann_vol_simple = annualized_volatility(simple_returns)
ann_vol_log = annualized_volatility(log_returns)

st.markdown("#### Results")
st.write(
    f"Simulated {sim_days} days of GBM prices with drift={sim_mu * 100:.1f}%, vol={sim_sigma * 100:.1f}%"
)

# --- Metrics ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Ann. Return (Arithmetic)", f"{ann_ret_arith_simple * 100:.2f}%")
col2.metric("Ann. Return (Geometric)", f"{ann_ret_geom_simple * 100:.2f}%")
col3.metric("Ann. Volatility (Simple)", f"{ann_vol_simple * 100:.2f}%")
col4.metric("Ann. Volatility (Log)", f"{ann_vol_log * 100:.2f}%")

# --- Charts ---
fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "Price Series",
        "Daily Simple Returns",
        "Returns Histogram",
        "Log Returns Histogram",
    ),
    vertical_spacing=0.12,
    horizontal_spacing=0.08,
)

# Price chart
fig.add_trace(
    go.Scatter(
        x=dates, y=prices, mode="lines", name="Close Price", line=dict(color="#1f77b4")
    ),
    row=1,
    col=1,
)

# Simple returns time series
fig.add_trace(
    go.Scatter(
        x=dates[1:],
        y=simple_returns,
        mode="lines",
        name="Simple Returns",
        line=dict(color="#2ca02c"),
    ),
    row=1,
    col=2,
)

# Simple returns histogram
fig.add_trace(
    go.Histogram(
        x=simple_returns,
        nbinsx=30,
        name="Simple Returns",
        marker_color="#2ca02c",
        opacity=0.7,
    ),
    row=2,
    col=1,
)

# Log returns histogram
fig.add_trace(
    go.Histogram(
        x=log_returns,
        nbinsx=30,
        name="Log Returns",
        marker_color="#9467bd",
        opacity=0.7,
    ),
    row=2,
    col=2,
)

fig.update_layout(height=600, showlegend=False)
fig.update_xaxes(title_text="Date", row=1, col=1)
fig.update_xaxes(title_text="Date", row=1, col=2)
fig.update_xaxes(title_text="Return", row=2, col=1)
fig.update_xaxes(title_text="Return", row=2, col=2)
fig.update_yaxes(title_text="Price ($)", row=1, col=1)
fig.update_yaxes(title_text="Return", row=1, col=2)
fig.update_yaxes(title_text="Frequency", row=2, col=1)
fig.update_yaxes(title_text="Frequency", row=2, col=2)

st.plotly_chart(fig, use_container_width=True)

# --- Sample Data Preview ---
with st.expander("View Sample Data"):
    display_df = df.copy()
    display_df["Simple Return"] = [np.nan] + list(simple_returns)
    display_df["Log Return"] = [np.nan] + list(log_returns)
    st.dataframe(display_df, use_container_width=True)

# ==========================================
# Summary Table
# ==========================================
st.markdown("""
---

## When to Use Which?

| Metric | Arithmetic | Geometric/Log |
|--------|------------|---------------|
| **Return** | Quick estimate, benchmarking | Actual compounded performance |
| **Volatility** | Simple approximation | Derivatives pricing, VaR |

For most practical purposes with daily data, the differences are minor. Use log returns if you want consistency with Black-Scholes and other standard models.
""")

# ==========================================
# Discussion
# ==========================================
st.markdown("---")
st.write("## Discussion")
st.markdown("""
Have questions or comments? Join the conversation on GitHub Discussions.

[Open Discussion on GitHub](https://github.com/shortivorytower/shortivorytower_streamlit_app/discussions)
""")
