# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Latest Release

## [0.4.0] - 2026-03-12

### Added

- Added reactive stock selection shared across components: clicking the Portfolio treemap updates the selected ticker (and syncs with the dropdown) and updates dependent charts. (PR #85)
- Added automated testing: 1 unit test, refactored logic into at least one testable function, and 3 Playwright tests; documented a single command to run tests in the README. (PR #90)


### Changed

- Major refactor: split the monolithic `app.py` into modular dashboard/chat components and introduced a runtime input proxy for safer session isolation. (PR #76)
- Improved documentation and end-user guidance in `README.md`, including peer-review driven updates and additional prompts. (PRs #83, #91, #93)
- Switched the QueryChat model configuration and adjusted sidebar sizing for improved usability. (PR #72)
- Updated dashboard visuals and layout:
  - Performance card y-axis changed to log scale and mermaid/diagram updates. (PRs #91, #93)
  - General UI naming consistency (“Magnificent 7 Tracker”), plus multiple UI/UX tweaks. (PR #85)


### Fixed

- Fixed metrics table sorting for numeric fields (e.g., Market Cap, Dividend Yield) by sorting on raw numeric values prior to formatting. (PR #85)

- **Feedback prioritization issue link:** #...

### Data / Backend
- Replaced the CSV backend with an ibis + DuckDB parquet workflow:
  - Added parquet data files and an ETL notebook to generate them.
  - Updated data loader to expose ibis table expressions and materialized pandas DataFrames.
  - Updated dashboard components to execute lazy ibis results where needed. (PR #94)

### Release Highlight: [Name of your advanced feature]

- **Option chosen:** D
- **PR:** #85
- **Why this option over the others:** 
We selected **Option D: Component click event interaction** because it best fits our
dashboard's primary workflow: exploring a portfolio by clicking on a visual summary
and immediately seeing linked, detailed views update.
- **Feature prioritization issue link:** #77

### Collaboration

- **CONTRIBUTING.md:** #95
- **M3 retrospective:** After M3 feedback, we shifted to smaller, scoped PRs with spec-first updates and earlier peer review to reduce last-minute merges.
- **M4:** We split tasks more evenly. 


### Reflection
- *Pytest unit test*: test_compute_risk_return_basic. It checks the function in refactored.py, compute_risk_return. This test validates the core math in compute_risk_return, the annualization of daily returns and volatility. The logic is nearly identical, it ensures that it sets the Date index, optionally filter by cutoff, compute pct_change, and annualize mean and std by 252, it just has the reactive dependencies removed
    - If the annualization multiplier changes from 252 (trading days) to 365 (calendar days), both assertions fail
    - If pct_change() is replaced with log returns, the mean shifts slightly and the AnnReturn assertion fails
    - If dropna(how="all") changes to dropna(how="any"), rows with partial data get dropped, potentially breaking the row count assumption
    - If rets.std() switches from sample std (ddof=1, pandas default) to population std (ddof=0), the volatility for non-uniform data would differ — though this specific test wouldn't catch it since std of identical values is 0 either way
    - If .dropna() on the output DataFrame drops rows differently, out.iloc[0] could raise an IndexError
- *refactorization*: compute_risk_return in refactored.py is a refactoring of the risk_return_df in the reactives.py file. The refactored code is a pure function and does what risk_return_df does (in reactives.py) the pytest unit test is test_compute_risk_return_basic in unit_test.py
- *Playwright Test 1*: test_watchlist_change_matches_data. It covers: loading the app, computes the expected dollar change for the first watchlist ticker from the raw data (current - previous), then asserts that the rendered DataGrid cell at row 0, col 1 shows that value formatted as $+X.XX. 
- What breaks if behavior changes: 
    - If the watchlist table column order changes (e.g. change column moves from index 1), the cell lookup hits the wrong column
    - If the dollar formatting changes (e.g. drops the + sign for positive values, or uses different decimal places), the string comparison fails
    - If watchlist_df row ordering changes (e.g. sorted differently), iloc[-1] and iloc[-2] no longer represent the two most recent dates
    - If the default toggle state starts as True (percent mode), the cell won't match the dollar format and the test fails 
- *Playwright Test 2*: test_rr_period_choices_exist. It covers: Navigates to the app and asserts the rr_period selectize input shows exactly these four choices in this order: ["Full", "1Y", "5Y", "10Y"]. 
- What breaks if behavior changes:
    - Adding, removing, or renaming any period option (e.g. adding "3Y", renaming "Full" to "All") causes the assertion to fail
    - Reordering the choices list fails the assertion since expect_choices checks order
    - If the input widget ID is renamed from "rr_period", Playwright can't locate the element
- *Playwright Test 3*: test_watchlist_toggle_changes_format. it covers: sets the watchlist_toggle switch to True and asserts that the first data cell in col 1 now matches a regex ending in %, confirming the display switched from dollar to percent formatting
- What breaks if behavior changes:
    - If toggling to True no longer switches to percent mode, the cell won't end in % and the regex fails
    - If the percent format changes to something that doesn't end in % (e.g. "10 pct"), the regex fails
    - If the table re-renders with a different row order after toggle, row 0 col 1 may not be the cell being reformatted




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