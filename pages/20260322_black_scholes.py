import streamlit as st
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go


# ==========================================
# Core Math: Black-Scholes Call Formula
# ==========================================
def black_scholes_call(S0, K, T, r, sigma):
    """
    Calculate Black-Scholes Call Option price.
    Returns: (call_price, d1, d2)
    """
    if T == 0:
        return max(0, S0 - K), 0.0, 0.0

    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = (S0 * norm.cdf(d1)) - (K * np.exp(-r * T) * norm.cdf(d2))

    return call_price, d1, d2


# ==========================================
# UI - Title
# ==========================================
st.title("Black-Scholes Model")
st.write("### (DRAFT TESTING Streamlit capabilities only) Interactive Option Pricing")

# ==========================================
# Article: Introduction
# ==========================================
st.markdown("""
## Introduction

The Black-Scholes formula assumes stock prices follow a 
**Geometric Brownian Motion (GBM)**.

---

## The Formula

The price of a European call option is given by:
""")

st.latex(r"C(S_0, T) = S_0 N(d_1) - Ke^{-rT} N(d_2)")
st.latex(
    r"d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}"
)

st.markdown(r"""
Where:
- $S_0$ = Current stock price
- $K$ = Strike price
- $T$ = Time to expiration (in years)
- $r$ = Risk-free interest rate
- $\sigma$ = Volatility of the stock
- $N(\cdot)$ = Cumulative standard normal distribution

---

## Calculated Results

Adjust the model parameters below to see how the call option price changes.
""")

# ==========================================
# Sidebar Parameters
# ==========================================
st.sidebar.header("Model Parameters")
input_S0 = st.sidebar.slider("Stock Price (S0)", 50.0, 150.0, 100.0)
input_K = st.sidebar.slider("Strike Price (K)", 50.0, 150.0, 105.0)
input_T = st.sidebar.slider("Time to Expiry (T, years)", 0.01, 5.0, 1.0)
input_r = st.sidebar.slider("Risk-free Rate (r, %)", 0.0, 15.0, 5.0) / 100.0
input_sigma = st.sidebar.slider("Volatility (sigma, %)", 5.0, 100.0, 30.0) / 100.0

# Calculate result
call_price, d1, d2 = black_scholes_call(
    input_S0, input_K, input_T, input_r, input_sigma
)

# --- Metrics ---
st.markdown("#### Results")
col1, col2, col3 = st.columns(3)
col1.metric("Call Option Price", f"${call_price:.2f}")
col2.metric("d1", f"{d1:.4f}")
col3.metric("d2", f"{d2:.4f}")

# ==========================================
# Article: Vega
# ==========================================
st.markdown("""
---

## Key Insight: Vega

The Black-Scholes model tells us that both **time** and **volatility** have value.

The option's sensitivity to volatility is called **Vega**:
""")

st.latex(
    r"\text{Vega} = \frac{\partial C}{\partial \sigma} = S_0 \sqrt{T} \cdot N'(d_1)"
)

st.markdown("""
Higher volatility increases option value because there's more potential for large price movements.

### Vega Analysis: Call Price vs. Volatility
""")

# --- Vega Chart ---
vol_range = np.linspace(0.05, 1.0, 50)
prices_vs_vol = [
    black_scholes_call(input_S0, input_K, input_T, input_r, v)[0] for v in vol_range
]

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=vol_range * 100,
        y=prices_vs_vol,
        mode="lines",
        name="Call Price",
        line=dict(color="#1f77b4", width=2),
    )
)

# Mark current volatility
fig.add_trace(
    go.Scatter(
        x=[input_sigma * 100],
        y=[call_price],
        mode="markers",
        name="Current",
        marker=dict(color="red", size=12, symbol="diamond"),
    )
)

fig.update_layout(
    title=f"Call Price vs. Volatility (K={input_K}, T={input_T})",
    xaxis_title="Volatility (%)",
    yaxis_title="Option Price ($)",
    showlegend=True,
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Discussion
# ==========================================
st.markdown("---")
st.write("## Discussion")
st.markdown("""
Have questions or comments? Join the conversation on GitHub Discussions.

[Open Discussion on GitHub](https://github.com/shortivorytower/shortivorytower_streamlit_app/discussions)
""")
