import pandas as pd

from refactored import compute_risk_return


def test_compute_risk_return_basic():
    """Verifies annualized return and volatility calculations so risk-return charts remain correct."""
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03"]),
            "AAPL": [100, 110, 121],  # 10% daily twice -> mean 0.10, std 0
        }
    )

    out = compute_risk_return(df, "Full", ["AAPL"])
    row = out.iloc[0]

    assert row["Ticker"] == "AAPL"
    assert round(row["AnnReturn"], 6) == round(0.10 * 252, 6)
    assert round(row["AnnVol"], 6) == 0.0
