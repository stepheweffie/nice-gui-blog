from nicegui import ui, app, Client
from typing import Optional
from fastapi.responses import RedirectResponse


def create_subscription():
    @ui.page('/subscribe')
    async def subscribe(client: Client) -> Optional[RedirectResponse]:
        if app.storage.user.get('authenticated', False):
            return RedirectResponse('/')