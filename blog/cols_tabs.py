from nicegui import ui, app
from post_list_layout import make_search_tab


def header():
    authenticated = app.storage.user.get('authenticated')
    cookied = app.storage.user.get('cookie')
    with ui.header().classes(replace='row items-center'):
        if authenticated:
            ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
        ui.label('NiceGUI Blog').classes('text-4xl m-4')

    if authenticated:
        with ui.left_drawer(value=False).classes('mx-auto p-0') as left_drawer:
            with ui.expansion('Subscriber Information'):
                ui.label('Email: ' + app.storage.user.get('email'))
            one_tab = ui.tab_panel('Search')

    if authenticated:
        with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
            ui.button(on_click=ui.open('/logout'), icon='logout').props('fab')

    if authenticated and not cookied:
        def true_cookie():
            cookie_footer.value = False
            app.storage.user.update({'cookie': True})

        def false_cookie():
            true_cookie()
            app.storage.user.update({'cookie': False})

        with ui.footer(value=True).classes('bg-blue-100') as cookie_footer:
            ui.label('Cookie Info').style('color: black;').classes('text-2xl')
            with ui.row():
                ui.label('This website uses cookies to improve your experience.').style('color: black;')
                ui.button('Accept', on_click= true_cookie).style('color: black;')
                ui.button('Decline', on_click=false_cookie).style('color: black;')

    if not authenticated:
        with ui.footer(value=True):
            ui.button('Search Posts', on_click=lambda: search_footer.toggle())
    if not authenticated:
        search_footer = ui.footer(value=False)
        with search_footer:
            ui.button('', icon='close', on_click=lambda: search_footer.toggle()).classes('text-xl')
            one_tab = ui.tab_panel('Search')
            make_search_tab(one_tab)




