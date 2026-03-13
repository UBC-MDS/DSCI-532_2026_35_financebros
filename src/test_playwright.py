from shiny.playwright import controller
from shiny.run import ShinyAppProc
from playwright.sync_api import Page
from shiny.pytest import create_app_fixture

import pandas as pd

from data_loader import watchlist_df
from stocks import watchlist as watchlist_dict

import re

app = create_app_fixture("app.py")


def test_watchlist_change_matches_data(page: Page, app: ShinyAppProc):
    """Verifies watchlist dollar changes match the underlying data so daily changes are accurate"""
    page.goto(app.url)

    first_ticker = next(iter(watchlist_dict.keys()))
    current = watchlist_df.iloc[-1][first_ticker]
    previous = watchlist_df.iloc[-2][first_ticker]
    expected = f"${(current - previous):+.2f}"

    watchlist_table = controller.OutputDataFrame(page, "render_watchlist")
    watchlist_table.expect_cell(expected, row=0, col=1)


def test_rr_period_choices_exist(page: Page, app: ShinyAppProc):
    """Verifies the risk‑return period filter exposes the expected options so users can compare horizons"""
    page.goto(app.url)

    rr_period = controller.InputSelectize(page, "rr_period")
    rr_period.expect_choices(["Full", "1Y", "5Y", "10Y"])


def test_watchlist_toggle_changes_format(page: Page, app: ShinyAppProc):
    """Verifies the watchlist toggle switches to percent formatting so users interpret changes correctly"""
    page.goto(app.url)

    toggle = controller.InputSwitch(page, "watchlist_toggle")
    toggle.set(True)

    watchlist_table = controller.OutputDataFrame(page, "render_watchlist")
    watchlist_table.expect_cell(re.compile(r".+%$"), row=0, col=1)
