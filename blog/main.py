import os
from typing import Optional
from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import ui, app
from nicegui.client import Client
from starlette.middleware.base import BaseHTTPMiddleware
import asyncio
from db_utils import init_db, async_session
import dash
from sub_account import header
from post_list_layout import main_page
from models import User
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import subscribe
unrestricted_page_routes = ['/']
MENU_SWITCH = True
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
# router = APIRouter(prefix='/api')
app_url = 'http://127.0.0.1:8080'
PORT = 8080
SERVE_HTML_TEMPLATE = False


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.
    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if request.url.path in Client.page_routes.values() and request.url.path not in unrestricted_page_routes:
                app.storage.user['referrer_path'] = request.url.path  # remember where the user wanted to go
                return RedirectResponse('/')
        return await call_next(request)


app.add_middleware(AuthMiddleware)


@ui.page('/login')
def login() -> Optional[RedirectResponse]:  # type: ignore
    async def try_login() -> None:
        new_user = User()
        try:
            # This is a test admin account that will be created if it doesn't exist
            new_user.create_user('admin', 'savant@admin.com', 'secret', True)
            async with async_session() as session:
                session.add(new_user)
                await session.commit()
        except IntegrityError:
            pass
        try:
            async with async_session() as session:
                find = select(User).where(User.email == email.value)
                result = await session.execute(find)
                user = result.scalars().first()
                if user.check_password(password.value):
                    if user.verified is False:  # change to True for production
                        app.storage.user.update({'email': email.value, 'authenticated': True, 'is_admin': user.is_admin})
                        authenticated = app.storage.user.get('authenticated')
                        print('user authenticated', authenticated)
                        await session.rollback()
                        ui.open('/dashboard')
                        ui.notify('Please verify your email', color='negative')

                else:
                    ui.notify('Wrong Password', color='negative')

        except AttributeError:
            ui.notify('Redirecting', color='negative')
            ui.open('/')

    with ui.card().classes('absolute-center w-96'):
        email = ui.input('Email').on('keydown.enter', try_login).classes('full-width')
        password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter',
                                                                                       try_login).classes('full-width')
        ui.button('Log in', on_click=try_login).classes('full-width')


@ui.page(path='/')
async def index(client: Client) -> None:

    if SERVE_HTML_TEMPLATE:
        html = 'assets/html/index.html'
        with open(html, 'r') as f:
            html = f.read()
            ui.html(html)

    else:
        header()
        await main_page(client)


@ui.page('/logout')
async def logout_page() -> Optional[RedirectResponse]:
    print('logging out')
    try:
        await app.storage.user.update({'authenticated': False})
    except TypeError:
        pass
    return RedirectResponse('/login')


subscribe.create_subscription()
dash.create_dashboard()
asyncio.run(init_db())

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(uvicorn_logging_level='info', binding_refresh_interval=0.2, storage_secret='secret_key', port=PORT,
           on_air=True)
