# Phase 2: App Specification (M2)

This document is a specification for our Shiny dashboard. It will be updated in M3 and M4 as the implementation evolves.

## 2.1 Updated Job Stories

| # | Job Story | Status | Notes |
|---:|---|:---:|---|
| 1 | When I want to compare Magnificent 7 companies, I want to view their key valuation and growth metrics side-by-side so I can quickly rank and evaluate them. | ⏳ Pending M3 | Focus: sortable table with selected ticker highlighted. |
| 2 | When I analyze investment tradeoffs, I want to see a risk vs return scatter plot so I can understand how volatility relates to performance across companies. | ⏳ Pending M3 | Hover tooltip should display ticker, return, and volatility. |

---

## 2.2 Component Inventory

This inventory is our implementation checklist for Phase 3+ (inputs → reactive calcs → outputs).

| ID | Type | Shiny widget / renderer | Depends on | Job story |
|---|---|---|---|---|
| `input_ticker` | Input | `ui.input_select()` | — | #1, #2 |
| `input_dates` | Input | `ui.input_date_range()` | — | #2 |
| `input_rr_period` | Input | `ui.input_select()` (Full, 1Y, 5Y, 10Y) | — | #2 |
| `analysis_close` | Reactive calc | `@reactive.calc` | `input_dates`, `input_rr_period` | #2 |
| `risk_return_df` | Reactive calc | `@reactive.calc` | `analysis_close` | #2 |
| `metrics_table_df` | Reactive calc | `@reactive.calc` | — | #1 |
| `tbl_stock_metrics` | Output | `@render.data_frame` / `render.DataGrid` | `metrics_table_df`, `input_ticker` | #1 |
| `plot_risk_return` | Output | `@render_plotly` → `go.Figure()` | `risk_return_df`, `input_ticker` | #2 |

---

### Risk & Valuation Metrics Table (Bottom-Left)

- Displays all 7 Magnificent stocks as rows.
- Columns include:
  - Ticker  
  - Date (latest available per ticker)  
  - Market Cap  
  - P/E Ratio  
  - Dividend Yield  
  - Revenue Growth  

**Behavior:**
- Table always shows the full 7-row dataset.
- The row matching `input_ticker` is visually highlighted.
- Table supports column sorting the stock based on selected metrics.
- Fundamental metrics are snapshot values and do not change with date range because it always shows the latest value.

---

### Risk vs Return Scatter Plot (Top-Right)

- Displays all 7 stocks as points.
- X-axis: Annualized Volatility (Risk)
- Y-axis: Annualized Return
- Values are computed from historical closing price data.

**Behavior:**
- `input_dates` sets the overall available date range.
- `input_rr_period` chooses the calculation window used within the selected range:
  - **Full**: use the entire selected date range
  - **1Y**: use the most recent 1 year within the selected range
  - **5Y**: use the most recent 5 years within the selected range
  - **10Y**: use the most recent 10 years within the selected range (if available)
- Hover tooltip displays:
  - Ticker
  - Annualized Return (%)
  - Volatility (%)
- The selected ticker (`input_ticker`) is visually emphasized (larger marker or distinct color).
---

## 2.3 Reactivity Diagram

```mermaid
flowchart TD
  D[/input_dates/] --> A{{analysis_close}}
  P[/input_rr_period/] --> A{{analysis_close}}

  A --> R{{risk_return_df}}
  R --> S([plot_risk_return])

  T[/input_ticker/] --> S
  M{{metrics_table_df}} --> G([tbl_stock_metrics])
  T --> G
```