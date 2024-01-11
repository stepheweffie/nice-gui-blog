from nicegui import ui, app, Client
from models import Subscriber
from db_utils import async_session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from search_tab import make_search_tab
from post_lists import post_preview
from security_layer import pass_security_layer

app_name = 'The Blog'
brand_name = 'My Brand'
terms = 'Terms of Service'
privacy = 'Privacy Policy'


async def main_page(client: Client) -> None:
    authenticated = app.storage.user.get('authenticated')
    onboard(authenticated)


def onboard(authenticated) -> None:
    with ui.row().classes('w-full wrap flex justify-start mt-4'):
        with ui.column().classes('xs-col-12 sm-col-12 md-col-6 lg-col-6 xl-col-6'):
            ui.label('The Latest Posts').classes('text-3xl m-4')
            post_preview()
        if not authenticated:
            with ui.column().classes('xs-col-12 sm-col-12 md-col-6 lg-col-6 xl-col-6'):
                subscribed = app.storage.user.get('subscribed')

                with ui.tabs() as tabs:
                    one = ui.tab('Search')
                    two_tab = ui.tab('Verify')
                    two_tab.visible = subscribed
                    two_two = ui.tab('Subscribe')
                    two_two.visible = not subscribed
                    three = ui.tab('Login')

                with ui.tab_panels(tabs, value=one):
                    one_tab = ui.tab_panel(one)
                    make_search_tab(one_tab)

                    async def verify_subscriber() -> None:
                        async with async_session() as session:
                            try:
                                find = select(Subscriber).where(Subscriber.email == app.storage.user.get('email'))
                                result = await session.execute(find)
                                subscriber = result.scalars().first()
                                subscriber.verify_subscriber(signup_password, signup_code.value)
                                await session.commit()
                            except IntegrityError:
                                pass
                            app.storage.user.update({'authenticated': True})
                            ui.notify('Login Successful', color='positive')
                            await session.rollback()
                            # set_visibility to cart modal on /
                            ui.open('/')

                    with ui.tab_panel(two_tab):
                        with ui.column().classes('items-center'):
                            with ui.card().classes('w-96'):
                                ui.label('Verify').classes('text-xl h-full')
                                signup_password = ui.input('Password').classes('w-full')
                                signup_code = ui.input('Secret Code').classes('w-full')
                                ui.button('Verify and Login', on_click=verify_subscriber).classes(
                                    'w-full transition-all')

                            with ui.row():
                                ui.label(f"By subscribing, you agree to our").classes('text-sm')
                                ui.link(f"{terms}").classes('text-sm')
                                ui.label(f"and").classes('text-sm')
                                ui.link(f"{privacy}").classes('text-sm')

                    async def create_subscriber() -> None:
                        async with async_session() as session:
                            try:
                                sub = Subscriber()
                                sub.email = signup_email.value
                                sub.tier = 'Free'
                                sub.create_subscriber(sub.email, sub.tier)
                                session.add(sub)
                                await session.commit()
                                ui.notify(f'Subscription Successful. Please check {signup_email.value}', color='positive')
                                app.storage.user.update(
                                    {'email': signup_email.value, 'authenticated': False, 'is_admin': False,
                                     'subscribed': True})
                                app.storage.user.update({'first_name': "Enter First Name"})
                                app.storage.user.update({'last_name': "Enter Last Name"})
                                app.storage.user.update({'username': "Enter A Username"})
                                app.storage.user.update({'tier': "Free"})
                                await session.rollback()
                            except IntegrityError:
                                ui.notify('Email already exists', color='negative')
                            ui.open('/')

                    with ui.tab_panel(two_two):
                        with ui.column().classes('items-center'):
                            with ui.card().classes('w-96'):
                                ui.label('Free Subscription Access').classes('text-xl h-full')
                                signup_email = ui.input('Email').classes('w-full')
                                ui.button('Subscribe', on_click=create_subscriber).classes('w-full transition-all')
                            with ui.row():
                                ui.label(f"By subscribing, you agree to our").classes('text-sm')
                                ui.link(f"{terms}").classes('text-sm')
                                ui.label(f"and").classes('text-sm')
                                ui.link(f"{privacy}").classes('text-sm')

                    async def login_subscriber() -> None:
                        async with async_session() as session:
                            try:
                                find = select(Subscriber).where(Subscriber.email == sub_email.value)
                                result = await session.execute(find)
                                subscriber = result.scalars().first()
                            except IntegrityError:
                                pass
                            if subscriber.check_password(sub_pass.value):
                                if subscriber.verified is True:  # change to True for production
                                    app.storage.user.update(
                                        {'email': sub_email.value, 'authenticated': True, 'is_admin': False})
                                    print('user authenticated', authenticated)
                                    await session.rollback()
                                    ui.notify('Login Successful', color='positive')

                    three_tab = ui.tab_panel(three)
                    with three_tab:
                        with ui.column().classes('items-center'):
                            with ui.card().classes('w-96 ml-10'):
                                ui.label('Login').classes('text-xl h-full')
                                sub_email = ui.input('User Email').classes('w-full')
                                sub_pass = ui.input('Password', password=True, password_toggle_button=True)\
                                    .classes('w-full')
                                ui.button('Log in', on_click=login_subscriber).classes('w-full')
                            with ui.row():
                                ui.link('Forgot Password?').classes('w-full')

