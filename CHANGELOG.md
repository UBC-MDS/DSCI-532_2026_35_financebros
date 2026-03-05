# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Latest Release

### Added
- Added `rr_period` time window selector (Full / 1Y / 5Y / 10Y) inside the Risk-Return Profile card header for in-chart filtering

### Changed
- Renamed all 8 dashboard components and dashboard title to more descriptive, professional names
- Moved Risk-Return scatter plot to Row 3 and Watchlist & Alerts up to Row 1
- Scatter plot now labels only the selected stock ticker instead of all tickers
- Updated scatter plot point colors: unselected `#4a9eff` (blue), selected `#ff6b35` (orange) with white border
- Increased font sizes globally: card headers, axis titles, tick labels, table values, sort controls, and sidebar labels
- Updated Sort by dropdown to white background for dark mode visibility
- Adjusted row heights across all three layout rows for better spacing

### Fixed
- Fixed dark mode hover color on DataGrid rows being unreadable (white background, light blue text)

### Added / Fixed

## [0.2.0]

1. Adding components 3 - multi-line chart comparing price trends of the Magnificent 7 stocks over a selected time period. 4 - A line chart comparing overall portfolio performance against a benchmark (S&P 500). [here](https://github.com/UBC-MDS/DSCI-532_2026_35_financebros/issues/46)

PR for the fix [here](https://github.com/UBC-MDS/DSCI-532_2026_35_financebros/pull/48)


2. Added components 7 and 8 - a heatmap showing the returns matrix and sizes of the Magnificent 7 stocks, and a watchlist component showing the current price and performance of each stock in the watchlist. [here](https://github.com/UBC-MDS/DSCI-532_2026_35_financebros/issues/47)

PR for the fix [here](https://github.com/UBC-MDS/DSCI-532_2026_35_financebros/pull/49)

3. Added component 1 and 2 - a panel of cards showing each ticker's current price and daily percentage change, and a line chart showing the price trend of a selected stock over time. [here](https://github.com/UBC-MDS/DSCI-532_2026_35_financebros/issues/53)

PR for the fix [here](https://github.com/UBC-MDS/DSCI-532_2026_35_financebros/pull/55)

4. Added app specification documentation, component inventory and reactivity diagram. [here](https://github.com/UBC-MDS/DSCI-532_2026_35_financebros/issues/47)

PR for the final document [here](https://github.com/UBC-MDS/DSCI-532_2026_35_financebros/pull/55)