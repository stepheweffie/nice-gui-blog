from nicegui import ui


def create_post():
    open_post_creation = ui.button('Create Post')
    with open_post_creation:
        ui.icon('add').classes('m-1')
        open_post_creation.classes('bg-black hover:bg-black-700 text-white font-bold py-2 px-4 rounded')
    return open_post_creation


def edit_post():
    open_post_edit = ui.button('Edit Post')
    with open_post_edit:
        ui.icon('build').classes('m-1')
        open_post_edit.classes('bg-black hover:bg-black-700 text-white font-bold py-2 px-4 rounded')
    return open_post_edit


def read_post():
    open_post_read = ui.button('Review Post')
    with open_post_read:
        ui.icon('read').classes('m-1')
        open_post_read.classes('bg-black hover:bg-black-700 text-white font-bold py-2 px-4 rounded')
    return open_post_read


def settings():
    open_settings = ui.button('Settings')
    with open_settings:
        ui.icon('settings').classes('m-1')
        open_settings.classes('bg-black hover:bg-black-700 text-white font-bold py-2 px-4 rounded')
    return open_settings


def logout():
    open_logout = ui.button('Logout')
    with open_logout:
        ui.icon('lock').classes('m-1')
        open_logout.classes('bg-black hover:bg-black-700 text-white font-bold py-2 px-4 rounded')
    return open_logout

