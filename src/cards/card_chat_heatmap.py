import pandas as pd
import plotly.graph_objects as go
from shiny.express import expressify, ui
from shinywidgets import render_plotly


@expressify
def card_chat_heatmap(qc):
    with ui.card(full_screen=True):
        ui.card_header("Correlation heatmap (returns)")

        @render_plotly
        def qc_box_plot():
            _raw = qc.df()
            df = _raw.execute() if hasattr(_raw, "execute") else _raw
            if df is None or df.empty:
                fig = go.Figure()
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#131722",
                    plot_bgcolor="#1e222d",
                    margin=dict(l=10, r=10, t=10, b=10),
                    annotations=[
                        dict(
                            text="No data available for the current filter.",
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

            df = df.copy()
            if "Date" not in df.columns or len(df.columns) < 3:
                fig = go.Figure()
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#131722",
                    plot_bgcolor="#1e222d",
                    margin=dict(l=10, r=10, t=10, b=10),
                    annotations=[
                        dict(
                            text="Need at least two ticker columns to compute correlation.",
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

            tickers = [c for c in df.columns if c != "Date"]
            prices = df[tickers].apply(pd.to_numeric, errors="coerce")
            rets = prices.pct_change().dropna(how="all")
            rets = rets.dropna(axis=1, thresh=max(2, int(0.5 * len(rets))))

            if rets.shape[1] < 2:
                fig = go.Figure()
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#131722",
                    plot_bgcolor="#1e222d",
                    margin=dict(l=10, r=10, t=10, b=10),
                    annotations=[
                        dict(
                            text="Not enough valid return series to compute correlation.",
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

            corr = rets.corr()
            fig = go.Figure(
                data=go.Heatmap(
                    z=corr.values,
                    x=corr.columns.tolist(),
                    y=corr.index.tolist(),
                    zmin=-1,
                    zmax=1,
                    hovertemplate="%{y} vs %{x}<br>corr=%{z:.2f}<extra></extra>",
                )
            )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#131722",
                plot_bgcolor="#1e222d",
                margin=dict(l=10, r=10, t=30, b=10),
                xaxis=dict(tickangle=45),
                yaxis=dict(autorange="reversed"),
            )
            return fig
