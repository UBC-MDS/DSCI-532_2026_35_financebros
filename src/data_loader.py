from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

DATA_DIR = Path(__file__).parent.parent / "data"

load_dotenv(DATA_DIR.parent / ".env", override=True)

close_df = pd.read_csv(DATA_DIR / "close.csv", parse_dates=["Date"])
metric_df = pd.read_csv(DATA_DIR / "metric.csv")
spy_df = pd.read_csv(DATA_DIR / "spy.csv", parse_dates=["Date"])
watchlist_df = pd.read_csv(DATA_DIR / "watchlist.csv", parse_dates=["Date"])

DATE_MIN = close_df["Date"].min().date()
DATE_MAX = close_df["Date"].max().date()
