# Magnificent 7 Tracker

An interactive stock dashboard for the Magnificent 7

## Live Demo

- **Stable:** https://019c96fb-7645-b17f-61b0-46a58d974625.share.connect.posit.cloud/
- **Preview:** https://019c96fc-ef4e-2932-2355-311a3030aeb5.share.connect.posit.cloud/

## About

The financebros dashboard is a web application that tracks key financial metrics regarding a portfolio comprised of the Magnificent Seven stocks: Apple, Microsoft, Amazon, Alphabet (Google’s parent company), Meta, Nvidia, and Tesla. The dashboard provides users with insights into the performance of these stocks, including price trends, volatility, and other relevant financial indicators. It also compares the performance of the portfolio against the S&P 500 index.

## How to Use the Dashboard

This section is a quick orientation for first-time users. The dashboard has two main tabs: **Dashboard** and **Chat**.


<details open>
<summary>Click to close app how-to</summary>

**1. Historical Closing Price Trend** *(top-left)*
This chart shows the daily closing price of your selected stock over the chosen date range. Use the **Select Stock** dropdown and **Select Date Range** inputs at the top of the page to filter the view. The percentage change label (e.g., `+1.92%`) reflects total return over the selected period.

**2. Portfolio Overview** *(top-center)*
A treemap showing the relative market-cap weight of each Magnificent 7 stock. Larger tiles = larger market cap. Red tiles indicate the stock is down on the current day; green tiles indicate it is up. Hovering over a tile shows the ticker, current price, and daily change.

**3. Watchlist & Alerts** *(top-right)*
A quick-glance table of stocks outside the Mag 7 that you may want to monitor. The **Change** column shows the day's dollar move — red for losses, green for gains. Toggle **Show %** to switch between dollar and percentage change. This panel is designed as a passive alert surface: if any watchlist stock moves significantly, it will stand out at a glance.

**4. Relative Performance Comparison** *(bottom-left)*
All seven stocks normalized to a base of 100 at the start of the selected date range, so you can compare growth on a level playing field regardless of absolute price. The y-axis uses a logarithmic scale, so equal vertical distances represent equal percentage moves — preventing high-growth stocks like NVDA from compressing everything else to a flat line. A stock with a value of 25k has grown 250× from the base. This panel is most useful for long date ranges to spot which stocks drove the most compounded growth.

**5. Price Performance vs. S&P 500 Benchmark** *(bottom-center)*
The selected stock (blue) plotted against SPY (gold), both normalized to 100. This answers the core question: *is this stock actually beating the market?* A blue line consistently above the gold line means the stock is outperforming the index over the chosen window.

**6. Fundamental Metrics Overview** *(bottom-left table)*
A sortable table of key fundamentals — Market Cap, P/E Ratio, Dividend Yield, and Revenue Growth — pulled from the most recent available quarterly filings. Use the **Sort by** dropdown and **Ascending/Descending** toggle to rank stocks by any metric. This is useful for quick fundamental screening (e.g., "which Mag 7 stock has the lowest P/E right now?").

**7. Risk-Return Profile** *(bottom-right)*
A scatter plot where each bubble represents one stock. The X-axis is annualized volatility (risk) and the Y-axis is annualized return. Stocks in the **upper-left** quadrant are the most desirable: high return, low risk. Use the time-period dropdown (e.g., `Full`, `1Y`, `3Y`) to see how the risk-return tradeoff has shifted across different market regimes.

### Chat Tab

The Chat tab gives you a conversational interface powered by Claude. You can ask it questions about any of the stocks or the data visible in the dashboard. It does **not** have live data access by default — for real-time prices and breaking news, cross-reference with the dashboard panels or a live financial source.

</details>

## Demo

<details open>
<summary>Click to close app demo</summary>

![Dashboard Demo](img/demo.gif)

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

## Tests

Run all tests with one command:

   ```bash
   python -m pytest -v --browser firefox  
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
