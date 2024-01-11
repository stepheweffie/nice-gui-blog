from nicegui import ui, app
from search_tab import make_search_tab
from db_utils import async_session
from models import Subscriber
from sqlalchemy import select
from security_layer import pass_security_layer


# Decorator for handling session and exceptions
def session_manager(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            try:
                return await func(session, *args, **kwargs)
            except Exception as e:
                session.rollback()
                print(f"An error occurred: {e}")
            finally:
                session.close()
    return wrapper


# Function to get subscriber based on email
async def get_subscriber(session, email: str):
    # Ensure that email is a string
    if not isinstance(email, str):
        raise ValueError("Email must be a string")

    find = select(Subscriber).where(Subscriber.email == email)
    result = await session.execute(find)
    return result.scalars().first()


# Refactored subscriber update function
@session_manager
async def update_subscriber(session) -> None:
    subscriber = await get_subscriber(session, app.storage.user.get('email'))
    if subscriber:
        print(subscriber.code)
        await session.commit()


# Refactored subscriber delete function
@session_manager
async def delete_subscriber(session) -> None:
    subscriber = await get_subscriber(session, app.storage.user.get('email'))
    if subscriber:
        session.delete(subscriber)
        await session.commit()


# Refactored update password function
@session_manager
async def update_password(session, button: ui.button) -> None:
    button.visible = False
    subscriber = await get_subscriber(session, app.storage.user.get('email'))
    if subscriber:
        print(subscriber.code)
        await session.commit()


def set_timer(switch: ui.switch) -> None:
    if switch.value:
        ui.timer(3.0, lambda: ui.notify('Account Locked', color="warning"), once=True)


def lock_menu(switch: ui.switch, drawer: ui.left_drawer) -> None:
    if switch.value:
        return pass_security_layer()
    drawer.toggle()


def create_search_footer():
    search_footer_button = (ui.button('Search Posts', icon='search', on_click=lambda: search_footer.toggle()
                                      ).classes('text-xl'))
    search_footer = ui.footer(value=False)
    with search_footer:
        ui.button('', icon='close', on_click=lambda: search_footer.toggle()).classes('text-md')
        with ui.row():
            one_tab = ui.tab_panel('Search')
            make_search_tab(one_tab)
    return search_footer_button


switches = {}
buttons = {}

auto_lock_switch = 'Timed Auto Lock'
menu_lock_switch = 'Lock Menu'
update_account_button_label = 'Update Account Info'
update_password_button_label = 'Update Password'
delete_account_button_label = 'Delete Account'


def create_row_with_label_and_input(label_text, input_value, input_class, row_class='w-full no-wrap'):
    with ui.row().classes(row_class):
        ui.input(label_text, value=input_value).classes(input_class)


def create_row_with_button(button_dict, button_text, on_click_action, button_class='w-full text-lg',
                           row_class='w-full no-wrap'):
    with ui.row().classes(row_class):
        button = ui.button(button_text, on_click=on_click_action).classes(button_class)
        button_dict[button_text] = button
        return button


def create_row_with_switch(switch_dict, switch_label, switch_value, on_change_action=None, switch_class='text-lg',
                           row_class='w-full no-wrap'):
    with ui.row().classes(row_class):
        switch = ui.switch(switch_label, value=switch_value, on_change=on_change_action).classes(switch_class)
        switch_dict[switch_label] = switch
        return switch


def create_row_with_select_and_label(label_text, select_options, select_value, select_class='full-width text-lg',
                                     row_class='w-full no-wrap'):
    with ui.row().classes(row_class):
        ui.label(label_text).classes('text-lg')
        ui.select(select_options, value=select_value).classes(select_class)


def sub_account():
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
                ui.timer(time_sec, lambda: pass_security_layer, once=True)
                return time_sec
        time_card.visible = False

    time_card = ui.card().classes('w-96').style(replace='position: absolute; top: 0; left: 0; '
                                                        'z-index: 10000;')
    time_card.visible = False
    with time_card:
        ui.label('Lock Screen Timer').classes('text-3xl')
        with ui.row().classes('w-full no-wrap'):
            time_opts = ['1 minute', '5 minutes', '10 minutes', '15 minutes', '30 minutes', '1 hour', '2 hours',
                         '4 hours', '8 hours', '12 hours', '24 hours']
            timer = ui.select(time_opts, value='30 minutes').classes('text-lg')
            timer.style(replace='margin-bottom: -5px;')
            ui.button('Save', on_click=lambda e: set_time_card(e, time_opts)).classes('w-full text-lg')

    with ui.header().classes(replace='row items-center'):
        if not authenticated:
            ui.button(on_click=lambda: lock_menu(menu_lock, left_drawer), icon='menu').props('color=primary')
        ui.label('NiceGUI Blog').classes('text-4xl m-4')

    if not authenticated:
        # get user info from db and app.storage first
        with ui.left_drawer(value=False).classes('mx-auto p-0') as left_drawer:
            with ui.row().classes('w-full no-wrap justify-end mt-4'):
                ui.label('Account Settings').classes('text-3xl m-4')
                ui.button('', icon='close', on_click=lambda: left_drawer.toggle()).classes('text-md')

            with ui.expansion('Subscriber Information').classes('w-full text-xl'):
                # In the 'Subscriber Information' section
                utilities = 'w-full text-lg'
                datas = ['email', 'first_name', 'last_name', 'username']
                labels = ['Email', 'First_Name', 'Last_Name', 'Username']

                def iterate_input_rows(text: str, att: str, classes: str):
                    create_row_with_label_and_input(f'{text}', app.storage.user.get(f'{att}'),
                                                    f'{classes}')

                for label, data in zip(labels, datas):
                    iterate_input_rows(label, data, utilities)

                create_row_with_button(buttons, 'Update Account Info', lambda: update_subscriber())

            with ui.expansion('Manage Password').classes('w-full text-xl'):
                # In the 'Manage Password' section
                create_row_with_button(buttons, update_password_button_label, lambda: update_password())

            with ui.expansion('Manage Subscription').classes('w-full text-xl'):
                # In the 'Manage Subscription' section
                sub_tier = app.storage.user.get('tier')
                ui.label(f'Current Tier: {sub_tier}').classes('text-md')
                create_row_with_button(buttons, 'Update Subscription', lambda: update_subscriber())

            with ui.expansion('Payment Information').classes('w-full text-xl'):
                create_row_with_button(buttons, 'Update Payment Info', lambda: update_subscriber())

            with ui.expansion('Manage Account').classes('w-full text-xl'):
                # In the 'Manage Account' section
                create_row_with_switch(switches, '2FA', False)
                auto_lock = create_row_with_switch(switches, auto_lock_switch, False, call_time_card)
                menu_lock = create_row_with_switch(switches, menu_lock_switch, False)
                create_row_with_switch(switches, 'NSFW Notify', False)
                create_row_with_button(buttons, 'Delete Account', on_click_action=lambda: delete_subscriber)

        with ui.footer(value=True).style(replace='position: absolute; bottom: 0; left: 0; z-index: 10000;'):
            create_search_footer()
            logout_button = ui.button('', icon='logout', on_click=lambda: app.storage.user.update({'authenticated': False}))
            # list of links in a row
            logout_button.classes('text-xl').style(replace='position: absolute; bottom: 10; right: 0;')

    if not authenticated and not cookied:
        def true_cookie():
            cookie_footer.value = False
            app.storage.user.update({'cookie': True})

        def false_cookie():
            true_cookie()
            app.storage.user.update({'cookie': False})

        with (ui.footer(value=True).classes('bg-blue-100') as cookie_footer):
            with ui.row().classes('w-full no-wrap justify-end mt-4'):
                ui.label('Cookie Notice').style('color: black;').classes('text-2xl')
                ui.label('This website uses cookies to improve your experience.').style('color: black;'
                                                                                        ).classes('text-lg')
                ui.button('Accept', on_click=true_cookie).style('color: black;')
                ui.button('Decline', on_click=false_cookie).style('color: black;')



