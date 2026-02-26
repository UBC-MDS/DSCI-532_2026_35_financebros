### 2.1 Updated Job Stories

Review your M1 job stories in light of your deployment setup and any new insights. Update or add stories as needed, and track their status:

| #   | Job Story                       | Status         | Notes                         |
| --- | ------------------------------- | -------------- | ----------------------------- |
| 1   | When I … I want to … so I can … | ✅ Implemented |                               |
| 2   | When I … I want to … so I can … | 🔄 Revised     | Changed from X to Y because … |
| 3   | When I … I want to … so I can … | ⏳ Pending M3  |                               |

### 2.2 Component Inventory

Plan every input, reactive calc, and output your app will have. Use this as a checklist during Phase 3. Minimum **2 components per team member** (6 for a 3-person team, 8 for a 4-person team), with **at least 2 inputs and 2 outputs**:


| ID                              | Type          | Shiny widget / renderer | Depends on                              | Job story |
| ------------------------------- | ------------- | ----------------------- | --------------------------------------- | --------- |
| `ticker`                        | Input         | `ui.input_selectize()`  | —                                       | #1        |
| `dates`                         | Input         | `ui.input_date_range()` | —                                       | #1        |
| `get_filtered_close`            | Reactive calc | `@reactive.calc`        | `dates`                                 | #1        |
| `render_performance_comparison` | Output        | `@render_plotly`        | `get_filtered_close`, `ticker`          | #1        |
| `render_sp500_comparison`       | Output        | `@render_plotly`        | `get_filtered_close`, `ticker`, `dates` | #1        |
