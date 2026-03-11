import numpy as np
import pandas as pd
import shiny.express as _se
from shiny import reactive

from data_loader import close_df


class _InputProxy:
    """Resolve to the current session's input at call time, not import time."""
    def __getattr__(self, name: str):
        return getattr(_se.input, name)


input = _InputProxy()

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
    period = input.rr_period()  # must be at the TOP so reactive knows to watch it

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
