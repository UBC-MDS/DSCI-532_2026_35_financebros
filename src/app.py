"""
Stock Visualization Dashboard - Magnificent 7 Portfolio
Finviz-inspired design with 8 visualization components.
"""

from pathlib import Path

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_plotly, output_widget

from stocks import stocks, wishlist as wishlist_dict

# -----------------------------------------------------------------------------
# Data Loading - Load CSV files once at startup
# -----------------------------------------------------------------------------
DATA_DIR = Path(__file__).parent.parent / "data"

close_df = pd.read_csv(DATA_DIR / "close.csv", parse_dates=["Date"])
metric_df = pd.read_csv(DATA_DIR / "metric.csv")
spy_df = pd.read_csv(DATA_DIR / "spy.csv", parse_dates=["Date"])
wishlist_df = pd.read_csv(DATA_DIR / "wishlist.csv", parse_dates=["Date"])

# Date range from close.csv
DATE_MIN = close_df["Date"].min().date()
DATE_MAX = close_df["Date"].max().date()

# -----------------------------------------------------------------------------
# Page Setup
# -----------------------------------------------------------------------------
ui.page_opts(title="Magnificent 7 Stock Explorer", fillable=True)

# -----------------------------------------------------------------------------
# Sidebar - Stock dropdown and date range
# -----------------------------------------------------------------------------
with ui.sidebar():
    ui.input_selectize(
        "ticker",
        "Select Stock",
        choices=stocks,
        selected="AAPL",
    )
    ui.input_date_range(
        "dates",
        "Select Date Range",
        start=DATE_MIN,
        end=DATE_MAX,
        min=DATE_MIN,
        max=DATE_MAX,
        format="yyyy-mm-dd",
        separator=" - ",
    )
    ui.input_select(
        "rr_period",
        "Risk/Return Window",
        choices=["Full", "1Y", "5Y", "10Y"],
        selected="Full",
    )

# -----------------------------------------------------------------------------
# Reactive Data Calculations
# -----------------------------------------------------------------------------


@reactive.calc
def get_filtered_close():
    """Filter close.csv by selected date range."""
    dates = input.dates()
    mask = (close_df["Date"] >= pd.Timestamp(dates[0])) & (
        close_df["Date"] <= pd.Timestamp(dates[1])
    )
    return close_df.loc[mask].copy()


@reactive.calc
def get_current_price():
    """Get most recent price for selected stock (from full close.csv, not date range)."""
    ticker = input.ticker()
    if ticker not in close_df.columns:
        return None
    return float(close_df[ticker].iloc[-1])


@reactive.calc
def get_selected_stock_series():
    """Get price series for selected stock within date range."""
    ticker = input.ticker()
    df = get_filtered_close()
    if ticker not in df.columns:
        return pd.Series(dtype=float)
    return df.set_index("Date")[ticker]

RR_TICKERS = [c for c in close_df.columns if c != "Date"]


def _padded_range(vals: pd.Series, pad_frac: float = 0.15):
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


@reactive.calc
def analysis_close():
    """
    Filters close.csv to selected date range, then applies rr window (Full/1Y/5Y/10Y)
    using the most recent N years inside the selected date range.
    """
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
    """
    From analysis_close(), compute annualized return + annualized volatility per ticker.
    """
    df = analysis_close()
    if df.empty:
        return pd.DataFrame(columns=["Ticker", "AnnReturn", "AnnVol"])

    prices = df.set_index("Date")[RR_TICKERS].astype(float)
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

# -----------------------------------------------------------------------------
# Layout - 3-column grid matching sketch.png
# Row 1: 1 (Current Price), 2 (Stock Chart), 6 (Risk-Return)
# Row 2: 3 (Performance), 4 (S&P 500), 7 (Treemap)
# Row 3: 5 (Metrics Table), 8 (Watchlist)
# -----------------------------------------------------------------------------
with ui.layout_columns(col_widths={"sm": (5, 5, 2)}, row_heights="auto"):

    # 1. Current Price Display
    with ui.card():
        ui.card_header("1. Current Price")

        @render.ui
        def render_current_price():
            """
            1. Current Price Display.
            Display current stock price. Reacts to dropdown only (not date range).
            Uses the most recent price from close.csv regardless of selected date range.
            Data: Last row from close.csv for selected stock.
            """
            pass
            return ui.div("—", class_="text-muted")

    # 2. Stock Price Chart
    with ui.card(full_screen=True):
        ui.card_header("2. Stock Price Chart")

        @render_plotly
        def render_stock_price_chart():
            """
            2. Stock Price Chart.
            Line graph of stock price from start to end of selected date range.
            Reacts to: dropdown + date range.
            Data: Filtered close.csv for selected stock and date range.
            """
            pass
            return go.Figure()

    # 6. Risk-Return Scatter Plot
    with ui.card(full_screen=True):
        ui.card_header("6. Risk-Return Scatshiny run --reload src/app.pyter")
        output_widget("rr_plot")

        @render_plotly
        def rr_plot():
            rr = risk_return_df()
            hi = input.ticker()

            # Empty data: still show % axes
            if rr is None or rr.empty:
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

            # Axis ranges so ALL points are always visible
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
                xaxis=dict(range=list(x_rng), tickformat=".0%", constrain="domain"),
                yaxis=dict(range=list(y_rng), tickformat=".0%", constrain="domain"),
            )
            return fig

with ui.layout_columns(col_widths={"sm": (5, 5, 2)}, row_heights="auto"):

    # 3. Performance Comparison
    with ui.card(full_screen=True):
        ui.card_header("3. Performance Comparison")

        @render_plotly
        def render_performance_comparison():
            """
            3. Performance Comparison.
            Multi-line chart comparing all portfolio stocks. Selected stock highlighted,
            others greyed out. Hovering over a point in the line will show the date, actual price at the date, and normalized value (tooltip).
            Reacts to: dropdown + date range.
            Data: All portfolio stocks from close.csv.
            """

            df = get_filtered_close().copy()
            ticker = input.ticker()

            if df.empty:
                return go.Figure()

            df = df.set_index("Date")

            raw_prices = df.copy()  # for the price/ tooltip

            # normalize to 100 at start since the raw prices arent comparable in the same graph, prices are too differentr
            normalized = df / df.iloc[0] * 100
            fig = go.Figure()

            for col in normalized.columns:

                fig.add_trace(
                    go.Scatter(
                        x=normalized.index,
                        y=normalized[col],
                        mode="lines",
                        name=col,
                        line=dict(
                            width=3 if col == ticker else 1,
                            color="green" if col == ticker else "lightgray",
                        ),
                        opacity=1 if col == ticker else 0.6,
                        # tooltip hover. I had help from chatgpt to generate the hovertemplate
                        customdata=raw_prices[col],
                        hovertemplate="<b>%{fullData.name}</b><br>"
                        + "Date: %{x|%Y-%m-%d}<br>"
                        + "Price: $%{customdata:.2f}<br>"
                        + "Performance: %{y:.2f}<extra></extra>",
                    )
                )

            # for col in normalized.columns:
            #     if col == ticker:
            #         fig.add_trace(
            #             go.Scatter(
            #                 x=normalized.index, y=normalized[col], mode="lines",
            #                 name=col, line=dict(color="green", width=3)))
            #     else:
            #         fig.add_trace(
            #             go.Scatter(
            #                 x=normalized.index, y=normalized[col], mode="lines",
            #                 name=col, line=dict(color="lightgray", width=2),
            #                 opacity=0.6))

            fig.update_layout(
                template="plotly_dark",
                yaxis_title="Normalized Performance (Base = 100)",
                xaxis_title="Date",
                showlegend=True,
                margin=dict(l=10, r=10, t=10, b=10),
            )

            return fig
            # pass
            # return go.Figure()

    # 4. S&P 500 Comparison
    with ui.card(full_screen=True):
        ui.card_header("4. S&P 500 Comparison")

        @render_plotly
        def render_sp500_comparison():
            """
            4. S&P 500 Comparison.
            Chart comparing selected stock vs SPY (S&P 500). Reacts to: dropdown + date range.
            Data: Selected stock from close.csv + SPY from spy.csv.
            """
            ticker = input.ticker()

            stock_df = get_filtered_close().copy()
            dates = input.dates()

            if stock_df.empty:
                return go.Figure()

            # filter SPY by same date range
            spy_filtered = spy_df[
                (spy_df["Date"] >= pd.Timestamp(dates[0]))
                & (spy_df["Date"] <= pd.Timestamp(dates[1]))
            ].copy()

            stock_df = stock_df.set_index("Date")
            spy_filtered = spy_filtered.set_index("Date")

            if ticker not in stock_df.columns:
                return go.Figure()

            stock_series = stock_df[ticker]
            spy_series = spy_filtered["SPY"]

            # like 3 above, normalize both to 100
            stock_norm = stock_series / stock_series.iloc[0] * 100
            spy_norm = spy_series / spy_series.iloc[0] * 100

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=stock_norm.index,
                    y=stock_norm,
                    mode="lines",
                    name=ticker,
                    line=dict(width=3),
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=spy_norm.index,
                    y=spy_norm,
                    mode="lines",
                    name="S&P 500 (SPY)",
                    line=dict(color="orange", width=2),
                )
            )

            fig.update_layout(
                template="plotly_dark",
                yaxis_title="Normalized Performance (Base = 100)",
                xaxis_title="Date",
                margin=dict(l=10, r=10, t=10, b=10),
            )

            return fig

            # pass
            # return go.Figure()

    # 7. Portfolio Treemap
    with ui.card(full_screen=True):
        ui.card_header("7. Portfolio Treemap")

        @render_plotly
        def render_portfolio_treemap():
            """
            7. Portfolio Treemap.
            Treemap of portfolio sized by market cap. Selected stock highlighted.
            Reacts to: dropdown only. Data: MarketCap from metric.csv.
            """
            selected_ticker = input.ticker()

            labels = []
            values = []
            text_info = []
            colors = []

            for _, row in metric_df.iterrows():
                ticker = str(row["Ticker"])
                company_name = stocks.get(ticker, ticker)
                labels.append(f"{ticker}")
                values.append(row["MarketCap"])
                text_info.append(f"{company_name}")

                if ticker == selected_ticker:
                    colors.append("#2962ff")
                else:
                    colors.append("#787b86")

            fig = go.Figure(
                go.Treemap(
                    labels=labels,
                    parents=[""] * len(labels),
                    values=values,
                    text=text_info,
                    textposition="middle center",
                    marker=dict(colors=colors, line=dict(color="#2a2e39", width=2)),
                    hovertemplate="<b>%{label}</b><br>%{text}<br>Market Cap: $%{value:,.0f}<extra></extra>",
                )
            )

            fig.update_layout(
                paper_bgcolor="#131722",
                plot_bgcolor="#1e222d",
                font=dict(color="#d1d4dc", size=14),
                margin=dict(l=10, r=10, t=10, b=10),
            )

            return fig


with ui.layout_columns(col_widths={"sm": (10, 2)}, row_heights="auto"):

    # 5. Stock Metrics Table
    with ui.card(style="width: 100%; height: 360px;"):
        ui.card_header("5. Stock Metrics Table")

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
                choices={"desc": "Desc", "asc": "Asc"},
                selected="desc",
                inline=True,
            )

        @render.data_frame
        def render_stock_metrics_table():
            df = metric_df.copy()

            if "Unnamed: 0" in df.columns:
                df = df.drop(columns=["Unnamed: 0"])

            sort_key = input.metrics_sort_by()
            ascending = (input.metrics_sort_dir() == "asc")

            sort_df = df.copy()
            for col in ["MarketCap", "P/E Ratio", "DividendYield", "Revenue Growth"]:
                if col in sort_df.columns:
                    sort_df[col] = pd.to_numeric(sort_df[col], errors="coerce")

            if sort_key in sort_df.columns:
                df["_sort_"] = sort_df[sort_key]
                df = df.sort_values("_sort_", ascending=ascending, na_position="last").drop(columns=["_sort_"])

            df = df.reset_index(drop=True)

            # formatting for display
            if "MarketCap" in df.columns:
                mc = pd.to_numeric(df["MarketCap"], errors="coerce") / 1_000_000_000
                df["MarketCap"] = mc.map(lambda x: "" if pd.isna(x) else f"{x:,.2f}B")

            if "P/E Ratio" in df.columns:
                pe = pd.to_numeric(df["P/E Ratio"], errors="coerce")
                df["P/E Ratio"] = pe.map(lambda x: "" if pd.isna(x) else f"{x:.3f}")

            if "DividendYield" in df.columns:
                dy = pd.to_numeric(df["DividendYield"], errors="coerce") * 100
                df["DividendYield"] = dy.map(lambda x: "" if pd.isna(x) else f"{x:.3f}%")

            if "Revenue Growth" in df.columns:
                rg = pd.to_numeric(df["Revenue Growth"], errors="coerce") * 100
                df["Revenue Growth"] = rg.map(lambda x: "" if pd.isna(x) else f"{x:.3f}%")

            return render.DataGrid(
                df,
                width="100%",
                height="260px",
                selection_mode="rows",
            )

    # 8. Watchlist Display
    with ui.card():
        ui.card_header("8. Watchlist")
        ui.input_switch("watchlist_toggle", "Show as $ or %", value=False)

        @render.data_frame
        def render_watchlist():
            """
            8. Watchlist Display.
            Table of watchlist stocks (from wishlist.csv) with Symbol, Company,
            and Change (colored red/green). Global toggle for percentage vs dollar.
            Reacts to: neither dropdown nor date range.
            """
            current_prices = wishlist_df.iloc[-1]
            previous_prices = wishlist_df.iloc[-2]

            watchlist_data = []
            for ticker in wishlist_dict.keys():
                current = current_prices[ticker]
                previous = previous_prices[ticker]
                dollar_change = current - previous
                percent_change = (dollar_change / previous) * 100

                if input.watchlist_toggle():
                    change_value = f"{percent_change:+.2f}%"
                else:
                    change_value = f"${dollar_change:+.2f}"

                watchlist_data.append(
                    {
                        "Symbol": ticker,
                        "Change": change_value,
                    }
                )

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
            )


# -----------------------------------------------------------------------------
# Apply finviz-inspired styles
# -----------------------------------------------------------------------------
# ui.include_css(Path(__file__).parent / "styles.css")
