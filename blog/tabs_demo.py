from nicegui import ui


with ui.dialog() as dialog, ui.card():
    with ui.tabs() as tabs:
        tab1 = ui.tab("TAB1")
        tab2 = ui.tab("TAB2")

    with ui.tab_panels(tabs, value=tab1) as tabs_panel:  # ISSUE 1
        with ui.tab_panel(tab1):
            with ui.column().classes('items-center'):
                field1 = ui.input('field1')

        with ui.tab_panel(tab2):
            with ui.column().classes('items-center'):
                field2 = ui.input('field2')

    with ui.row():
        ui.button("Save", on_click=lambda: dialog.submit("Yes"))
        ui.button("Cancel", on_click=lambda: dialog.submit(None))

ui.button('Open a dialog', on_click=dialog.open)

ui.run()