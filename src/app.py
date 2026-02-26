"""
Stock Visualization Dashboard - Magnificent 7 Portfolio
Finviz-inspired design with 8 visualization components.
"""

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_plotly

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
DATE_MIN = close_df["Date"].min()
DATE_MAX = close_df["Date"].max()

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


# -----------------------------------------------------------------------------
# Layout - 3-column grid matching sketch.png
# Row 1: 1 (Current Price), 2 (Stock Chart), 6 (Risk-Return)
# Row 2: 3 (Performance), 4 (S&P 500), 7 (Treemap)
# Row 3: 5 (Metrics Table), 8 (Watchlist)
# -----------------------------------------------------------------------------
with ui.layout_columns(col_widths=[1, 1, 1], row_heights="auto"):

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
        ui.card_header("6. Risk-Return Scatter")

        @render_plotly
        def render_risk_return_scatter():
            """
            6. Risk-Return Scatter Plot.
            Scatter plot of risk (volatility) vs return for all portfolio stocks.
            Selected stock highlighted. Reacts to: dropdown only (uses selected date range).
            Data: Calculate from close.csv; highlight selected stock.
            """
            pass
            return go.Figure()


with ui.layout_columns(col_widths=[1, 1, 1], row_heights="auto"):

    # 3. Performance Comparison
    with ui.card(full_screen=True):
        ui.card_header("3. Performance Comparison")

        @render_plotly
        def render_performance_comparison():
            """
            3. Performance Comparison.
            Multi-line chart comparing all portfolio stocks. Selected stock highlighted,
            others greyed out. Reacts to: dropdown + date range.
            Data: All portfolio stocks from close.csv.
            """
            pass
            return go.Figure()

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
            pass
            return go.Figure()

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
            pass
            return go.Figure()


with ui.layout_columns(col_widths=[1, 1], row_heights="auto"):

    # 5. Stock Metrics Table
    with ui.card():
        ui.card_header("5. Stock Metrics Table")

        @render.data_frame
        def render_stock_metrics_table():
            """
            5. Stock Metrics Table.
            Table with Stock name, P/E ratio, Revenue growth, Annual return (placeholder),
            Volatility (placeholder). Reacts to: dropdown only.
            Data: metric.csv for P/E and Revenue Growth.
            """
            pass
            return pd.DataFrame()

    # 8. Watchlist Display
    with ui.card():
        ui.card_header("8. Watchlist")
        ui.input_switch(
            "watchlist_toggle", "Show as $ (dollar) / % (percent)", value=False
        )

        @render.data_frame
        def render_watchlist():
            """
            8. Watchlist Display.
            Table of watchlist stocks (from wishlist.csv) with Symbol, Company,
            and Change (colored red/green). Global toggle for percentage vs dollar.
            Reacts to: neither dropdown nor date range.
            """
            pass
            return pd.DataFrame()


# -----------------------------------------------------------------------------
# Apply finviz-inspired styles
# -----------------------------------------------------------------------------
ui.include_css(Path(__file__).parent / "styles.css")
