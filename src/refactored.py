import numpy as np
import pandas as pd


def compute_risk_return(df: pd.DataFrame, period: str, tickers: list[str]) -> pd.DataFrame:
    """
    Compute annualized return and volatility for each ticker over the given period, pure func
    """
    if df.empty:
        return pd.DataFrame(columns=["Ticker", "AnnReturn", "AnnVol"])

    prices = df.set_index("Date")[tickers].astype(float)

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
