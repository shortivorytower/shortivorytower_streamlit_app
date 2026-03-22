import streamlit as st
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
import streamlit.components.v1 as components


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
st.write("### Interactive Option Pricing")

# ==========================================
# Article: Introduction
# ==========================================
st.markdown("""
## Introduction

This is a test for using interactive methods to keep records.

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
# Inline Parameters (moved from sidebar)
# ==========================================
st.markdown("#### Model Parameters")
param_col1, param_col2, param_col3, param_col4, param_col5 = st.columns(5)

with param_col1:
    input_S0 = st.slider("Stock Price (S0)", 50.0, 150.0, 100.0)
with param_col2:
    input_K = st.slider("Strike Price (K)", 50.0, 150.0, 105.0)
with param_col3:
    input_T = st.slider("Time to Expiry (T, years)", 0.01, 5.0, 1.0)
with param_col4:
    input_r = st.slider("Risk-free Rate (r, %)", 0.0, 15.0, 5.0) / 100.0
with param_col5:
    input_sigma = st.slider("Volatility (sigma, %)", 5.0, 100.0, 30.0) / 100.0

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

col_info1, col_info2 = st.columns([1, 2])

with col_info1:
    st.write("#### Analytics")
    st.markdown(
        "![Views](https://moe-counter.glitch.me/get/@your_github_username_quant_blog?theme=rule34)"
    )

with col_info2:
    st.write("## Discussion")
    st.write("Leave a comment below (requires GitHub account).")

    giscus_html = """
        <script src="https://giscus.app/client.js"
                data-repo="shortivorytower/shortivorytower_streamlit_app"
                data-repo-id="R_kgDORtjWOw"
                data-category="General"
                data-category-id="DIC_kwDORtjWO84C5A0a"
                data-mapping="pathname"
                data-strict="0"
                data-reactions-enabled="1"
                data-emit-metadata="0"
                data-input-position="bottom"
                data-theme="preferred_color_scheme"
                data-lang="zh-HK"
                crossorigin="anonymous"
                async>
        </script>
    """
    components.html(giscus_html, height=600, scrolling=True)
