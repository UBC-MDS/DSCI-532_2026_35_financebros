import pandas as pd
from shiny.express import expressify, render, ui

from _input import input
from data_loader import watchlist_df
from stocks import watchlist as watchlist_dict


@expressify
def card_watchlist():
    with ui.card(class_="watchlist-card"):
        ui.card_header("Watchlist & Alerts")
        ui.input_switch("watchlist_toggle", "Show %", value=False)

        @render.data_frame
        def render_watchlist():
            current_prices = watchlist_df.iloc[-1]
            previous_prices = watchlist_df.iloc[-2]

            watchlist_data = []
            for ticker in watchlist_dict.keys():
                current = current_prices[ticker]
                previous = previous_prices[ticker]
                dollar_change = current - previous
                percent_change = (dollar_change / previous) * 100
                change_value = (
                    f"{percent_change:+.2f}%"
                    if input.watchlist_toggle()
                    else f"${dollar_change:+.2f}"
                )
                watchlist_data.append({"Symbol": ticker, "Change": change_value})

            df = pd.DataFrame(watchlist_data)
            return render.DataTable(
                df,
                styles=[
                    {
                        "rows": [
                            i
                            for i, row in enumerate(watchlist_data)
                            if "-" not in row["Change"]
                        ],
                        "cols": [0, 1],
                        "style": {
                            "color": "#44bb70",
                            "font-weight": "600",
                            "background-color": "transparent",
                        },
                    },
                    {
                        "rows": [
                            i
                            for i, row in enumerate(watchlist_data)
                            if "-" in row["Change"]
                        ],
                        "cols": [0, 1],
                        "style": {
                            "color": "#d62728",
                            "font-weight": "600",
                            "background-color": "transparent",
                        },
                    },
                ],
                filters=False,
                selection_mode="none",
                height="100%",
                summary=False,
            )
