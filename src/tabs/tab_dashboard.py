import numpy as np
import pandas as pd
import shiny.express as _se
from shiny import reactive
from shiny.express import expressify, ui

from data_loader import close_df, DATE_MIN, DATE_MAX
from stocks import stocks
from _input import input
from cards.card_price_chart import card_price_chart
from cards.card_portfolio import card_portfolio
from cards.card_watchlist import card_watchlist
from cards.card_performance import card_performance
from cards.card_sp500 import card_sp500
from cards.card_metrics import card_metrics
from cards.card_risk_return import card_risk_return

RR_TICKERS = [c for c in close_df.columns if c != "Date"]


@expressify
def dashboard_tab():
    # Reactive calcs are defined per-session (inside this function) so they
    # capture the real session, not the stub session at import time.
    @reactive.calc
    def get_filtered_close():
        dates = input.dates()
        mask = (close_df["Date"] >= pd.Timestamp(dates[0])) & (
            close_df["Date"] <= pd.Timestamp(dates[1])
        )
        return close_df.loc[mask].copy()

    @reactive.calc
    def analysis_close():
        d0, d1 = input.dates()
        df = (
            close_df[
                (close_df["Date"] >= pd.Timestamp(d0))
                & (close_df["Date"] <= pd.Timestamp(d1))
            ]
            .copy()
            .sort_values("Date")
        )
        if df.empty:
            return df
        period = input.rr_period()
        if period == "Full":
            return df
        years = {"1Y": 1, "5Y": 5, "10Y": 10}[period]
        cutoff = df["Date"].max() - pd.DateOffset(years=years)
        return df[df["Date"] >= cutoff].copy()

    @reactive.calc
    def risk_return_df():
        df = analysis_close()
        period = input.rr_period()
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
        out = pd.DataFrame(
            {
                "Ticker": rets.mean().index,
                "AnnReturn": rets.mean().values * 252,
                "AnnVol": rets.std().values * np.sqrt(252),
            }
        ).dropna()
        return out.reset_index(drop=True)

    with ui.nav_panel("Dashboard"):
        with ui.layout_columns(col_widths={"sm": (3, 3, 6)}, row_heights="auto"):
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
                "ticker", "Select Stock", choices=stocks, selected="AAPL"
            )
            ui.div()  # spacer

        with ui.layout_columns(col_widths={"sm": (7, 3, 2)}, row_heights="auto"):
            card_price_chart(get_filtered_close)
            card_portfolio()
            card_watchlist()

        with ui.layout_columns(col_widths={"sm": (7, 5)}, row_heights="auto"):
            card_performance(get_filtered_close)
            card_sp500(get_filtered_close)

        with ui.layout_columns(col_widths={"sm": (7, 5)}, row_heights="auto"):
            card_metrics()
            card_risk_return(risk_return_df)
