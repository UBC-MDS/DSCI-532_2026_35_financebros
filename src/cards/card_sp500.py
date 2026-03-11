import pandas as pd
import plotly.graph_objects as go
from shiny.express import expressify, ui
from shinywidgets import render_plotly

from _input import input
from data_loader import spy_df


@expressify
def card_sp500(get_filtered_close):
    with ui.card(full_screen=True):
        ui.card_header("Price Performance vs. S&P 500 Benchmark")

        @render_plotly
        def render_sp500_comparison():
            ticker = input.ticker()
            stock_df = get_filtered_close().copy()
            dates = input.dates()

            if stock_df.empty:
                return go.Figure()

            spy_filtered = spy_df[
                (spy_df["Date"] >= pd.Timestamp(dates[0]))
                & (spy_df["Date"] <= pd.Timestamp(dates[1]))
            ].copy()

            stock_df = stock_df.set_index("Date")
            spy_filtered = spy_filtered.set_index("Date")

            if ticker not in stock_df.columns:
                return go.Figure()

            stock_norm = stock_df[ticker] / stock_df[ticker].iloc[0] * 100
            spy_norm = spy_filtered["SPY"] / spy_filtered["SPY"].iloc[0] * 100

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=stock_norm.index, y=stock_norm, mode="lines", name=ticker, line=dict(width=3)))
            fig.add_trace(go.Scatter(x=spy_norm.index, y=spy_norm, mode="lines", name="S&P 500 (SPY)", line=dict(color="orange", width=2)))
            fig.update_layout(
                template="plotly_dark",
                yaxis_title="Normalized Performance (Base = 100)",
                xaxis_title="Date",
                margin=dict(l=10, r=10, t=10, b=10),
            )
            return fig
