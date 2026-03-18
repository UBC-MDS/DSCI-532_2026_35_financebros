from pathlib import Path
import ibis
import pandas as pd
from dotenv import load_dotenv

DATA_DIR = Path(__file__).parent.parent / "data"
load_dotenv(DATA_DIR.parent / ".env", override=True)

# Shared DuckDB connection via ibis
con = ibis.duckdb.connect()

# Ibis table expressions (lazy)
close_tbl = con.read_parquet(str(DATA_DIR / "close.parquet"))
metric_tbl = con.read_parquet(str(DATA_DIR / "metric.parquet"))
spy_tbl = con.read_parquet(str(DATA_DIR / "spy.parquet"))
watchlist_tbl = con.read_parquet(str(DATA_DIR / "watchlist.parquet"))

# Pandas DataFrames (materialized once for cards that use .iloc, .iterrows)
close_df = close_tbl.to_pandas()
metric_df = metric_tbl.to_pandas()
spy_df = spy_tbl.to_pandas()
watchlist_df = watchlist_tbl.to_pandas()

# Date bounds
DATE_MIN = close_tbl.Date.min().execute().date()
DATE_MAX = close_tbl.Date.max().execute().date()
