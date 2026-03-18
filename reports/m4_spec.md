# Phase 4: Finalizing the Dashboard


```mermaid
flowchart TD
  T[/input_ticker/] --> S([rr_plot])
  T --> G([render_stock_metrics_table])
  T --> TR([render_portfolio_treemap])
  T --> PC([render_performance_comparison])
  T --> SP([render_sp500_comparison])
  T --> SC([render_stock_price_chart])
  T --> CH([chat])

  D[/input_dates/] --> A{{analysis_close}}
  D --> F{{get_filtered_close}}
  D --> CH

  P[/input_rr_period/] --> A

  A --> R{{risk_return_df}}
  R --> S

  F --> PC
  F --> SP
  F --> SC

  MS[/input_metrics_sort_by/] --> G
  MD[/input_metrics_sort_dir/] --> G

  WT[/input_watchlist_toggle/] --> W([render_watchlist])

  CD[(close_df)] --> CP([render_current_price])
  CD --> CH

  MD2[(metric_df)] --> CH
  ```

## Advanced Feature Decision (Option D)

We selected **Option D: Component click event interaction** because it best fits our
dashboard's primary workflow: exploring a portfolio by clicking on a visual summary
and immediately seeing linked, detailed views update. Our Portfolio Overview treemap
is already the central entry point for exploration, so enabling click-to-select
provides a natural, low-friction way to drive all dependent charts without adding
extra UI controls. This supports faster comparison, reduces cognitive load, and
aligns with our goal of keeping the app "dashboard-first" rather than form-first. 
We found that options A–C are AI‑focused, they’re useful but secondary to the core visual workflow, also
they add value mostly to users who already know how (or want) to use the AI feature.
Additionally, we think our feature helps lower cognitive load, and enables higher discoverability as
click‑to‑select is intuitive and immediately visible in the UI.

**What we implemented**

- Added `reactive.calc` on Portfolio Overview (`card_portfolio.py`) to capture the
  clicked stock and update the shared `selected_ticker`.
- Synced the treemap click with the existing dropdown so both stay consistent.
- Connected the selection to the following charts so they react as if the stock
  was selected directly:
- Historical Closing Price Trend (`card_price_chart.py`)
- Relative Performance Comparison (`card_performance.py`)
- Price Performance vs. S&P 500 Benchmark (`card_sp500.py`)
- Risk-Return Profile (`card_risk_return.py`)

## Calculation Details

### `get_filtered_close`

**Inputs:** `input_dates`

**Transformation:**
Filters the full historical closing price dataset (`close.csv`) to only the rows within the selected date range. No further windowing is applied — this is the base filtered dataset used by the performance charts.

**Used by:** `render_performance_comparison`, `render_sp500_comparison`, `render_stock_price_chart`

---

### `analysis_close`

**Inputs:** `input_dates`, `input_rr_period`

**Transformation:**
Filters `close.csv` to the selected date range, then applies the risk/return window (`rr_period`): Full, 1Y, 5Y, or 10Y. If Full is selected, the entire filtered range is used. Otherwise, only the most recent N years within the selected range are kept. This produces the final price window used for risk and return calculations.

**Used by:** `risk_return_df`

---

### `risk_return_df`

**Inputs:** `analysis_close`

**Transformation:**
Computes daily percentage returns for each ticker from the filtered price data, then calculates annualized return (`mean_daily * 252`) and annualized volatility (`std_daily * sqrt(252)`). Outputs a summary dataframe with one row per stock.

**Used by:** `rr_plot`

---

### Outputs 

**`render_current_price`** — Reads `close_df` directly (not date-filtered). Displays the most recent closing price and day-over-day percentage change for all Magnificent 7 stocks as a Finviz-style ticker strip. Color-coded green/red/grey based on direction of change.

**`render_stock_price_chart`** — Consumes `get_filtered_close` and `input_ticker`. Plots the selected stock's closing price over the selected date range as a line chart with a range slider. Title includes the overall percentage change for the period.

**`render_performance_comparison`** — Consumes `get_filtered_close` and `input_ticker`. Normalizes all stock prices to 100 at the start of the date range and plots multi-line performance, highlighting the selected ticker.

**`render_sp500_comparison`** — Consumes `get_filtered_close`, `input_ticker`, and `input_dates`. Normalizes the selected stock and SPY to 100 and plots both lines for direct comparison.

**`render_stock_metrics_table`** — Reads `metric_df` directly. Sorts by the selected metric (`metrics_sort_by`) in the selected order (`metrics_sort_dir`) before formatting and displaying values.

**`rr_plot`** — Consumes `risk_return_df` and `input_ticker`. Renders a scatter plot of annualized volatility vs annualized return, with the selected ticker visually highlighted.

**`render_watchlist`** — Reads `wishlist_df` directly. Computes the most recent day-over-day price change per watchlist stock and displays it in dollar or percentage format based on `watchlist_toggle`, color-coded green/red.