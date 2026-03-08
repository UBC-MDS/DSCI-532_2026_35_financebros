"""
Magnificent 7 · Portfolio Intelligence Dashboard
"""

from pathlib import Path

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_plotly, output_widget
from querychat.express import QueryChat
import chatlas as clt
from dotenv import load_dotenv
import io

from stocks import stocks, watchlist as watchlist_dict

# -----------------------------------------------------------------------------
# Data Loading - Load CSV files once at startup
# -----------------------------------------------------------------------------
DATA_DIR = Path(__file__).parent.parent / "data"

load_dotenv(DATA_DIR.parent / ".env", override=True)

close_df = pd.read_csv(DATA_DIR / "close.csv", parse_dates=["Date"])
metric_df = pd.read_csv(DATA_DIR / "metric.csv")
spy_df = pd.read_csv(DATA_DIR / "spy.csv", parse_dates=["Date"])
watchlist_df = pd.read_csv(DATA_DIR / "watchlist.csv", parse_dates=["Date"])

# Date range from close.csv
DATE_MIN = close_df["Date"].min().date()
DATE_MAX = close_df["Date"].max().date()

# -----------------------------------------------------------------------------
# Page Setup
# -----------------------------------------------------------------------------
ui.page_opts(title="Magnificent 7 Stock Explorer", fillable=True)

ui.tags.style(
    """
/* Finviz-style strip */
.tickerstrip {
  display: flex;
  align-items: stretch;
  border: 1px solid #2a2e39;
  border-radius: 10px;
  overflow: hidden;             /* makes separators look clean */
  background: #1e222d;
}

/* Each tile */
.tickerbox {
  flex: 1;
  padding: 10px 10px 8px 10px;
  min-width: 0;
  text-align: left;
}

/* Thin vertical separators between boxes */
.tickerbox + .tickerbox {
  border-left: 1px solid #2a2e39;
}

.tickerbox-ticker {
  font-weight: 700;
  font-size: 12px;
  letter-spacing: 0.04em;
  color: #d1d4dc;
  text-transform: uppercase;
  margin-bottom: 4px;
}

/* Price row */
.tickerbox-price {
  font-weight: 700;
  font-size: 16px;
  color: #ffffff;
  line-height: 1.1;
}

/* Return row */
.tickerbox-ret {
  margin-top: 4px;
  font-weight: 600;
  font-size: 12px;
  line-height: 1.1;
  display: inline-flex;
  gap: 6px;
  align-items: center;
}

.ret-pos { color: #44bb70; }
.ret-neg { color: #d62728; }
.ret-flat { color: #9aa0a6; }

/* Arrow style */
.ret-arrow {
  font-size: 12px;
  opacity: 0.95;
}

/* Subtle hover like finviz */
.tickerbox:hover {
  background: #232a37;
}

/* Small screens: allow horizontal scroll instead of wrapping */
@media (max-width: 900px) {
  .tickerstrip {
    overflow-x: auto;
  }
  .tickerbox {
    flex: 0 0 140px;
  }
}

/* Fix DataGrid hover in dark mode */
.shiny-data-grid table tbody tr:hover {
    background-color: #2a3a4a !important;
    color: #ffffff !important;
}

.shiny-data-grid table tbody tr:hover td {
    background-color: #2a3a4a !important;
    color: #ffffff !important;
}

/* Override any inline or inherited styles */
[data-row]:hover {
    background-color: #2a3a4a !important;
    color: #ffffff !important;
}

/* Card header title - modest size so UI doesn't feel oversized */
.card-header {
    font-size: 1rem !important;
}

/* Labels and controls - standard readable size */
label[for="metrics_sort_by"],
label[for="metrics_sort_dir"] {
    font-size: 0.875rem !important;
}

/* Sort by - regular select input */
#metrics_sort_by {
    font-size: 0.875rem !important;
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #cccccc !important;
}

.selectize-control .selectize-dropdown {
    font-size: 0.875rem !important;
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* Descending/Ascending radio buttons */
#metrics_sort_dir label {
    font-size: 0.875rem !important;
}

/* Table cell values and headers */
.shiny-data-grid table td,
.shiny-data-grid table th {
    font-size: 0.8125rem !important;
}

/* Risk-Return period dropdown */
#rr_period + .selectize-control .selectize-input {
    font-size: 0.875rem !important;
}

#rr_period + .selectize-control .selectize-dropdown {
    font-size: 0.875rem !important;
}

/* QueryChat table: disable hover highlight */
.shiny-data-grid .rt-tr:hover,
.shiny-data-grid .data-grid-row:hover,
.shiny-data-frame table tbody tr:hover,
.shiny-data-frame .rt-tr:hover {
  background-color: transparent !important;
}

/* ShinyChat: dark theme overrides */
.shinychat-chat,
.shinychat,
.shinychat-container {
  background: #131722 !important;
  color: #d1d4dc !important;
}

.shinychat-chat .card,
.shinychat .card {
  background: #1e222d !important;
  border: 1px solid #2a2e39 !important;
}

.shinychat-message,
.shinychat-message * {
  color: #d1d4dc !important;
}

.shinychat-input,
.shinychat-input textarea,
.shinychat-input input,
.shinychat textarea,
.shinychat input {
  background: #1e222d !important;
  color: #d1d4dc !important;
  border: 1px solid #2a2e39 !important;
}

.shinychat .btn,
.shinychat-chat .btn {
  border-color: #2a2e39 !important;
}

/* Sidebar: force light text in dark mode */
.bslib-sidebar-layout .sidebar,
.bslib-sidebar-layout .sidebar * {
  color: #d1d4dc !important;
}

.bslib-sidebar-layout .sidebar label,
.bslib-sidebar-layout .sidebar .control-label,
.bslib-sidebar-layout .sidebar .shiny-input-container label {
  color: #d1d4dc !important;
}

.bslib-sidebar-layout .sidebar .form-control,
.bslib-sidebar-layout .sidebar select,
.bslib-sidebar-layout .sidebar textarea,
.bslib-sidebar-layout .sidebar input {
  background-color: #1e222d !important;
  color: #d1d4dc !important;
  border: 1px solid #2a2e39 !important;
}

.bslib-sidebar-layout > .sidebar {
  background-color: #131722 !important;
}
"""
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
        (close_df["Date"] >= pd.Timestamp(d0)) & (close_df["Date"] <= pd.Timestamp(d1))
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
    df = analysis_close()
    period = input.rr_period()  # ← must be at the TOP so reactive knows to watch it

    if df.empty:
        return pd.DataFrame(columns=["Ticker", "AnnReturn", "AnnVol"])

    prices = df.set_index("Date")[RR_TICKERS].astype(float)

    if period != "Full":
        years = int(period.replace("Y", ""))
        cutoff = pd.Timestamp.today() - pd.DateOffset(years=years)
        prices = prices[prices.index >= cutoff]

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
with ui.navset_tab(id="main_tabs"):

    with ui.nav_panel("Dashboard"):

        # -----------------------------------------------------------------------------
        # Sidebar - Stock dropdown and date range (app2: dates + ticker only)
        # -----------------------------------------------------------------------------
        with ui.layout_sidebar():
            with ui.sidebar():
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

                ui.input_selectize(
                    "ticker",
                    "Select Stock",
                    choices=stocks,
                    selected="AAPL",
                )

            with ui.layout_columns(col_widths={"sm": (7, 3, 2)}, row_heights="auto"):

                # 1. Stock Price Chart (app2)
                with ui.card(full_screen=True):
                    ui.card_header("Historical Closing Price Trend")

                    @render_plotly
                    def render_stock_price_chart():
                        """
                        1. Stock Price Chart.
                        Line graph of stock price from start to end of selected date range.
                        Reacts to: dropdown + date range.
                        Data: Filtered close.csv for selected stock and date range.
                        """
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
                        pct_change = (
                            (end_price / start_price - 1) * 100 if start_price != 0 else 0.0
                        )
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

                # 2. Current Price + Portfolio Treemap (app2 combined)
                with ui.card():
                    ui.card_header("Portfolio Overview")

                    @render_plotly
                    def render_current_price():
                        """
                        Combined: Market cap treemap with current price and day-over-day change.
                        Green = price up, red = price down. Selected ticker highlighted (full contrast),
                        others dimmed. Reacts to dropdown only.
                        """
                        selected_ticker = input.ticker()
                        cur = close_df.iloc[-1]
                        prev = close_df.iloc[-2]

                        GREEN = "#44bb70"
                        RED = "#d62728"
                        GRAY = "#787b86"
                        DIM_OPACITY = 0.45

                        labels = []
                        values = []
                        text_info = []
                        colors = []
                        customdata_list = []

                        for _, row in metric_df.iterrows():
                            ticker = str(row["Ticker"])
                            if ticker not in close_df.columns:
                                continue
                            market_cap = row["MarketCap"]
                            current = float(cur[ticker])
                            previous = float(prev[ticker])
                            pct = 0.0 if previous == 0 else (current / previous - 1.0) * 100

                            if pct > 0.05:
                                base_color = GREEN
                                arrow = "▲"
                            elif pct < -0.05:
                                base_color = RED
                                arrow = "▼"
                            else:
                                base_color = GRAY
                                arrow = "•"

                            is_selected = ticker == selected_ticker
                            if is_selected:
                                colors.append(base_color)
                            else:
                                r, g, b = (
                                    int(base_color[1:3], 16),
                                    int(base_color[3:5], 16),
                                    int(base_color[5:7], 16),
                                )
                                colors.append(f"rgba({r},{g},{b},{DIM_OPACITY})")

                            labels.append(ticker)
                            values.append(market_cap)
                            price_change_txt = f"${current:,.2f} {arrow}{pct:.2f}%"
                            text_info.append(price_change_txt)
                            customdata_list.append([current, pct])

                        fig = go.Figure(
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
                            font=dict(color="#d1d4dc", size=14),
                            margin=dict(l=10, r=10, t=10, b=10),
                        )
                        return fig

                # 3. Watchlist Display (app2)
                with ui.card():
                    ui.card_header("Watchlist & Alerts")
                    ui.input_switch("watchlist_toggle", "Show as $ or %", value=False)

                    @render.data_frame
                    def render_watchlist():
                        """
                        3. Watchlist Display.
                        Table of watchlist stocks (from watchlist.csv) with Symbol, Company,
                        and Change (colored red/green). Global toggle for percentage vs dollar.
                        Reacts to: neither dropdown nor date range.
                        """
                        current_prices = watchlist_df.iloc[-1]
                        previous_prices = watchlist_df.iloc[-2]

                        watchlist_data = []
                        for ticker in watchlist_dict.keys():
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

            with ui.layout_columns(col_widths={"sm": (7, 5)}, row_heights="auto"):

                # 3. Performance Comparison (app2)
                with ui.card(full_screen=True):
                    ui.card_header("Relative Performance Comparison")

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

                # 4. S&P 500 Comparison (app2)
                with ui.card(full_screen=True):
                    ui.card_header("Price Performance vs. S&P 500 Benchmark")

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

            with ui.layout_columns(col_widths={"sm": (7, 5)}, row_heights="auto"):

                # 5. Stock Metrics Table (app2)
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

                        # Sort BEFORE formatting on numeric values
                        if sort_key in df.columns:
                            df[sort_key] = pd.to_numeric(df[sort_key], errors="coerce")
                            df = df.sort_values(
                                sort_key, ascending=ascending, na_position="last"
                            )

                        df = df.reset_index(drop=True)

                        # Format AFTER sorting
                        if "MarketCap" in df.columns:
                            mc = (
                                pd.to_numeric(df["MarketCap"], errors="coerce")
                                / 1_000_000_000
                            )
                            df["MarketCap"] = mc.map(
                                lambda x: "" if pd.isna(x) else f"{x:,.2f}B"
                            )

                        if "P/E Ratio" in df.columns:
                            pe = pd.to_numeric(df["P/E Ratio"], errors="coerce")
                            df["P/E Ratio"] = pe.map(
                                lambda x: "" if pd.isna(x) else f"{x:.2f}"
                            )

                        if "DividendYield" in df.columns:
                            dy = (
                                pd.to_numeric(df["DividendYield"], errors="coerce")
                                * 100
                            )
                            df["DividendYield"] = dy.map(
                                lambda x: "" if pd.isna(x) else f"{x:.2f}%"
                            )

                        if "Revenue Growth" in df.columns:
                            rg = (
                                pd.to_numeric(df["Revenue Growth"], errors="coerce")
                                * 100
                            )
                            df["Revenue Growth"] = rg.map(
                                lambda x: "" if pd.isna(x) else f"{x:.2f}%"
                            )

                        return render.DataGrid(
                            df,
                            width="100%",
                            height="100%",
                            filters=False,
                            selection_mode="rows",
                        )

                # 6. Risk-Return Scatter Plot (app2: rr_period in card header)
                with ui.card(full_screen=True):
                    with ui.card_header():
                        ui.div(
                            ui.div("Risk-Return Profile", style="font-weight:700;"),
                            ui.input_selectize(
                                "rr_period",
                                None,
                                choices=["Full", "1Y", "5Y", "10Y"],
                                selected="Full",
                            ),
                            style="display:flex; justify-content:space-between; align-items:center; width:100%;",
                        )

                    @render_plotly
                    def rr_plot():
                        """
                        6. Risk-Return Scatter Plot.
                        Scatter plot of risk (volatility) vs return for all portfolio stocks.
                        Selected stock highlighted. Reacts to: dropdown only (uses selected date range).
                        Data: Calculate from close.csv; highlight selected stock.
                        """
                        rr = risk_return_df()
                        hi = input.ticker()

                        X_MIN, X_MAX = 0.0, 1.0
                        Y_MIN, Y_MAX = -0.10, 1.0

                        LAYOUT_BASE = dict(
                            template="plotly_dark",
                            #height=520,
                            autosize=True,
                            margin=dict(l=60, r=30, t=20, b=60),
                            xaxis_title="Annualized Volatility",
                            yaxis_title="Annualized Return",
                            xaxis=dict(
                                range=[X_MIN, X_MAX],
                                autorange=False,
                                fixedrange=True,
                                tickformat=".0%",
                                tickmode="linear",
                                tick0=0,
                                dtick=0.2,
                            ),
                            yaxis=dict(
                                range=[Y_MIN, Y_MAX],
                                autorange=False,
                                fixedrange=True,
                                tickformat=".0%",
                                tickmode="linear",
                                tick0=-0.1,
                                dtick=0.2,
                            ),
                        )

                        if rr is None or rr.empty:
                            fig = go.Figure()
                            fig.update_layout(
                                **LAYOUT_BASE,
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

                        rr = rr.copy()
                        rr["AnnVol"] = pd.to_numeric(rr["AnnVol"], errors="coerce")
                        rr["AnnReturn"] = pd.to_numeric(rr["AnnReturn"], errors="coerce")
                        rr = rr.dropna(subset=["Ticker", "AnnVol", "AnnReturn"])
                        rr["AnnVol"] = rr["AnnVol"].clip(X_MIN, X_MAX)
                        rr["AnnReturn"] = rr["AnnReturn"].clip(Y_MIN, Y_MAX)
                        rr = rr.reset_index(drop=True)

                        # Label only the selected stock (app2)
                        annotations = []
                        sel_rows = rr[rr["Ticker"] == hi]
                        if not sel_rows.empty:
                            i = sel_rows.index[0]
                            annotations.append(
                                dict(
                                    x=rr.at[i, "AnnVol"],
                                    y=rr.at[i, "AnnReturn"] + 0.035,
                                    text=rr.at[i, "Ticker"],
                                    showarrow=False,
                                    font=dict(size=13, color="white"),
                                    xanchor="center",
                                    yanchor="bottom",
                                )
                            )

                        others = rr[rr["Ticker"] != hi]
                        selected = rr[rr["Ticker"] == hi]

                        fig = go.Figure()

                        fig.add_trace(
                            go.Scatter(
                                x=others["AnnVol"],
                                y=others["AnnReturn"],
                                mode="markers",
                                marker=dict(size=12, opacity=0.65, color="#4a9eff"),
                                hovertemplate="Ticker = %{customdata}<br>Volatility = %{x:.2%}<br>Return = %{y:.2%}<extra></extra>",
                                customdata=others["Ticker"],
                                showlegend=False,
                            )
                        )

                        if not selected.empty:
                            fig.add_trace(
                                go.Scatter(
                                    x=selected["AnnVol"],
                                    y=selected["AnnReturn"],
                                    mode="markers",
                                    marker=dict(
                                        size=18,
                                        opacity=1.0,
                                        line=dict(width=2, color="white"),
                                        color="#ff6b35",
                                    ),
                                    hovertemplate="Ticker = %{customdata}<br>Volatility = %{x:.2%}<br>Return = %{y:.2%}<extra></extra>",
                                    customdata=selected["Ticker"],
                                    showlegend=False,
                                )
                            )

                        fig.update_xaxes(range=[X_MIN, X_MAX], autorange=False)
                        fig.update_yaxes(range=[Y_MIN, Y_MAX], autorange=False)
                        fig.update_layout(
                            template="plotly_dark",
                            yaxis_title="Annualized Return",
                            xaxis_title="Annualized Volatility",
                            margin=dict(l=10, r=10, t=10, b=10),
                            annotations=annotations,
                            xaxis=dict(
                                title_font=dict(size=18),
                                tickfont=dict(size=15),
                            ),
                            yaxis=dict(
                                title_font=dict(size=18),
                                tickfont=dict(size=15),
                            ),
                        )
                        return fig

    with ui.nav_panel("Chat"):
        ui.markdown(
            """
            ## Finance Bros Chat

            Ask questions like:
            - "Show only dates after 2021"
            - "Filter to AAPL and MSFT"
            - "Sort by NVDA descending"

            The chat generates SQL to filter/sort the dataset, and the table below updates reactively.
            """
        )

        qc_data = close_df.copy()

        qc = QueryChat(
            qc_data,
            "stocks",
            client=clt.ChatAnthropic(model="claude-sonnet-4-0"),
            greeting=(
                "Hello! I am your Finance Bros assistant. And I am at your service. Let me know how I can help you explore the stock data."
            ),
        )

        with ui.layout_sidebar():
            with ui.sidebar():
                ui.tags.div(
                    {
                        "style": "height: 400px; overflow-y: auto; display: flex; flex-direction: column;"
                    },
                    qc.ui(),
                )
                ui.hr()
                ui.input_action_button("qc_reset", "Reset", class_="w-100")
                ui.hr()
                ui.input_action_button(
                    "qc_dl_filtered", "Download filtered CSV", class_="w-100"
                )

            with ui.card(full_screen=True):
                ui.card_header("Filtered table")

                @render.text
                def qc_title():
                    return qc.title() or "Stocks dataset"

                @render.data_frame
                def qc_table():
                    return qc.df()

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
                            go.Scatter(
                                x=df["Date"],
                                y=df[col],
                                mode="lines",
                                name=col,
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

            with ui.card(full_screen=True):
                ui.card_header("Correlation heatmap (returns)")

                @render_plotly
                def qc_box_plot():
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

                    # Use returns for correlation
                    tickers = [c for c in df.columns if c != "Date"]
                    prices = df[tickers].apply(pd.to_numeric, errors="coerce")
                    rets = prices.pct_change().dropna(how="all")

                    # Drop columns with too little data
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

        @reactive.effect
        @reactive.event(input.qc_dl_filtered)
        def _download_csv():
            df = qc.df()
            if df is None:
                df = pd.DataFrame()
            csv_str = df.to_csv(index=False)
            # base64-encode and trigger browser download via JS
            import base64

            b64 = base64.b64encode(csv_str.encode()).decode()
            ui.insert_ui(
                ui.tags.script(
                    f"""
                    (function() {{
                        const a = document.createElement('a');
                        a.href = 'data:text/csv;base64,{b64}';
                        a.download = 'filtered_stocks_wide.csv';
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                    }})();
                """
                ),
                selector="body",
                where="beforeEnd",
            )

        @reactive.effect
        @reactive.event(input.qc_reset)
        def _qc_reset_effect():
            qc.sql("SELECT * FROM stocks")


# -----------------------------------------------------------------------------
# Apply finviz-inspired styles
# -----------------------------------------------------------------------------
ui.include_css(Path(__file__).parent / "styles.css")
