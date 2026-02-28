### 2.1 Updated Job Stories

Review your M1 job stories in light of your deployment setup and any new insights. Update or add stories as needed, and track their status:

| #   | Job Story                       | Status         | Notes                         |
| --- | ------------------------------- | -------------- | ----------------------------- |
| 1   | Reporting: As an investor I want to be able to see a quick preview of the current state of each of the magnificent 7, including current price and performance, so that I can identify which companies are performing better. | ✅ Implemented | Accounted for by component 1                               |
| 2   | Performance tracking: As an investor I want to be able to track the performance of each stock from the Magnificent 7, that I select, over time, so that I can make informed decisions about buying or selling. | ✅ Implemented     | Accounted for by component 2 |

### 2.2 Component Inventory

Plan every input, reactive calc, and output your app will have. Use this as a checklist during Phase 3. Minimum **2 components per team member** (6 for a 3-person team, 8 for a 4-person team), with **at least 2 inputs and 2 outputs**:


| ID                              | Type          | Shiny widget / renderer | Depends on                              | Job story |
| ------------------------------- | ------------- | ----------------------- | --------------------------------------- | --------- |
| `render_current_price`          | Output        | `@render.ui`            | `close_df`                              | #1        |
| `render_stock_price_chart`      | Output        | `@render_plotly`        | `get_filtered_close`, `ticker`          | #2        |