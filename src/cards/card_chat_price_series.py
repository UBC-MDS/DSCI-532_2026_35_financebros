import plotly.graph_objects as go
from shiny.express import expressify, ui
from shinywidgets import render_plotly


@expressify
def card_chat_price_series(qc):
    with ui.card(full_screen=True):
        ui.card_header("Filtered price series")

        @render_plotly
        def qc_line_chart():
            df = qc.df()
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
            if "Date" not in df.columns or len(df.columns) < 2:
                fig = go.Figure()
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#131722",
                    plot_bgcolor="#1e222d",
                    margin=dict(l=10, r=10, t=10, b=10),
                    annotations=[
                        dict(
                            text="No stock columns to plot.",
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

            fig = go.Figure()
            for col in df.columns:
                if col == "Date":
                    continue
                fig.add_trace(
                    go.Scatter(x=df["Date"], y=df[col], mode="lines", name=col)
                )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#131722",
                plot_bgcolor="#1e222d",
                margin=dict(l=10, r=10, t=30, b=10),
                hovermode="x unified",
                xaxis=dict(
                    title="Date", showgrid=True, gridcolor="rgba(255,255,255,0.06)"
                ),
                yaxis=dict(
                    title="Close Price ($)",
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.06)",
                    tickprefix="$",
                ),
                showlegend=True,
            )
            return fig
