#!/usr/bin/env python3
import json
from nicegui import ui, app, Client
from sqlalchemy import delete, select
from models import User, Post, Theme
from sqlalchemy.exc import SQLAlchemyError
import os
# from utils import is_light_color
from db_utils import async_session
import webbrowser
from dash_settings import dash_theme_colors, _bg_color, dark_bg_color, toggle_dark_mode, set_modal_bg, \
    generate_bg, modal_design, call_sub_table, new_theme, new_theme_colors, theme_df, current_theme, get_background
from contextlib import contextmanager
from modals_utils import post_create_media, theme_editor, dict_update, theme_edit, generate
from editor import vue_html_content, vue_js_script
import datetime
# from collections import Counter
# import polars as pl

app_url = 'http://localhost:8080'
UPLOAD_DIR = 'uploads'
app.add_media_files('/uploads', UPLOAD_DIR)
app.add_static_files('/static/highlight-css', 'static/highlight-css')
app.add_static_files('/static/python', 'static/python')
app.add_static_files('/ace', 'ace')
app.add_static_files('/ace/src-min', 'ace/src-min')
app.add_static_files('/static/js', 'static/js')
app.add_static_files('/static/css', 'static/css')
app.add_static_files('/static/html', 'static/html')
app.add_static_files('/static/images', 'static/images')
js_templates = os.listdir('ace/src-min')
ace = js_templates.index('ace.js')
js_templates.pop(ace)
js_templates.insert(0, 'ace.js')
ace = os.path.join('/ace/src-min', js_templates[0])
dash_bg = 'assets/images/dashboard.svg'
bg_classes = 'w-3/4 h-full'
bg_style = 'z-index: -99'
bg_props = 'preserveAspectRatio="none"'


@contextmanager
def dash_frame(df):
    """Custom page frame to share the same styling and behavior across pages"""
    # Load Theme Colors For Color Classes
    the_df = new_theme(new_theme_colors, df)
    print(the_df)
    colors_dict = the_df[-1].to_dict(as_series=False)
    colors = {k: v[-1] for k, v in colors_dict.items()}
    ui.colors(**colors)
    # Load Background
    set_body_bg = get_background()
    style = f'background-color: {set_body_bg}'
    generate_bg(style)
    with ui.column():
        yield


async def editor_js():
    editor = await ui.run_javascript(vue_js_script)


def create_dashboard() -> None:
    @ui.page('/editor')
    async def editor_page(client: Client):
        with ui.row().classes('items-top'):
            await client.connected()
            webbrowser.open(f'{app_url}/ace/edit_code.html')

    @ui.refreshable
    async def list_of_users() -> None:

        async def delete_user(user_id: int) -> None:
            async with async_session() as session:
                await session.execute(delete(User).where(User.id == user_id))
                await session.commit()
            list_of_users.refresh()

        async with async_session() as session:
            result = await session.execute(select(User))
            users = result.scalars().all()

        for user in reversed(users):
            with ui.card().classes('m-4'):
                with ui.row().classes('items-center'):
                    ui.label('Name:')
                    ui.html(f"<h3>{user.name}</h3>")
                    ui.label('Email:')
                    ui.html(f"<h3>{user.email}</h3>")
                    ui.label('Admin:')
                    ui.html(f"<h3>{user.is_admin}</h3>")
                    ui.button(icon='delete', on_click=lambda u=user: delete_user(u.id)).props('flat')

    @ui.refreshable
    async def list_of_posts() -> None:
        async def delete_post(post_id: int) -> None:
            async with async_session() as session:
                await session.execute(delete(Post).where(Post.id == post_id))
                await session.commit()
            list_of_posts.refresh()

        async with async_session() as session:
            result = await session.execute(select(Post))
            posts = result.scalars().all()

        for post in reversed(posts):
            with ui.card().classes('m-4'):
                with ui.row().classes('items-center'):
                    ui.label('Title:')
                    ui.html(f"<h3>{post.title}</h3>")
                    # ui.button(icon='edit', on_click=lambda p=post: post_edit_modal(p)).props('flat')
                    ui.label('User:')
                    ui.html(f"<h3>{post.author}</h3>")
                    ui.label('Draft:')
                    ui.html(f"<h3>{post.is_draft}</h3>")
                    ui.label('Published:')
                    ui.html(f"<h3>{post.is_published}</h3>")
                    ui.button(icon='delete', on_click=lambda u=post: delete_post(u.id)).props('flat')

    @ui.refreshable
    async def list_of_themes(vals: dict) -> None:
        async def delete_theme(theme_id: int) -> None:
            async with async_session() as session:
                await session.execute(delete(Theme).where(Theme.id == theme_id))
                await session.commit()
            list_of_themes.refresh()

        async with async_session() as session:
            result = await session.execute(select(Theme))
            themes = result.scalars().all()

            def on_theme_select(event):
                selected_theme_name = event.value
                selected_theme = next((theme for theme in themes if theme.name == selected_theme_name), None)
                if selected_theme:
                    # Assuming you want to update vals with the selected theme's colors
                    dict_update(vals, selected_theme_name)

            with ui.column():
                theme_dropdown = ui.select([theme.name for theme in themes])
                vals = new_theme_colors
                theme_dropdown.on("change", on_theme_select).classes('m-4')

            theme_edit()

            with ui.expansion('Expand Color Palette'):
                with ui.column().classes('col-12'):
                    for cc, v in vals.items():
                        vals[cc] = v
                        theme_editor(cc, v, vals)

    @ui.page('/dashboard')
    async def dash(client: Client):
        with dash_frame(theme_df):
            ui.add_head_html('<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet">')
            dark = ui.dark_mode(on_change=lambda v: set_modal_bg(dark_bg_color if v.value else _bg_color))
            bg_modal = ui.element('modal')
            modal = ui.element('modal').classes('rounded-lg shadow-lg').style(
                'min-width: 70%; z-index: 999;')
            with ui.left_drawer(top_corner=True, bottom_corner=True).classes('w-full') as left_drawer:
                with ui.column().classes('w-full items-left px-4'):
                    with ui.row().classes('items-left').style('position: relative; width: 100%;'):
                        dark_mode_switch = ui.switch('Dark Mode', value=False).classes('text-xl font-bold').props(
                            'inline color=accent')
                        sun = ui.element('i').classes('eva eva-sun').classes('text-5xl')
                        moon = ui.element('i').classes('eva eva-moon').classes('text-5xl')
                        dark_mode_switch.on('change', lambda e: toggle_dark_mode(e, bg_modal))
                        dark_mode_switch.on('click', lambda e: dark.toggle())
                        moon.bind_visibility_from(dark_mode_switch, 'value', backward=lambda v: v)
                        sun.bind_visibility_from(dark_mode_switch, 'value', backward=lambda v: not v)

            async def create_user(name, email, password, admin) -> None:
                new_user = User()
                new_user.create_user(name, email, password, admin)
                async with async_session() as session:
                    session.add(new_user)
                    try:
                        await session.commit()
                        list_of_users.refresh()
                    except SQLAlchemyError as e:
                        ui.notify(f'Error creating user: {str(e)}', level='error')
                        await session.rollback()

            async def create_post(title, user, published, draft) -> None:
                new_post = Post()
                new_post.create_post(title, user, published, draft)
                async with async_session() as session:
                    session.add(new_post)
                    try:
                        await session.commit()
                        list_of_posts.refresh()

                    except SQLAlchemyError as e:
                        ui.notify(f'Error creating post: {str(e)}', level='error')
                        await session.rollback()

            async def edit_post(title, content, draft) -> None:
                edit_post = Post()
                edit_post.edit_post(title, content, draft)
                async with async_session() as session:
                    session.add(edit_post)
                    try:
                        await session.commit()
                        list_of_posts.refresh()

                    except SQLAlchemyError as e:
                        ui.notify(f'Error editing post: {str(e)}', level='error')
                        await session.rollback()

            async def create_theme(name, t_dict) -> None:
                new_theme = Theme()
                new_theme.name = name
                new_theme.created_on = datetime.datetime.now()

                for key, value in t_dict.items():
                    if hasattr(new_theme, key):
                        setattr(new_theme, key, value)

                async with async_session() as session:
                    session.add(new_theme)
                    try:
                        await session.commit()
                        list_of_themes.refresh()
                    except SQLAlchemyError as e:
                        ui.notify(f'Error creating theme: {str(e)}', level='error')
                        await session.rollback()

            async def user_modal() -> None:
                with bg_modal:
                    # Without a new modal the modal will not close
                    bg = toggle_dark_mode(dark_mode_switch.value, bg_modal)
                    with ui.row().classes('full-width').style(add='position: sticky; max-height: fit-content;'):
                        with modal and bg:
                            bg.style(add='position: absolute; max-width: 96%;'
                                         'margin-top: 40px;')
                            close = ui.icon('close').classes('text-2xl')
                            close.on("click", lambda: bg_modal.remove(bg))
                            build = ui.column().classes('mx-auto p-4')
                            with build:
                                ui.label('Create User').classes('text-4xl m-4')
                                with ui.row().classes('w-full items-center px-4'):
                                    name = ui.input(label='Name')
                                    email = ui.input(label='Email')
                                    password = ui.input(label='Password', password=True)
                                    admin = ui.checkbox('Is Admin')
                                    ui.button('Create User',
                                              on_click=lambda: create_user(name.value, email.value, password.value,
                                                                           admin.value))

                                await list_of_users()
                                list_of_users.refresh()

            async def post_create_modal(client: Client) -> None:
                # await client.connected()
                with bg_modal:
                    # Without a new modal the modal will not close
                    bg = toggle_dark_mode(dark_mode_switch.value, bg_modal)
                    with ui.row().classes('full-width').style(add='position: sticky; max-height: fit-content;'):
                        with modal and bg:

                            bg.style(add='position: absolute; max-width: 94%;'
                                         'margin-top: 40px;')

                            close = ui.icon('close').classes('text-2xl')
                            close.on("click", lambda: bg_modal.remove(bg))
                            build = ui.column().classes('mx-auto p-4')
                            with build:
                                ui.label('Create Post').classes('text-4xl m-4')
                                usable_row = ui.row().classes('w-full items-center px-4')
                                with ui.column().classes('mx-auto p-4 w-full items-left'):
                                    with usable_row:
                                        title = ui.input(label='Title')
                                        title.style(replace='width: 80%;')
                                    with usable_row:
                                        user = ui.input(label='Author')
                                        user.style(replace='width: 60%;')
                                        published = ui.checkbox('Is Published')
                                        draft = ui.checkbox('Is Draft')
                                        with usable_row:
                                            ui.button("Save Post", icon='save', on_click=lambda: create_post(
                                                user=user.value, title=title.value, published=published.value,
                                                draft=draft.value
                                            )).classes(
                                                'mx-5 mb-5 w-full')
                                    with usable_row:
                                        post_create_media()

                                    # Text Editor Tools
                                    with usable_row:
                                        with ui.expansion("WSIWYG Editor", icon='editor').classes('w-full ml-5'):
                                            ui.html(vue_html_content)
                                            await editor_js()

            async def post_edit_modal() -> None:
                with bg_modal:
                    # Without a new modal the modal will not close
                    bg = toggle_dark_mode(dark_mode_switch.value, bg_modal)
                    with ui.row().classes('full-width').style(add='position: sticky; max-height: fit-content;'):
                        with modal and bg:
                            bg.style(add='position: absolute; max-width: 96%; '
                                         'margin-top: 40px;')
                            close = ui.icon('close').classes('text-2xl')
                            close.on("click", lambda: bg_modal.remove(bg))
                            build = ui.column().classes('mx-auto p-4')
                            with build:
                                with ui.column().classes('w-full mx-auto px-4'):
                                    ui.label('Edit Post').classes('text-4xl')
                                    await list_of_posts()
                                    list_of_posts.refresh()
                                date = datetime.datetime.now()
                                with ui.input('Date').bind_value(globals(), 'date') as date_input:
                                    with ui.menu() as menu:
                                        ui.date(on_change=lambda: ui.notify(f'Date: {date}')).bind_value(date_input)
                                    with date_input.add_slot('append'):
                                        ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')
                                with ui.row().classes('full-width items-center px-4'):
                                    # HTML Template Expansion
                                    ui.label('Templates').classes('text-2xl')
                                    # add expansion from import
                            with ui.row().classes('w-full items-center px-4 mx-auto'):
                                ui.button('Save Post',
                                          on_click=lambda: edit_post(post=list_of_posts()[0])).classes(
                                    'bg-primary text-white font-bold py-2 px-4 rounded mb-5 ml-5')

            async def read_posts() -> None:
                with bg_modal:
                    # Without a new modal the modal will not close
                    bg = toggle_dark_mode(dark_mode_switch.value, bg_modal)
                    with ui.row().classes('full-width').style(add='position: sticky; max-height: fit-content;'):

                        with modal and bg:
                            bg.style(add='position: absolute; max-width: 96%; '
                                         'margin-top: 40px;')
                            close = ui.icon('close').classes('text-2xl')
                            close.on("click", lambda: bg_modal.remove(bg))
                            build = ui.column().classes('mx-auto p-4')
                            with build:
                                ui.label('Read Posts').classes('text-2xl font-bold')
                                with ui.row().classes('w-full items-center px-4'):
                                    await list_of_posts()
                                    list_of_posts.refresh()

            async def create_theme_modal():
                with bg_modal:
                    values = {}
                    # Without a new modal the modal will not close
                    bg = toggle_dark_mode(dark_mode_switch.value, bg_modal)
                    with ui.row().classes('full-width').style(add='position: sticky; max-height: fit-content;'):
                        with modal and bg:
                            bg.style(add='position: absolute; max-width: 96%; '
                                         'margin-top: 40px;')
                            close = ui.icon('close').classes('text-2xl')
                            close.on("click", lambda: bg_modal.remove(bg))
                            build = ui.column().classes('mx-auto p-4')
                            with build:
                                with ui.row().classes('w-full px-4'):
                                    ui.label('Create A Theme').classes('text-4xl')
                                    ui.button('Generate', on_click=lambda: generate_theme()).classes('text-2xl')

                                with ui.row():
                                    with build.classes('w-full'):
                                        await list_of_themes(values)
                                        list_of_themes.refresh(values)

                            def generate_theme():
                                with bg_modal:
                                    # Without a new modal the modal will not close
                                    bg = toggle_dark_mode(dark_mode_switch.value, bg_modal)
                                    with ui.row().classes('full-width').style(
                                            add='position: sticky; max-height: fit-content;'):
                                        with modal and bg:
                                            bg.style(add='position: absolute; max-width: 96%; '
                                                         'margin-top: 40px;')
                                            close = ui.icon('close').classes('text-2xl')
                                            close.on("click", lambda: bg_modal.remove(bg))
                                            build = ui.column().classes('mx-auto p-4')
                                            with build:
                                                name = ui.input('Enter Theme Name').classes('text-2xl')
                                                with ui.row():
                                                    cancel = ui.button('Cancel').classes('text-2xl')
                                                    cancel.on("click", lambda: bg_modal.remove(bg))

                                                    save = ui.button('Save').classes('text-2xl')
                                                    save.on('click', lambda: generate(name.value))

            with left_drawer:
                with ui.button('', icon='person', on_click=user_modal).classes(
                        'w-full text-lg font-bold py-2 px-4 rounded'):
                    ui.label('Manage Users').classes('m-1')

                with ui.button("", icon='add', on_click=post_create_modal).classes(
                        'w-full text-lg font-bold py-2 px-4 rounded'):
                    ui.label('Create Post').classes('m-1')

                with ui.button("", icon='build', on_click=post_edit_modal).classes(
                        'w-full text-lg py-2 px-4 rounded font-bold'):
                    ui.label('Edit Posts ').classes('m-1')

                with ui.button("", icon='newspaper', on_click=read_posts).classes(
                        'w-full text-lg font-bold py-2 px-4 rounded'):
                    ui.label('Review Posts ').classes('m-1')

                open_editor = ui.button('', icon='edit', on_click=lambda: ui.open(editor_page, new_tab=True))
                with open_editor:
                    ui.label('Code Editor').classes('m-1')
                    open_editor.classes('w-full text-lg font-bold py-2 px-4 rounded')

                open_settings = ui.button('', icon='settings', on_click=lambda: settings_drawer.toggle())
                with open_settings:
                    ui.label('Settings').classes('m-1')
                    open_settings.classes('w-full text-lg font-bold py-2 px-4 rounded')

                open_theme = ui.button('', icon='dashboard', on_click=create_theme_modal).classes(
                    'w-full text-lg font-bold py-2 px-4 rounded')
                with open_theme:
                    ui.label('Create a Theme').classes('m-1')
                    open_theme.classes('w-full text-lg font-bold py-2 px-4 rounded')

                with ui.button('', icon='lock').classes('w-full text-lg font-bold py-2 px-4 rounded'):
                    ui.label('Logout').classes('m-1').on('click', lambda: ui.open('/logout'))

            async def save_theme(theme_dict):
                theme_dict.update()
                with bg_modal:
                    # Without a new modal the modal will not close
                    bg = toggle_dark_mode(dark_mode_switch.value, bg_modal)
                    with ui.row().classes('full-width'):
                        with modal and bg:
                            bg.style(add='position: fixed; max-width: 200%; left: 35%')
                            close = ui.icon('close').classes('text-2xl')
                            close.on("click", lambda: bg_modal.remove(bg))
                            build = ui.column().classes('mx-auto p-20')
                            with build:
                                ui.label('Save Your Theme').classes('text-4xl').on('keydown_enter',
                                                                                   lambda e: save_json( theme_df))\
                                    .classes('text-xl w-72')
                                ui.button('Save', on_click= save_json()).classes('full-width')

            def save_json(theme_dict):
                # theme_dict = _df[-1].to_dict()
                # theme_dict = prepare_dict_for_json(theme_dict)
                new_colors = {"theme": f'{current_theme}', "classes": theme_dict}
                with open('theme.json', 'w') as f:
                    json.dump(new_colors, f, indent=4)
                    dash_frame()
                    new_theme(theme_df, theme_dict)

            with ui.right_drawer(top_corner=True, bottom_corner=True, value=False).props('bordered') as settings_drawer:
                with settings_drawer.classes('items-left'):
                    with ui.scroll_area().classes('w-full h-full pr-3'):
                        ui.label('Theme').classes('text-2xl w-full')
                        with ui.expansion('Edit Theme Colors', icon='color_lens').classes('w-full text-xl'):
                            with ui.column().classes('w-full'):
                                save_ = ui.button("Save Theme").classes('text-lg w-56 q-btn')
                                save_.on('click', lambda: save_theme(new_theme_colors))
                                if not os.path.exists('theme.json'):
                                    # add default colors
                                    theme_data = {
                                        "theme": "Dak Bold",
                                        "classes": {
                                            "primary": dash_theme_colors["primary"],
                                            "secondary": dash_theme_colors["secondary"],
                                            "accent": dash_theme_colors["accent"],
                                            "positive": dash_theme_colors["positive"],
                                            "negative": dash_theme_colors["negative"],
                                            "info": dash_theme_colors["info"],
                                            "warning": dash_theme_colors["warning"],
                                            "dark": dash_theme_colors["dark"],
                                        }}
                                    with open('theme.json', 'w') as file:
                                        json.dump(theme_data, file, indent=4)

                                for cc, v in new_theme_colors.items():
                                    # new_theme_colors[cc] = v
                                    theme_editor(cc, v, new_theme_colors)

                        with ui.expansion('Modal Colors', icon='brush').classes('w-full text-xl'):
                            with ui.column().classes('w-full'):
                                ui.button('Design', on_click=modal_design).classes('text-lg w-56 q-btn')

                        ui.label('Fonts').classes('text-2xl')
                        with ui.expansion(f'Change Fonts', icon='font_download').classes('w-full text-xl'):
                            with ui.column():
                                ui.button('Font Family').classes('text-lg w-56 q-btn')
                                ui.button('Font Weight').classes('text-lg w-56 q-btn')
                                ui.button('Font Size').classes('text-lg w-56 q-btn')

                        ui.label('Logo').classes('text-2xl')
                        with ui.expansion('Upload', icon='diamond').classes('w-full text-xl'):
                            with ui.column():
                                ui.upload(label='Upload Logo', auto_upload=True).classes('w-56')
                                ui.button('Save Logo').classes('text-lg w-56 q-btn')

                        ui.label('Layout').classes('text-2xl')
                        with ui.expansion('Use Template', icon='view_sidebar').classes('w-full text-xl'):
                            with ui.column():
                                ui.button('Change Template').classes('text-lg w-56 q-btn')

                        ui.label('Account').classes('text-2xl w-full')
                        with ui.expansion('Security', icon='security').classes('w-full text-xl'):
                            with ui.column().classes('w-full'):
                                ui.button('Manage Account').classes('text-lg w-56 q-btn')
                        with ui.expansion('Subscribers', icon='face').classes('w-full text-xl'):
                            with ui.column().classes('w-full'):
                                ui.button('Manage Subscribers', on_click=call_sub_table).classes('text-lg w-56 qq-btn')
                        with ui.expansion('Tier Subs', icon='people').classes('w-full text-xl'):
                            with ui.column().classes('w-full'):
                                ui.button('Tier One').classes('text-lg w-56')
                                ui.button('Tier Two').classes('text-lg w-56')
                                ui.button('Tier Three').classes('text-lg w-56')



