"""
v2.py — Standalone test: Risk vs Return scatter (Magnificent 7)

Inputs:
- Date range
- Window: Full / 1Y / 5Y / 10Y
- Highlight ticker

Data:
- data/close.csv

Run:
  shiny run --reload src/components/v2.py
"""
"""
v2.py — Simple Shiny Core test: Risk vs Return scatter
Run:
  shiny run --reload src/components/v2.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_plotly

# --- load close.csv ---
DATA_DIR = Path(__file__).parent.parent.parent / "data"
close_df = pd.read_csv(DATA_DIR / "close.csv", parse_dates=["Date"])

DATE_MIN = close_df["Date"].min()
DATE_MAX = close_df["Date"].max()

TICKERS = [c for c in close_df.columns if c != "Date"]

app_ui = ui.page_fluid(
    ui.h4("Risk vs Return (test)"),
    ui.layout_columns(
        ui.input_select(
            "ticker",
            "Highlight ticker",
            choices=TICKERS,
            selected=TICKERS[0] if len(TICKERS) else None,
        ),
        ui.input_select(
            "rr_period",
            "Window",
            choices=["Full", "1Y", "5Y", "10Y"],
            selected="Full",
        ),
        col_widths=[6, 6],
    ),
    ui.input_date_range(
        "dates",
        "Date range",
        start=DATE_MIN,
        end=DATE_MAX,
        min=DATE_MIN,
        max=DATE_MAX,
    ),
    output_widget("rr_plot_test"),
)


def _padded_range(vals: pd.Series, pad_frac: float = 0.12):
    vals = pd.to_numeric(vals, errors="coerce").dropna()
    if vals.empty:
        return None
    vmin = float(vals.min())
    vmax = float(vals.max())
    if np.isclose(vmin, vmax):
        pad = abs(vmin) * pad_frac if vmin != 0 else 0.01
        return (vmin - pad, vmax + pad)
    pad = (vmax - vmin) * pad_frac
    return (vmin - pad, vmax + pad)


def server(input, output, session):
    @reactive.calc
    def analysis_close():
        d0, d1 = input.dates()
        df = close_df[
            (close_df["Date"] >= pd.Timestamp(d0))
            & (close_df["Date"] <= pd.Timestamp(d1))
        ].copy()
        df = df.sort_values("Date")

        if df.empty:
            return df

        period = input.rr_period()
        if period == "Full":
            return df

        years = {"1Y": 1, "5Y": 5, "10Y": 10}[period]
        end_date = df["Date"].max()
        start_date = end_date - pd.DateOffset(years=years)
        return df[df["Date"] >= start_date].copy()

    @reactive.calc
    def risk_return_df():
        df = analysis_close()
        if df.empty:
            return pd.DataFrame(columns=["Ticker", "AnnReturn", "AnnVol"])

        prices = df.set_index("Date")[TICKERS].astype(float)
        rets = prices.pct_change().dropna(how="all")
        if rets.empty:
            return pd.DataFrame(columns=["Ticker", "AnnReturn", "AnnVol"])

        mean_daily = rets.mean()
        std_daily = rets.std()

        out = pd.DataFrame(
            {
                "Ticker": mean_daily.index,
                "AnnReturn": mean_daily.values * 252,
                "AnnVol": std_daily.values * np.sqrt(252),
            }
        ).dropna()

        return out.reset_index(drop=True)

    @render_plotly
    def rr_plot_test():
        rr = risk_return_df()
        hi = input.ticker()

        # ---- EMPTY DATA: still show nice % axes (no -1..5) ----
        if rr.empty:
            fig = go.Figure()
            fig.update_layout(
                template="plotly_dark",
                height=520,
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis_title="Annualized Volatility",
                yaxis_title="Annualized Return",
                xaxis=dict(range=[-0.1, 0.1], tickformat=".0%"),
                yaxis=dict(range=[-0.1, 0.1], tickformat=".0%"),
                annotations=[
                    dict(
                        text="No data in selected range",
                        x=0.5,
                        y=0.5,
                        xref="paper",
                        yref="paper",
                        showarrow=False,
                        font=dict(size=16),
                    )
                ],
            )
            return fig

        # ---- axis ranges so ALL points are always visible ----
        x_rng = _padded_range(rr["AnnVol"], pad_frac=0.15)
        y_rng = _padded_range(rr["AnnReturn"], pad_frac=0.15)

        fig = go.Figure()

        others = rr[rr["Ticker"] != hi]
        fig.add_trace(
            go.Scatter(
                x=others["AnnVol"],
                y=others["AnnReturn"],
                mode="markers+text",
                text=others["Ticker"],
                textposition="top center",
                marker=dict(size=12, opacity=0.65),
                hovertemplate="Ticker=%{text}<br>Vol=%{x:.2%}<br>Return=%{y:.2%}<extra></extra>",
                showlegend=False,
            )
        )

        selected = rr[rr["Ticker"] == hi]
        if not selected.empty:
            fig.add_trace(
                go.Scatter(
                    x=selected["AnnVol"],
                    y=selected["AnnReturn"],
                    mode="markers+text",
                    text=selected["Ticker"],
                    textposition="top center",
                    marker=dict(size=18, opacity=1.0, line=dict(width=2, color="white")),
                    hovertemplate="Ticker=%{text}<br>Vol=%{x:.2%}<br>Return=%{y:.2%}<extra></extra>",
                    showlegend=False,
                )
            )

        fig.update_layout(
            template="plotly_dark",
            height=520,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Annualized Volatility",
            yaxis_title="Annualized Return",
            xaxis=dict(range=x_rng, tickformat=".0%", constrain="domain"),
            yaxis=dict(range=y_rng, tickformat=".0%", constrain="domain"),
        )

        return fig


app = App(app_ui, server)