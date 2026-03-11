# DSCI-532_2026_35_financebros
Dashboard for stonks

## Live Demo

- **Stable:** https://019c96fb-7645-b17f-61b0-46a58d974625.share.connect.posit.cloud/
- **Preview:** https://019c96fc-ef4e-2932-2355-311a3030aeb5.share.connect.posit.cloud/

## About

The financebros dashboard is a web application that tracks key financial metrics regarding a portfolio comprised of the Magnificent Seven stocks: Apple, Microsoft, Amazon, Alphabet (Google’s parent company), Meta, Nvidia, and Tesla. The dashboard provides users with insights into the performance of these stocks, including price trends, volatility, and other relevant financial indicators. It also compares the performance of the portfolio against the S&P 500 index.
## Demo

<details open>
<summary>Click to close app demo</summary>

![Dashboard Demo](img/demo_m7_resized.gif)

</details>

## For Developers

To set up and run the dashboard locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/UBC-MDS/DSCI-532_2026_35_financebros.git
   ```

2. **Navigate to the repository folder:**
   ```bash
   cd DSCI-532_2026_35_financebros
   ```

3. **Create the conda environment:**
   ```bash
   conda env create -f environment.yml
   ```

4. **Activate the environment:**
   ```bash
   conda activate DSCI-532_2026_35_financebros
   ```

5. **Run the Shiny app:**
   ```bash
   shiny run src/app.py
   ```

The dashboard will be available at the URL shown in the terminal (typically `http://127.0.0.1:8000`).

## Code Structure

```
src/
├── app.py                  # Entry point — registers tabs and holds all global CSS
├── data_loader.py          # Loads CSV data files and defines DATE_MIN/DATE_MAX constants
├── stocks.py               # Ticker dictionaries: Magnificent 7 and watchlist stocks
├── reactives.py            # Shared reactive calculations (date filtering, risk-return metrics)
├── _input.py               # Runtime proxy for Shiny's input object (session isolation)
│
├── tabs/
│   ├── tab_dashboard.py    # Dashboard tab — top-bar controls and card layout
│   └── tab_chat.py         # Chat tab — Claude-backed QueryChat with Reset and Download CSV
│
└── cards/
    │   # Dashboard cards (driven by selected ticker + date range)
    ├── card_portfolio.py       # Market-cap treemap of all 7 stocks
    ├── card_price_chart.py     # Price history for the selected stock
    ├── card_performance.py     # Normalized return vs. all other stocks
    ├── card_sp500.py           # Selected stock vs. S&P 500 (SPY) benchmark
    ├── card_risk_return.py     # Risk-return scatter (annualized volatility vs. return)
    ├── card_metrics.py         # Sortable fundamentals table (P/E, market cap, etc.)
    ├── card_watchlist.py       # Watchlist table with color-coded price changes
    │
    │   # Chat cards (driven by QueryChat SQL filter)
    ├── card_chat_table.py          # Filtered data table with dynamic SQL-generated title
    ├── card_chat_price_series.py   # Multi-line price chart of filtered data
    └── card_chat_heatmap.py        # Correlation heatmap of daily returns
```
