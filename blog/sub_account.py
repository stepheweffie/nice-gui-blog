from nicegui import ui, app
from post_list_layout import make_search_tab
from db_utils import async_session
from models import Subscriber
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


async def update_subscriber() -> None:
    async with async_session() as session:
        try:
            find = select(Subscriber).where(Subscriber.email == app.storage.user.get('email'))
            result = await session.execute(find)
            subscriber = result.scalars().first()
            print(subscriber.code)
            await session.commit()
        except IntegrityError:
            pass


async def update_password() -> None:
    async with async_session() as session:
        try:
            find = select(Subscriber).where(Subscriber.email == app.storage.user.get('email'))
            result = await session.execute(find)
            subscriber = result.scalars().first()
            print(subscriber.code)
            await session.commit()
        except IntegrityError:
            pass


def header():
    authenticated = app.storage.user.get('authenticated')
    cookied = app.storage.user.get('cookie')
    with ui.header().classes(replace='row items-center'):
        if not authenticated:
            ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
        ui.label('NiceGUI Blog').classes('text-4xl m-4')

    if not authenticated:
        # get user info from db and app.storage first
        with ui.left_drawer(value=False).classes('mx-auto p-0') as left_drawer:
            with ui.row().classes('w-full no-wrap justify-end mt-4'):
                ui.label('Account Settings').classes('text-3xl m-4')
                ui.button('', icon='close', on_click=lambda: left_drawer.toggle()).classes('text-lg')
            with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
                ui.button(on_click=ui.open('/logout'), icon='logout').props('fab')
            with ui.expansion('Subscriber Information').classes('w-full text-xl'):
                with ui.row().classes('w-full no-wrap'):
                    ui.input('Email', value=app.storage.user.get('email')).classes(
                        'full-width text-lg')
                    ui.button('', icon='save', on_click=lambda: app.storage.user.update({'email': ui.input('Email')
                                                                                    .value})).classes('text-lg')
                with ui.row().classes('w-full no-wrap'):
                    name_input = ui.input('First Name', value=app.storage.user.get('first_name')).classes(
                        'full-width text-lg')
                    ui.button('', icon='save', on_click=lambda: app.storage.user.update({'first_name': name_input
                                                                                    .value})).classes('text-lg')
                with ui.row().classes('w-full no-wrap'):
                    lname_input = ui.input('Last Name', value=app.storage.user.get('last_name')).classes(
                        'full-width text-lg')
                    ui.button('', icon='save', on_click=lambda: app.storage.user.update({'last_name': lname_input
                                                                                    .value})).classes('text-lg')
                with ui.row().classes('w-full no-wrap'):
                    username_input = ui.input('Username', value=app.storage.user.get('username')).classes(
                        'full-width text-lg')
                    ui.button('', icon='save', on_click=lambda: app.storage.user.update({'username': username_input
                                                                                    .value})).classes('text-lg')
                with ui.row().classes('w-full no-wrap'):
                    options = ['Free', 'Tier 1', 'Tier 2', 'Tier 3']
                    tier_select = ui.select(options, label='Subscription Tier', value=app.storage.user.get('tier')).classes(
                        'full-width text-lg')
                    ui.button('', icon='save', on_click=lambda: app.storage.user.update({'tier': tier_select
                                                                                    .value})).classes('text-lg')
                with ui.row().classes('w-full no-wrap justify-center'):
                    ui.button('Update Account Info', on_click=lambda: update_subscriber()).classes('w-full text-lg')

            with ui.expansion('Manage Password').classes('w-full text-xl'):
                with ui.row().classes('w-full no-wrap'):
                    ui.button('Send Code', on_click=lambda: update_password()).classes('w-full text-lg')

                with ui.row().classes('w-full no-wrap'):
                    ui.input('New Password', password=True, password_toggle_button=True).classes(
                        'full-width text-lg')

                with ui.row().classes('w-full no-wrap'):
                    ui.input('Verification Code', password=True, password_toggle_button=True).classes(
                        'full-width text-lg')

                with ui.row().classes('w-full no-wrap'):
                    ui.button('Save', on_click=lambda: update_password()).classes('w-full text-lg')

    if not authenticated and not cookied:
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

    if authenticated:
        with ui.footer(value=True):
            ui.button('Search Posts', on_click=lambda: search_footer.toggle())
    if authenticated:
        search_footer = ui.footer(value=False)
        with search_footer:
            ui.button('', icon='close', on_click=lambda: search_footer.toggle()).classes('text-xl')
            one_tab = ui.tab_panel('Search')
            make_search_tab(one_tab)




