# dashboard.py
"""
Full Financial Dashboard (KPIs, Cash Flow, EBITDA, ARIMA Forecasting)
Single-file Streamlit app. Generates synthetic data and demonstrates KPI computation,
ARIMA forecasting with statsmodels (auto_arima via pmdarima recommended), and interactive Plotly visualizations.
"""

import streamlit as st
if "state_var" not in st.session_state:
    st.session_state.state_var = 0

st.set_page_config(layout="wide", page_title="Financial Dashboard", initial_sidebar_state="expanded")

import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Forecasting
from statsmodels.tsa.arima.model import ARIMA
import pmdarima as pm
import warnings
warnings.filterwarnings("ignore")

# -----------------------
# Utilities & Data Gen
# -----------------------
@st.cache_data
def generate_financials(start_date="2019-01-01", months=72, seed=42):
    """
    Generate synthetic monthly P&L and cashflow for `months` months.
    Returns a DataFrame with monthly Revenue, COGS, Opex, Depreciation, Interest, Tax, and Cash Flow items.
    """
    np.random.seed(seed)
    dates = pd.date_range(start=start_date, periods=months, freq="MS")
    t = np.arange(months)

    # Base revenue with seasonality & trend
    base_rev = 200_000
    trend = 2_000 * t  # monthly linear trend
    seasonal = 20_000 * np.sin(2 * np.pi * (t % 12) / 12)  # yearly seasonality
    noise = np.random.normal(0, 12_000, size=months)
    revenue = base_rev + trend + seasonal + noise
    revenue = np.maximum(revenue, 10_000)  # avoid negatives

    # COGS as % of revenue with some noise
    cogs_pct = 0.45 + 0.03 * np.sin(2 * np.pi * (t % 12) / 12 + 0.5)  # small seasonality
    cogs = revenue * cogs_pct + np.random.normal(0, 2_000, size=months)

    # Opex (SG&A) partly fixed + variable
    opex_fixed = 40_000
    opex_variable = 0.10 * revenue
    opex_noise = np.random.normal(0, 3_000, size=months)
    opex = opex_fixed + opex_variable + opex_noise

    # Depreciation (stable), Interest (small), Tax (applied on pre-tax)
    depreciation = np.full(months, 5_000)
    interest = 2_000 + 200 * np.sin(2 * np.pi * t / 24)
    pretax_income = revenue - cogs - opex - depreciation - interest
    tax_rate = 0.20
    tax = np.where(pretax_income > 0, pretax_income * tax_rate, 0)

    net_income = pretax_income - tax

    # Cashflow: add non-cash (depr) and changes in working capital simulated
    working_cap_change = -np.round(np.random.normal(2000, 8_000, size=months))
    capex = np.where((t % 36) == 0, 50_000, 4_000 + np.random.normal(0, 1_000, size=months))
    cash_from_operations = net_income + depreciation + ( - working_cap_change)
    free_cash_flow = cash_from_operations - capex

    df = pd.DataFrame({
        "date": dates,
        "revenue": revenue,
        "cogs": cogs,
        "opex": opex,
        "depreciation": depreciation,
        "interest": interest,
        "tax": tax,
        "net_income": net_income,
        "working_cap_change": working_cap_change,
        "capex": capex,
        "cash_from_operations": cash_from_operations,
        "free_cash_flow": free_cash_flow
    }).set_index("date")

    # Round for display
    df = df.round(2)
    return df

# -----------------------
# KPI Calculations
# -----------------------
def compute_kpis(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    # Basic KPIs
    revenue = latest["revenue"]
    revenue_prev = prev["revenue"]
    revenue_mom = (revenue / revenue_prev - 1) if revenue_prev != 0 else np.nan

    gross_profit = revenue - latest["cogs"]
    gross_margin = gross_profit / revenue

    operating_income = revenue - latest["cogs"] - latest["opex"] - latest["depreciation"]
    ebitda = revenue - latest["cogs"] - latest["opex"]
    ebitda_margin = ebitda / revenue

    net_income = latest["net_income"]

    # Cash KPIs
    fcf = latest["free_cash_flow"]
    cash_from_ops = latest["cash_from_operations"]

    # Growth metrics (YoY)
    try:
        yoy_idx = df.index.get_loc(df.index[-1] - pd.DateOffset(years=1))
    except Exception:
        # fallback: use 12 months back by position
        yoy_idx = -13 if len(df) > 12 else None

    if yoy_idx is not None and abs(yoy_idx) <= len(df):
        rev_yoy = (revenue / df["revenue"].iloc[yoy_idx]) - 1
    else:
        rev_yoy = np.nan

    # CAGR over the full period
    start_rev = df["revenue"].iloc[0]
    n_years = (df.index[-1] - df.index[0]).days / 365.25
    cagr = (revenue / start_rev) ** (1 / n_years) - 1 if start_rev > 0 else np.nan

    kpis = {
        "Revenue": revenue,
        "Revenue MoM %": revenue_mom,
        "Revenue YoY %": rev_yoy,
        "Revenue CAGR %": cagr,
        "Gross Profit": gross_profit,
        "Gross Margin %": gross_margin,
        "EBITDA": ebitda,
        "EBITDA Margin %": ebitda_margin,
        "Operating Income": operating_income,
        "Net Income": net_income,
        "Free Cash Flow": fcf,
        "Cash from Ops": cash_from_ops
    }
    return kpis

# -----------------------
# Forecasting (ARIMA)
# -----------------------
def arima_forecast(series, periods=12, seasonal=True, m=12):
    """
    Uses pmdarima.auto_arima to determine reasonable ARIMA parameters and then
    fits statsmodels.ARIMA to produce forecast and confidence intervals.
    Returns DataFrame with forecast, lower, upper.
    """
    # Ensure series has a datetime index and is monthly
    series = series.asfreq('MS')
    # Use auto_arima to get order
    try:
        auto = pm.auto_arima(series, seasonal=seasonal, m=m, suppress_warnings=True, stepwise=True, error_action="ignore", max_p=5, max_q=5)
        order = auto.order
        seasonal_order = auto.seasonal_order if seasonal else (0, 0, 0, 0)
    except Exception:
        # fallback
        order = (1, 1, 1)
        seasonal_order = (0, 0, 0, 0)

    # Fit statsmodels ARIMA
    model = ARIMA(series, order=order)
    fit = model.fit()
    res = fit.get_forecast(steps=periods)
    mean = res.predicted_mean
    conf = res.conf_int(alpha=0.05)
    df_fore = pd.DataFrame({
        "forecast": mean,
        "lower": conf.iloc[:, 0],
        "upper": conf.iloc[:, 1]
    })
    return df_fore, order

# -----------------------
# Plotting helpers (Plotly)
# -----------------------
def kpi_cards(kpis):
    # Build a simple KPI row with Plotly indicators, or use Streamlit columns for simpler UI
    cols = st.columns(6)
    labels = ["Revenue", "Revenue MoM %", "EBITDA", "EBITDA Margin %", "Net Income", "Free Cash Flow"]
    for col, label in zip(cols, labels):
        val = kpis.get(label)
        if " %" in label or label.endswith("%"):
            disp = f"{val*100:.2f}%" if pd.notna(val) else "—"
        else:
            disp = f"€{val:,.0f}" if pd.notna(val) else "—"
        col.metric(label=label, value=disp)

# -----------------------
# Main Streamlit UI
# -----------------------
def main():
    st.title("📊 Financial Dashboard — Full Example (Synthetic Data)")

    # Sidebar controls
    st.sidebar.header("Settings")
    start_date = st.sidebar.date_input("Start date", value=datetime(2019, 1, 1))
    months = st.sidebar.slider("Months of history", min_value=36, max_value=120, value=72, step=12)
    forecast_months = st.sidebar.slider("Forecast months", min_value=6, max_value=36, value=12, step=6)
    seed = st.sidebar.number_input("Random seed (for synthetic data)", min_value=0, value=42, step=1)

    df = generate_financials(start_date=start_date.strftime("%Y-%m-%d"), months=months, seed=int(seed))

    # KPIs
    kpis = compute_kpis(df)
    st.subheader("Key Performance Indicators (Latest Month)")
    kpi_cards(kpis)

    # Time series charts: Revenue, EBITDA, Net Income
    st.subheader("Time Series Overview")
    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(x=df.index, y=df["revenue"], name="Revenue", mode="lines+markers", hovertemplate="€%{y:,.0f}<br>%{x|%b %Y}"))
    fig_ts.add_trace(go.Scatter(x=df.index, y=df["revenue"] - df["cogs"], name="Gross Profit", mode="lines"))
    fig_ts.add_trace(go.Scatter(x=df.index, y=df["net_income"], name="Net Income", mode="lines"))
    fig_ts.update_layout(legend=dict(orientation="h"), height=450, margin=dict(l=40, r=20, t=40, b=20))
    st.plotly_chart(fig_ts, use_container_width=True)

    # EBITDA and Margins
    st.subheader("Margins & EBITDA")
    df_m = df.copy()
    df_m["ebitda"] = df_m["revenue"] - df_m["cogs"] - df_m["opex"]
    df_m["ebitda_margin"] = df_m["ebitda"] / df_m["revenue"]

    fig_eb = go.Figure()
    fig_eb.add_trace(go.Bar(x=df_m.index, y=df_m["ebitda"], name="EBITDA"))
    fig_eb.add_trace(go.Scatter(x=df_m.index, y=df_m["ebitda_margin"]*df_m["ebitda"].max(), name="EBITDA Margin (scaled)", mode="lines", yaxis="y2"))
    fig_eb.update_layout(
        yaxis=dict(title="EBITDA (€)"),
        yaxis2=dict(title="EBITDA Margin (scaled)", overlaying="y", side="right", showgrid=False),
        height=450
    )
    st.plotly_chart(fig_eb, use_container_width=True)

    # Profitability heatmap by simulated product/region (example)
    st.subheader("Profitability Heatmap (Products × Regions) — Example")
    products = [f"P{i}" for i in range(1, 9)]
    regions = ["EU", "US", "APAC", "LATAM"]
    profit_margins = np.random.uniform(0.02, 0.35, (len(products), len(regions)))
    heat_df = pd.DataFrame(profit_margins, index=products, columns=regions)

    fig_heat = px.imshow(heat_df, text_auto=".1%", aspect="auto", labels=dict(x="Region", y="Product", color="Margin"))
    fig_heat.update_layout(height=360)
    st.plotly_chart(fig_heat, use_container_width=True)

    # Cashflow waterfall for latest year
    st.subheader("Cash Flow Waterfall (last 12 months)")
    cf = df[["cash_from_operations", "capex", "free_cash_flow"]].tail(12)
    cum_cf = cf.sum()
    wf_items = [
        {"name": "Cash from Operations", "value": cum_cf["cash_from_operations"]},
        {"name": "CapEx", "value": -cum_cf["capex"]},
        {"name": "Free Cash Flow", "value": cum_cf["free_cash_flow"]}
    ]
    # Simple waterfall using bar chart
    wf_df = pd.DataFrame(wf_items)
    fig_wf = go.Figure(go.Bar(x=wf_df["name"], y=wf_df["value"], text=[f"€{v:,.0f}" for v in wf_df["value"]], textposition="auto"))
    fig_wf.update_layout(height=360)
    st.plotly_chart(fig_wf, use_container_width=True)

    # Forecasting
    st.subheader("Revenue Forecast (ARIMA)")
    revenue_series = df["revenue"]
    with st.spinner("Running auto-arima + ARIMA forecast..."):
        try:
            # Use pmdarima to get order; then use statsmodels ARIMA for CI
            arima_res, order = arima_forecast(revenue_series, periods=forecast_months, seasonal=True, m=12)
            last_date = df.index[-1]
            forecast_index = pd.date_range(start=last_date + pd.offsets.MonthBegin(1), periods=forecast_months, freq="MS")
            arima_res.index = forecast_index

            fig_fc = go.Figure()
            fig_fc.add_trace(go.Scatter(x=revenue_series.index, y=revenue_series, name="Historical Revenue"))
            fig_fc.add_trace(go.Scatter(x=arima_res.index, y=arima_res["forecast"], name="ARIMA Forecast", mode="lines"))
            fig_fc.add_trace(go.Scatter(x=arima_res.index, y=arima_res["upper"], name="Upper CI", mode="lines", line=dict(width=0), showlegend=False))
            fig_fc.add_trace(go.Scatter(x=arima_res.index, y=arima_res["lower"], name="Lower CI", mode="lines", line=dict(width=0), fill='tonexty', fillcolor='rgba(0,100,80,0.1)', showlegend=False))
            fig_fc.update_layout(height=480)
            st.plotly_chart(fig_fc, use_container_width=True)

            st.markdown(f"**ARIMA order used (approx)**: {order}")
        except Exception as e:
            st.error(f"Forecasting failed: {e}")

    # Table / Details
    st.subheader("Detailed Financial Table (last 36 months)")
    st.dataframe(df.tail(36).style.format("{:,.2f}"))

    # Download data
    csv = df.to_csv().encode("utf-8")
    st.download_button(label="Download CSV (full)", data=csv, file_name="financials.csv", mime="text/csv")

    st.markdown("---")
    st.caption("This dashboard uses synthetic data for demonstration. Replace `generate_financials` with your real data source (ERP / accounting exports) and adapt account mappings accordingly.")

if __name__ == "__main__":
    main()
