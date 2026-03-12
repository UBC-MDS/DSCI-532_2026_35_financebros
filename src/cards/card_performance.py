import plotly.graph_objects as go
from shiny.express import expressify, ui
from shinywidgets import render_plotly


@expressify
def card_performance(get_filtered_close, get_normalized_close, selected_ticker):
    with ui.card(full_screen=True):
        ui.card_header("Relative Performance Comparison")

        @render_plotly
        def render_performance_comparison():
            ticker = selected_ticker()
            normalized = get_normalized_close()  # ← cached, not recomputed
            raw_prices = get_filtered_close().set_index("Date")

            if normalized.empty:
                return go.Figure()

            fig = go.Figure()
            for col in normalized.columns:
                fig.add_trace(
                    go.Scatter(
                        x=normalized.index,
                        y=normalized[col],
                        mode="lines",
                        name=col,
                        line=dict(width=3 if col == ticker else 1, color="green" if col == ticker else "lightgray"),
                        opacity=1 if col == ticker else 0.6,
                        customdata=raw_prices[col],
                        hovertemplate=(
                            "<b>%{fullData.name}</b><br>"
                            "Date: %{x|%Y-%m-%d}<br>"
                            "Price: $%{customdata:.2f}<br>"
                            "Performance: %{y:.2f}<extra></extra>"
                        ),
                    )
                )
            fig.update_layout(
                template="plotly_dark",
                yaxis_title="Normalized Performance (Base = 100)",
                xaxis_title="Date",
                showlegend=True,
                margin=dict(l=10, r=10, t=10, b=10),
            )
            return fig