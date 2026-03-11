import pandas as pd
from shiny.express import expressify, render, ui

from _input import input
from data_loader import metric_df


@expressify
def card_metrics():
    with ui.card(full_screen=True):
        ui.card_header("Fundamental Metrics Overview")

        with ui.layout_columns(col_widths=[7, 5]):
            ui.input_select(
                "metrics_sort_by",
                "Sort by",
                choices={
                    "Market Cap": "MarketCap",
                    "P/E Ratio": "P/E Ratio",
                    "Dividend Yield": "DividendYield",
                    "Revenue Growth": "Revenue Growth",
                },
                selected="MarketCap",
            )
            ui.input_radio_buttons(
                "metrics_sort_dir",
                "Order",
                choices={"desc": "Descending", "asc": "Ascending"},
                selected="desc",
                inline=True,
            )

        @render.data_frame
        def render_stock_metrics_table():
            df = metric_df.copy()
            if "Unnamed: 0" in df.columns:
                df = df.drop(columns=["Unnamed: 0"])

            sort_key = input.metrics_sort_by()
            ascending = input.metrics_sort_dir() == "asc"

            if sort_key in df.columns:
                df[sort_key] = pd.to_numeric(df[sort_key], errors="coerce")
                df = df.sort_values(sort_key, ascending=ascending, na_position="last")

            df = df.reset_index(drop=True)

            if "MarketCap" in df.columns:
                mc = pd.to_numeric(df["MarketCap"], errors="coerce") / 1_000_000_000
                df["MarketCap"] = mc.map(lambda x: "" if pd.isna(x) else f"{x:,.2f}B")
            if "P/E Ratio" in df.columns:
                pe = pd.to_numeric(df["P/E Ratio"], errors="coerce")
                df["P/E Ratio"] = pe.map(lambda x: "" if pd.isna(x) else f"{x:.2f}")
            if "DividendYield" in df.columns:
                dy = pd.to_numeric(df["DividendYield"], errors="coerce") * 100
                df["DividendYield"] = dy.map(lambda x: "" if pd.isna(x) else f"{x:.2f}%")
            if "Revenue Growth" in df.columns:
                rg = pd.to_numeric(df["Revenue Growth"], errors="coerce") * 100
                df["Revenue Growth"] = rg.map(lambda x: "" if pd.isna(x) else f"{x:.2f}%")

            return render.DataGrid(df, width="100%", height="100%", filters=False, selection_mode="rows")
