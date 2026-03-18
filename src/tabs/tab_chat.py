import base64

import pandas as pd
import shiny.express as _se
from shiny import reactive
from shiny.express import expressify, ui
from querychat.express import QueryChat
import chatlas as clt

from cards.card_chat_table import card_chat_table
from cards.card_chat_price_series import card_chat_price_series
from cards.card_chat_heatmap import card_chat_heatmap

from data_loader import close_tbl


class _InputProxy:
    """Resolve to the current session's input at call time, not import time."""

    def __getattr__(self, name: str):
        return getattr(_se.input, name)


input = _InputProxy()


@expressify
def chat_tab():
    with ui.nav_panel("Chat"):
        ui.markdown(
            """
            ## The Magnificent Analyst

            Ask questions like:
            - "Show only dates after 2021"
            - "Filter to AAPL and MSFT"
            - "Sort by NVDA descending"

            The chat generates SQL to filter/sort the dataset, and the table below updates reactively.
            """
        )

        qc = QueryChat(
            close_tbl,
            "stocks",
            client=clt.ChatAnthropic(model="claude-3-haiku-20240307"),
            greeting=(
                "Hello! I am the Magnificent Analyst, your guide to the Magnificent 7 stock data. Let me know how I can help you explore it!"
            ),
        )

        with ui.layout_sidebar():
            with ui.sidebar(width=420):
                ui.tags.div(
                    {
                        "style": "height: 560px; overflow-y: auto; display: flex; flex-direction: column;"
                    },
                    qc.ui(),
                )
                ui.hr()
                ui.input_action_button("qc_reset", "Reset", class_="w-100")
                ui.hr()
                ui.input_action_button(
                    "qc_dl_filtered", "Download filtered CSV", class_="w-100"
                )

            card_chat_table(qc)
            card_chat_price_series(qc)
            card_chat_heatmap(qc)

        @reactive.effect
        @reactive.event(input.qc_dl_filtered)
        def _download_csv():
            _raw = qc.df()
            df = _raw.execute() if hasattr(_raw, "execute") else _raw
            if df is None:
                df = pd.DataFrame()
            csv_str = df.to_csv(index=False)
            b64 = base64.b64encode(csv_str.encode()).decode()
            ui.insert_ui(
                ui.tags.script(
                    f"""
                    (function() {{
                        const a = document.createElement('a');
                        a.href = 'data:text/csv;base64,{b64}';
                        a.download = 'filtered_stocks_wide.csv';
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                    }})();
                """
                ),
                selector="body",
                where="beforeEnd",
            )

        @reactive.effect
        @reactive.event(input.qc_reset)
        def _qc_reset_effect():
            qc.sql("SELECT * FROM stocks")
