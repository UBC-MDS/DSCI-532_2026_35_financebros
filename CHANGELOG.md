# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Latest Release

## [0.3.0]

### Added
- Track dataset files and integrate datasets with the app (commit 58e2e33).
- Finished Query Chat interactive window (commit f53bdfa).
- Added `rr_period` time window selector (Full / 1Y / 5Y / 10Y) inside the Risk-Return Profile card header for in-chart filtering.
- Added a CSS rule to make the toggle sidebar visible; added hover colours and default button colours to `styles.css`.

### Changed
- Application updates and refactor in `app.py` (commit 87129a0).
- Dependency and environment updates: `requirements.txt` and `environment.yml` updated (commits 63fed0a, cd67e56, 02c4ed4, 4cc4c68, cb16cdf).
- Renamed dashboard components and dashboard title to more descriptive, professional names.
- Layout changes: moved Risk-Return scatter plot to Row 3 and Watchlist & Alerts to Row 1.
- Scatter plot now labels only the selected stock ticker and updated point colors: unselected `#4a9eff`, selected `#ff6b35` with white border.
- Increased font sizes globally for headers, axis titles, tick labels, table values, sort controls, and sidebar labels.
- Updated Sort by dropdown to white background for dark mode visibility.
- Adjusted row heights across layout rows for better spacing; changed card heights per row for improved layout (commit 73e370d).
- UI/styling tweaks: auto-fill CSS adjustments (commit f8c6289) and a lighter color theme (commit eba8a7d).
- Reset button styling updated (commit e8222ac).

### Fixed
- Fixed dark mode hover color on DataGrid rows being unreadable (white background, light blue text).
- Minor typo and text fixes (commit 91e0cee).

### Reflection
At this stage the dashboard provides a useful, interactive view of portfolio and risk-return information: core visual components render and the new Query Chat and rr_period selector show the direction of richer interactivity. These pieces make exploratory analysis and quick comparisons straightforward for users, and the UI styling updates increase readability.

We ran into workflow and code problems this week. A very large app.py (~1k lines) made merging changes painful and caused big conflicts when we rearranged components. The dev branch also introduced regressions that broke the Posit Cloud deployment and made it look like changes were rolled back (missing chat tab and UI issues). To avoid this again, we will discuss countermeasures such as split app.py into smaller components and utility files, use short-lived feature branches with small pull requests, pin and test dependencies, add basic CI checks,... The goal is to minimize merge conflict, catch deployment breaks earlier and increase debugging efficiency. 


## [0.2.0]

1. Adding components 3 - multi-line chart comparing price trends of the Magnificent 7 stocks over a selected time period. 4 - A line chart comparing overall portfolio performance against a benchmark (S&P 500). [here](https://github.com/UBC-MDS/DSCI-532_2026_35_financebros/issues/46)

PR for the fix [here](https://github.com/UBC-MDS/DSCI-532_2026_35_financebros/pull/48)


2. Added components 7 and 8 - a heatmap showing the returns matrix and sizes of the Magnificent 7 stocks, and a watchlist component showing the current price and performance of each stock in the watchlist. [here](https://github.com/UBC-MDS/DSCI-532_2026_35_financebros/issues/47)

PR for the fix [here](https://github.com/UBC-MDS/DSCI-532_2026_35_financebros/pull/49)

3. Added component 1 and 2 - a panel of cards showing each ticker's current price and daily percentage change, and a line chart showing the price trend of a selected stock over time. [here](https://github.com/UBC-MDS/DSCI-532_2026_35_financebros/issues/53)

PR for the fix [here](https://github.com/UBC-MDS/DSCI-532_2026_35_financebros/pull/55)

4. Added app specification documentation, component inventory and reactivity diagram. [here](https://github.com/UBC-MDS/DSCI-532_2026_35_financebros/issues/47)

PR for the final document [here](https://github.com/UBC-MDS/DSCI-532_2026_35_financebros/pull/55)