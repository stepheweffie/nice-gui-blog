from nicegui import ui, app
from post_list_layout import make_search_tab
from db_utils import async_session
from models import Subscriber
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from security_layer import dash_security_layer


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


async def delete_subscriber() -> None:
    async with async_session() as session:
        try:
            find = select(Subscriber).where(Subscriber.email == app.storage.user.get('email'))
            result = await session.execute(find)
            subscriber = result.scalars().first()
            session.delete(subscriber)
            await session.commit()
        except IntegrityError:
            pass


async def update_password(button: ui.button) -> None:
    button.visible = False
    async with async_session() as session:
        try:
            find = select(Subscriber).where(Subscriber.email == app.storage.user.get('email'))
            result = await session.execute(find)
            subscriber = result.scalars().first()
            print(subscriber.code)
            await session.commit()
        except IntegrityError:
            pass


def set_timer(switch: ui.switch) -> None:
    if switch.value:
        ui.timer(3.0, lambda: ui.notify('Account Locked', color="warning"), once=True)


def lock_menu(switch: ui.switch, drawer: ui.left_drawer) -> None:
    if switch.value:
        return dash_security_layer()
    drawer.toggle()


def header():
    authenticated = app.storage.user.get('authenticated')
    cookied = app.storage.user.get('cookie')

    def call_time_card():
        time_card.visible = auto_lock.value

    def set_time_card(minutes: str, times: list):
        # zip the options with the time in seconds and make a timer to set off
        seconds = [60, 300, 600, 900, 1800, 3600, 7200, 14400, 28800, 43200, 86400]
        times_in_seconds = zip(times, seconds)
        for time_str, time_sec in times_in_seconds:
            if minutes == time_str:
                ui.timer(time_sec, lambda: dash_security_layer, once=True)
                return time_sec
        time_card.visible = False

    time_card = ui.card().classes('w-96').style(replace='position: absolute; top: 0; left: 0; '
                                                        'z-index: 10000;')
    time_card.visible = False
    with time_card:
        ui.label('Lock Screen Timer').classes('text-3xl')
        with ui.row().classes('w-full no-wrap'):
            timer = ui.select(
                ['1 minute', '5 minutes', '10 minutes', '15 minutes', '30 minutes', '1 hour', '2 hours', '4 hours',
                 '8 hours', '12 hours', '24 hours'], value='30 minutes').classes('text-lg')
            ui.button('Save', on_click=lambda e: set_time_card(e, options)).classes('w-full text-lg')

    with ui.header().classes(replace='row items-center'):
        if not authenticated:
            ui.button(on_click=lambda: lock_menu(menu_lock_switch, left_drawer), icon='menu').props('flat color=white')
        ui.label('NiceGUI Blog').classes('text-4xl m-4')

    if not authenticated:
        # get user info from db and app.storage first
        with ui.left_drawer(value=False).classes('mx-auto p-0') as left_drawer:
            with ui.row().classes('w-full no-wrap justify-end mt-4'):
                ui.label('Account Settings').classes('text-3xl m-4')
                ui.button('', icon='close', on_click=lambda: left_drawer.toggle()).classes('text-md')
            with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
                ui.button(on_click=ui.open('/logout'), icon='logout').props('fab')

            with ui.expansion('Subscriber Information').classes('w-full text-xl'):
                with ui.row().classes('w-full no-wrap'):
                    ui.input('Email', value=app.storage.user.get('email')).classes(
                        'full-width text-lg')

                with ui.row().classes('w-full no-wrap'):
                    name_input = ui.input('First Name', value=app.storage.user.get('first_name')).classes(
                        'full-width text-lg')

                with ui.row().classes('w-full no-wrap'):
                    lname_input = ui.input('Last Name', value=app.storage.user.get('last_name')).classes(
                        'full-width text-lg')

                with ui.row().classes('w-full no-wrap'):
                    username_input = ui.input('Username', value=app.storage.user.get('username')).classes(
                        'full-width text-lg')

                with ui.row().classes('w-full no-wrap justify-center'):
                    ui.button('Update Account Info', on_click=lambda: update_subscriber()).classes('w-full text-lg')

            with ui.expansion('Manage Password').classes('w-full text-xl'):
                with ui.row().classes('w-full no-wrap'):
                    code_button = ui.button('Send Code', on_click=lambda: update_password(code_button)).classes(
                        'w-full text-lg')
                    resend_button = ui.button('Resend Code', on_click=lambda: update_password(resend_button)).classes(
                        'w-full text-lg')

                    resend_button.visible = not code_button.visible

                with ui.row().classes('w-full no-wrap'):
                    ui.input('New Password', password=True, password_toggle_button=True).classes(
                        'full-width text-lg')

                with ui.row().classes('w-full no-wrap'):
                    ui.input('Verification Code', password=True, password_toggle_button=True).classes(
                        'full-width text-lg')

                with ui.row().classes('w-full no-wrap'):
                    ui.button('Save', on_click=lambda: update_password()).classes('w-full text-lg')

            with ui.expansion('Manage Subscription').classes('w-full text-xl'):
                with ui.row().classes('w-full no-wrap'):
                    ui.label('Current Subscription Tier: ').classes('text-lg')
                    ui.label(app.storage.user.get('tier')).classes('text-lg')

                with ui.row().classes('w-full no-wrap'):
                    options = ['Free', 'Tier 1', 'Tier 2', 'Tier 3']
                    tier_select = ui.select(options, label='Change Subscription Tier', value=app.storage.user.get('tier')).classes(
                        'full-width text-lg')

                with ui.row().classes('w-full no-wrap'):
                    ui.button('Update Subscription', on_click=lambda: update_subscriber()).classes('w-full text-lg')

            with ui.expansion('Payment Information').classes('w-full text-xl'):
                with ui.row().classes('w-full no-wrap'):
                    ui.button('Change Payment Method', on_click=lambda: update_subscriber()).classes('w-full text-lg')

            with ui.expansion('Manage Account').classes('w-full text-xl'):
                with ui.row().classes('w-full no-wrap'):
                    two_factor_switch = ui.switch('2FA', value=False).classes('text-lg')

                with ui.row().classes('w-full no-wrap'):
                    auto_lock = ui.switch('Auto Locking Screen', value=False, on_change=call_time_card).classes(
                        'text-lg')

                with ui.row().classes('w-full no-wrap'):
                    ui.switch('NSFW Notify', value=False).classes('text-lg')

                with ui.row().classes('w-full no-wrap'):
                    menu_lock_switch = ui.switch('Lock Account Menu', value=False).classes('text-lg')

                with ui.row().classes('w-full no-wrap justify-center'):
                    ui.button('Delete Account', on_click=lambda: delete_subscriber).classes('w-full text-lg')

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




