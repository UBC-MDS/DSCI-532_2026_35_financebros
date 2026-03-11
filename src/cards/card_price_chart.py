import pandas as pd
import plotly.graph_objects as go
from shiny.express import expressify, ui
from shinywidgets import render_plotly

from _input import input
from data_loader import close_df


@expressify
def card_price_chart(get_filtered_close):
    with ui.card(full_screen=True):
        ui.card_header("Historical Closing Price Trend")

        @render_plotly
        def render_stock_price_chart():
            ticker = input.ticker()
            df = get_filtered_close().copy()

            if df.empty or ticker not in df.columns:
                fig = go.Figure()
                fig.update_layout(
                    template="plotly_dark",
                    autosize=True,
                    paper_bgcolor="#131722",
                    plot_bgcolor="#1e222d",
                    margin=dict(l=10, r=10, t=10, b=10),
                    annotations=[
                        dict(
                            text="No data available for the selected range/ticker.",
                            x=0.5,
                            y=0.5,
                            xref="paper",
                            yref="paper",
                            showarrow=False,
                            font=dict(color="#d1d4dc", size=14),
                        )
                    ],
                )
                return fig

            df = df.sort_values("Date")
            x = df["Date"]
            y = df[ticker].astype(float)

            start_price = float(y.iloc[0])
            end_price = float(y.iloc[-1])
            pct_change = (end_price / start_price - 1) * 100 if start_price != 0 else 0.0
            pct_color = "#44bb70" if pct_change >= 0 else "#d62728"

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    mode="lines",
                    name=ticker,
                    line=dict(color="#2962ff", width=2.5),
                    hovertemplate="<b>%{x|%Y-%m-%d}</b><br>"
                    f"{ticker}: $%{{y:.2f}}<extra></extra>",
                )
            )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#131722",
                plot_bgcolor="#1e222d",
                margin=dict(l=10, r=10, t=30, b=10),
                hovermode="x unified",
                xaxis=dict(
                    title="Date",
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.06)",
                    rangeslider=dict(visible=True),
                    rangeselector=None,
                ),
                yaxis=dict(
                    title="Close Price ($)",
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.06)",
                    tickprefix="$",
                ),
                title=dict(
                    text=f"{ticker} Close Price  <span style='color:{pct_color}; font-size:12px;'>({pct_change:+.2f}%)</span>",
                    x=0.01,
                    xanchor="left",
                    font=dict(size=16, color="#d1d4dc"),
                ),
                showlegend=False,
            )
            return fig
