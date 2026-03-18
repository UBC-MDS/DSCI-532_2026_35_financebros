from pathlib import Path

from shiny.express import ui

from tabs.tab_dashboard import dashboard_tab
from tabs.tab_chat import chat_tab

ui.page_opts(title="Magnificent 7 Stock Tracker", fillable=True)

ui.tags.style(
    """
/* Finviz-inspired Stock Visualization Theme */

:root {
  --finviz-bg-dark: #131722;
  --finviz-bg-card: #1e222d;
  --finviz-bg-sidebar: #1e222d;
  --finviz-text: #d1d4dc;
  --finviz-text-muted: #787b86;
  --finviz-green: #44bb70;
  --finviz-red: #d62728;
  --finviz-border: #2a2e39;
  --finviz-accent: #2962ff;
}

/* Global dark theme */
body {
  background-color: var(--finviz-bg-dark) !important;
  color: var(--finviz-text) !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

.main,
.bslib-card-body p {
  color: var(--finviz-text) !important;
}

h2, .h2 {
  font-size: calc(1rem + .9vw) !important;
}

/* Card styling */
.bslib-card {
  color: var(--finviz-text) !important;
  background-color: var(--finviz-bg-card) !important;
  border: 1px solid var(--finviz-border) !important;
  border-radius: 4px !important;
  height: 28vh !important;
}

.bslib-card-header,
.card-header {
  background-color: rgba(42, 46, 57, 0.6) !important;
  border-bottom: 1px solid var(--finviz-border) !important;
  color: var(--finviz-text) !important;
  font-weight: 600 !important;
  font-size: 1rem !important;
}

.bslib-card .card-body {
  height: calc(28vh - 40px) !important;
  overflow: hidden !important;
}

.watchlist-card .card-body {
  overflow-y: auto !important;
}

.portfolio-card {
  height: 30vh !important;
}

.portfolio-card .card-body {
  height: calc(30vh - 40px) !important;
}

/* Shiny data grid styling */
.shiny-data-grid table thead th {
  background-color: transparent !important;
  color: var(--finviz-text) !important;
}

.shiny-data-grid table tbody tr:hover,
.shiny-data-grid table tbody tr:hover td,
[data-row]:hover {
  background-color: #2a3a4a !important;
  color: #ffffff !important;
}

.shiny-data-grid table td,
.shiny-data-grid table th {
  font-size: 0.8125rem !important;
}

/* QueryChat: disable hover on chat tables */
.shiny-data-grid .rt-tr:hover,
.shiny-data-grid .data-grid-row:hover,
.shiny-data-frame table tbody tr:hover,
.shiny-data-frame .rt-tr:hover {
  background-color: transparent !important;
}

/* Form controls */
.form-control,
.form-select,
input[type="text"],
select {
  background-color: var(--finviz-bg-dark) !important;
  color: var(--finviz-text) !important;
  border: 1px solid var(--finviz-border) !important;
}

.form-control:focus,
.form-select:focus {
  border-color: var(--finviz-accent) !important;
  box-shadow: 0 0 0 0.2rem rgba(41, 98, 255, 0.25) !important;
}

#dates input {
  font-size: 0.75rem !important;
}

label {
  color: var(--finviz-text) !important;
}

label[for="metrics_sort_by"],
label[for="metrics_sort_dir"] {
  font-size: 0.875rem !important;
}

/* Specific control styling */
#metrics_sort_by {
  font-size: 0.875rem !important;
  background-color: #ffffff !important;
  color: #000000 !important;
  border: 1px solid #cccccc !important;
}

.selectize-control .selectize-dropdown {
  font-size: 0.875rem !important;
  background-color: #ffffff !important;
  color: #000000 !important;
}

#metrics_sort_dir label {
  font-size: 0.875rem !important;
}

#rr_period + .selectize-control .selectize-input,
#rr_period + .selectize-control .selectize-dropdown {
  font-size: 0.875rem !important;
}

/* Plotly charts */
.js-plotly-plot .plotly .main-svg {
  color: var(--finviz-text) !important;
  background-color: transparent !important;
}

.js-plotly-plot,
.plotly,
.plotly > div {
  height: 100% !important;
}

/* Ticker strip */
.tickerstrip {
  display: flex;
  align-items: stretch;
  border: 1px solid var(--finviz-border);
  border-radius: 10px;
  overflow: hidden;
  background: var(--finviz-bg-card);
}

.tickerbox {
  flex: 1;
  padding: 10px 10px 8px 10px;
  min-width: 0;
  text-align: left;
}

.tickerbox + .tickerbox {
  border-left: 1px solid var(--finviz-border);
}

.tickerbox-ticker {
  font-weight: 700;
  font-size: 12px;
  letter-spacing: 0.04em;
  color: var(--finviz-text);
  text-transform: uppercase;
  margin-bottom: 4px;
}

.tickerbox-price {
  font-weight: 700;
  font-size: 16px;
  color: #ffffff;
  line-height: 1.1;
}

.tickerbox-ret {
  margin-top: 4px;
  font-weight: 600;
  font-size: 12px;
  line-height: 1.1;
  display: inline-flex;
  gap: 6px;
  align-items: center;
}

.ret-pos { color: var(--finviz-green); }
.ret-neg { color: var(--finviz-red); }
.ret-flat { color: #9aa0a6; }

.ret-arrow {
  font-size: 12px;
  opacity: 0.95;
}

.tickerbox:hover {
  background: #232a37;
}

@media (max-width: 900px) {
  .tickerstrip {
    overflow-x: auto;
  }
  .tickerbox {
    flex: 0 0 140px;
  }
}

/* ShinyChat dark theme */
.shinychat-chat,
.shinychat,
.shinychat-container {
  background: #131722 !important;
  color: var(--finviz-text) !important;
}

.shinychat-chat .card,
.shinychat .card {
  background: var(--finviz-bg-card) !important;
  border: 1px solid var(--finviz-border) !important;
}

.shinychat-message,
.shinychat-message *,
.querychat-greeting,
.querychat-greeting * {
  color: var(--finviz-text) !important;
}

/* QueryChat greeting and message bubbles */
.querychat p,
.querychat span,
.querychat div,
[class*="querychat"] p,
[class*="querychat"] span,
[class*="querychat"] div {
  color: var(--finviz-text) !important;
}

.shinychat-input,
.shinychat-input textarea,
.shinychat-input input,
.shinychat textarea,
.shinychat input {
  background: var(--finviz-bg-card) !important;
  color: var(--finviz-text) !important;
  border: 1px solid var(--finviz-border) !important;
}

.shinychat .btn,
.shinychat-chat .btn {
  border-color: var(--finviz-border) !important;
}

/* Reset / Download CSV buttons in Chat sidebar */
#qc_reset,
#qc_dl_filtered {
  background-color: var(--finviz-bg-card) !important;
  color: var(--finviz-text) !important;
  border: 1px solid var(--finviz-border) !important;
}

#qc_reset:hover,
#qc_dl_filtered:hover {
  background-color: #2a2e39 !important;
  color: #ffffff !important;
  border-color: var(--finviz-accent) !important;
}
"""
)

with ui.navset_tab(id="main_tabs"):
    dashboard_tab()
    chat_tab()

# -----------------------------------------------------------------------------
# Apply finviz-inspired styles
# -----------------------------------------------------------------------------
# ui.include_css(Path(__file__).parent / "styles.css")
