from nicegui import ui, app


def create_subscription():
    @ui.page('/subscribe')
    async def subscribe():
        if app.storage.user.get('authenticated', False):
            subscription_modal()
        subscriber_modal()


def subscription_modal():
    return True


def subscriber_modal():
    return True

