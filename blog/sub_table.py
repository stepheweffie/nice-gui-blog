#!/usr/bin/env python3
import time
from nicegui import ui


@ui.page('/')
def sub_table():
    with ui.row().style('font-size: 2.25em;'):
        columns = [
            {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True},
            {'name': 'email', 'label': 'Email', 'field': 'email', 'sortable': True},
            {'name': 'tier', 'label': 'Tier', 'field': 'tier', 'sortable': True},
        ]
        rows = [
            {'id': 0, 'name': 'Alice', 'email': '', 'tier': 'admin'},
            {'id': 1, 'name': 'Bob', 'email': '', 'tier': 'one'},
            {'id': 2, 'name': 'Lionel', 'email': '', 'tier': 'two'},
            {'id': 3, 'name': 'Michael', 'email': '', 'tier': 'three'},
            {'id': 4, 'name': 'Julie', 'email': '', 'tier': 'three'},
            {'id': 5, 'name': 'Livia', 'email': '', 'tier': 'free'},
            {'id': 6, 'name': 'Carol', 'email': '', 'tier': 'free'},
        ]
        with ui.table(title='My Subscribers', columns=columns, rows=rows, selection='multiple',
                      pagination=10).classes('w-3/4').style(
                     'position: absolute; top: 0%;'
                     'left: 0%; transform: translate(0%, 0%); font-size: 1.25em') as table:

            with table.add_slot('top-right'):
                with ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').add_slot('append'):
                    ui.icon('search').classes('text-4xl')
            with table.add_slot('bottom-row'):
                with table.row():
                    with table.cell():
                        ui.button(on_click=lambda: (
                            table.add_rows({'id': time.time(), 'name': new_name.value, 'email': new_email.value,
                                            'tier': new_tier.value}),
                            new_name.set_value(None),
                            new_email.set_value(None),
                            new_tier.set_value(None),
                        ), icon='add').props('flat fab-mini')
                    with table.cell():
                        new_name = ui.input('Name')
                    with table.cell():
                        new_email = ui.input('Email')
                    with table.cell():
                        tiers = ['Free', 'One', 'Two', 'Three', 'Admin']
                        new_tier = ui.select(options=tiers, label='Tier', value=tiers[0]).classes('text-xl').style(
                            'font-size: 1.25em;')

                with table.row():
                    with table.cell():
                        ui.label().bind_text_from(table, 'selected', lambda val: f'Current selection: {val}')
                    ui.button('Remove', on_click=lambda: table.remove_rows(*table.selected)) \
                        .bind_visibility_from(table, 'selected', backward=lambda val: bool(val)).classes('absolute')

    # ui.query('td').style('font-size: 1.25em;')


ui.run()
