import plotly.graph_objects as go
from shiny import reactive
from shiny.express import expressify, ui
from shinywidgets import render_plotly, reactive_read

from _input import input
from data_loader import close_df, metric_df


@expressify
def card_portfolio(selected_ticker, _ticker_source):
    with ui.card(class_="portfolio-card"):
        ui.card_header("Portfolio Overview")

        @render_plotly
        def render_current_price():
            ticker = selected_ticker()
            cur = close_df.iloc[-1]
            prev = close_df.iloc[-2]

            GREEN = "#44bb70"
            RED = "#d62728"
            GRAY = "#787b86"
            DIM_OPACITY = 0.45

            labels, values, text_info, colors, customdata_list = [], [], [], [], []

            for _, row in metric_df.iterrows():
                t = str(row["Ticker"])
                if t not in close_df.columns:
                    continue
                market_cap = row["MarketCap"]
                current = float(cur[t])
                previous = float(prev[t])
                pct = 0.0 if previous == 0 else (current / previous - 1.0) * 100

                if pct > 0.05:
                    base_color, arrow = GREEN, "▲"
                elif pct < -0.05:
                    base_color, arrow = RED, "▼"
                else:
                    base_color, arrow = GRAY, "•"

                if t == ticker:
                    colors.append(base_color)
                else:
                    r, g, b = (
                        int(base_color[1:3], 16),
                        int(base_color[3:5], 16),
                        int(base_color[5:7], 16),
                    )
                    colors.append(f"rgba({r},{g},{b},{DIM_OPACITY})")

                labels.append(t)
                values.append(market_cap)
                text_info.append(f"${current:,.2f} {arrow}{pct:.2f}%")
                customdata_list.append([current, pct])

            fig = go.FigureWidget(  # ← FigureWidget instead of Figure
                go.Treemap(
                    labels=labels,
                    parents=[""] * len(labels),
                    values=values,
                    text=text_info,
                    textposition="middle center",
                    customdata=customdata_list,
                    marker=dict(colors=colors, line=dict(color="#2a2e39", width=2)),
                    hovertemplate="<b>%{label}</b><br>Price: $%{customdata[0]:,.2f}<br>Change: %{customdata[1]:+.2f}%<br>Market Cap: $%{value:,.0f}<extra></extra>",
                )
            )
            fig.update_layout(
                paper_bgcolor="#131722",
                plot_bgcolor="#1e222d",
                font=dict(color="#d1d4dc", size=16),
                margin=dict(l=10, r=10, t=10, b=10),
            )

            # ── Register click handler directly on the FigureWidget ──────────
            def _handle_click(trace, points, state):
                if points.point_inds:
                    clicked = labels[points.point_inds[0]]
                    selected_ticker.set(clicked)  # ← only this, no update_selectize

            fig.data[0].on_click(_handle_click)
            return fig

        # ── No longer need the reactive.effect — handler is on the widget ────