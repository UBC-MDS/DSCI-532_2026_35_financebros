### 2.1 Updated Job Stories

Review your M1 job stories in light of your deployment setup and any new insights. Update or add stories as needed, and track their status:

| #   | Job Story                       | Status         | Notes                         |
| --- | ------------------------------- | -------------- | ----------------------------- |
| 1   | Portfolio Visualization: As an investor, when I select a stock from the Magnificent 7, I want to see its relative market capitalization compared to other companies in a treemap, so that I can understand the size and weight of each company in the portfolio at a glance. | ✅ Implemented | Implemented as component 7 (Portfolio Treemap), highlights selected stock in blue |
| 2   | Watchlist Tracking: As an investor, when I monitor my watchlist stocks, I want to see their latest price changes in both dollar and percentage formats (togglable), so that I can quickly assess performance and decide whether to buy or sell. | ✅ Implemented | Implemented as component 8 (Watchlist), uses color-coded changes (green/red) |

### 2.2 Component Inventory

Plan every input, reactive calc, and output your app will have. Use this as a checklist during Phase 3. Minimum **2 components per team member** (6 for a 3-person team, 8 for a 4-person team), with **at least 2 inputs and 2 outputs**:


| ID                         | Type          | Shiny widget / renderer     | Depends on           | Job story |
| -------------------------- | ------------- | --------------------------- | -------------------- | --------- |
| `watchlist_toggle`         | Input         | `ui.input_switch()`         | —                    | #2        |
| `render_portfolio_treemap` | Output        | `@render_plotly`            | `ticker`             | #1        |
| `render_watchlist`         | Output        | `@render.data_frame`        | `watchlist_toggle`   | #2        |
