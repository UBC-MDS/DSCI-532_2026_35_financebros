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