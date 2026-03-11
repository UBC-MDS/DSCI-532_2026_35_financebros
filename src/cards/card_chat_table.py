from shiny.express import expressify, render, ui


@expressify
def card_chat_table(qc):
    with ui.card(full_screen=True):
        ui.card_header("Filtered table")

        @render.text
        def qc_title():
            return qc.title() or "Stocks dataset"

        @render.data_frame
        def qc_table():
            return qc.df()
