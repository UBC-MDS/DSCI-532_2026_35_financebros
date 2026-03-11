import pandas as pd
import plotly.graph_objects as go
from shiny.express import expressify, ui
from shinywidgets import render_plotly

from _input import input


@expressify
def card_risk_return(risk_return_df):
    with ui.card(full_screen=True):
        with ui.card_header():
            ui.div(
                ui.div("Risk-Return Profile", style="font-weight:700;"),
                ui.input_selectize("rr_period", None, choices=["Full", "1Y", "5Y", "10Y"], selected="Full"),
                style="display:flex; justify-content:space-between; align-items:center; width:100%;",
            )

        @render_plotly
        def rr_plot():
            rr = risk_return_df()
            hi = input.ticker()

            X_MIN, X_MAX = 0.0, 1.0
            Y_MIN, Y_MAX = -0.10, 1.0

            LAYOUT_BASE = dict(
                template="plotly_dark",
                autosize=True,
                margin=dict(l=60, r=30, t=20, b=60),
                xaxis_title="Annualized Volatility",
                yaxis_title="Annualized Return",
                xaxis=dict(range=[X_MIN, X_MAX], autorange=False, fixedrange=True, tickformat=".0%", tickmode="linear", tick0=0, dtick=0.2),
                yaxis=dict(range=[Y_MIN, Y_MAX], autorange=False, fixedrange=True, tickformat=".0%", tickmode="linear", tick0=-0.1, dtick=0.2),
            )

            if rr is None or rr.empty:
                fig = go.Figure()
                fig.update_layout(**LAYOUT_BASE, annotations=[dict(text="No data in selected range", x=0.5, y=0.5, xref="paper", yref="paper", showarrow=False, font=dict(size=16))])
                return fig

            rr = rr.copy()
            rr["AnnVol"] = pd.to_numeric(rr["AnnVol"], errors="coerce")
            rr["AnnReturn"] = pd.to_numeric(rr["AnnReturn"], errors="coerce")
            rr = rr.dropna(subset=["Ticker", "AnnVol", "AnnReturn"])
            rr["AnnVol"] = rr["AnnVol"].clip(X_MIN, X_MAX)
            rr["AnnReturn"] = rr["AnnReturn"].clip(Y_MIN, Y_MAX)
            rr = rr.reset_index(drop=True)

            annotations = []
            sel_rows = rr[rr["Ticker"] == hi]
            if not sel_rows.empty:
                i = sel_rows.index[0]
                annotations.append(dict(x=rr.at[i, "AnnVol"], y=rr.at[i, "AnnReturn"] + 0.035, text=rr.at[i, "Ticker"], showarrow=False, font=dict(size=13, color="white"), xanchor="center", yanchor="bottom"))

            others = rr[rr["Ticker"] != hi]
            selected = rr[rr["Ticker"] == hi]

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=others["AnnVol"], y=others["AnnReturn"], mode="markers", marker=dict(size=12, opacity=0.65, color="#4a9eff"), hovertemplate="Ticker = %{customdata}<br>Volatility = %{x:.2%}<br>Return = %{y:.2%}<extra></extra>", customdata=others["Ticker"], showlegend=False))
            if not selected.empty:
                fig.add_trace(go.Scatter(x=selected["AnnVol"], y=selected["AnnReturn"], mode="markers", marker=dict(size=18, opacity=1.0, line=dict(width=2, color="white"), color="#ff6b35"), hovertemplate="Ticker = %{customdata}<br>Volatility = %{x:.2%}<br>Return = %{y:.2%}<extra></extra>", customdata=selected["Ticker"], showlegend=False))

            fig.update_xaxes(range=[X_MIN, X_MAX], autorange=False)
            fig.update_yaxes(range=[Y_MIN, Y_MAX], autorange=False)
            fig.update_layout(
                template="plotly_dark",
                yaxis_title="Annualized Return",
                xaxis_title="Annualized Volatility",
                margin=dict(l=10, r=10, t=10, b=10),
                annotations=annotations,
                xaxis=dict(title_font=dict(size=18), tickfont=dict(size=15)),
                yaxis=dict(title_font=dict(size=18), tickfont=dict(size=15)),
            )
            return fig
