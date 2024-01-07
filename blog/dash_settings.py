from nicegui import ui
from dotenv import load_dotenv
from sub_table import sub_table
import polars as pl
import json

load_dotenv()

bg_modal = ui.element('modal')
modal = ui.element('modal').classes('rounded-lg shadow-lg').style(
    'min-width: 70%; z-index: 999; position: fixed;')

dash_theme_colors = {'primary': '#000000', 'secondary': '#f500d0', 'accent': '#9e14f5', 'positive': '#d0ff63',
                     'negative': '#fc3048', 'info': '#00fff7', 'warning': '#f3f700', 'dark': '#1d1d1d',
                     }
modal_colors = {'bg_color': 'rgba(5, 255, 255, 0.9)', 'text_color': 'black',
                'dark_bg_color': 'rgba(0, 0, 0, 0.9)', 'dark_text_color': 'white'}
default_colors = {}

dark = ui.dark_mode(on_change=lambda v: set_modal_bg(dark_bg_color if v.value else _bg_color))
new_modal_colors = {}
_bg_color = modal_colors['bg_color']
dark_bg_color = modal_colors['dark_bg_color']
_text_color = modal_colors['text_color']
dark_text_color = modal_colors['dark_text_color']

current_theme = 'Dark Bold'

with open('theme.json', 'r') as file:
    colors = json.load(file)
    if colors.get("theme") == current_theme:
        theme_classes = colors['classes']
    new_theme_colors = theme_classes
    theme_df = pl.DataFrame({k: pl.Series(dtype=pl.Utf8) for k in new_theme_colors.keys()})

select1 = ui.select(
                    ['pink', 'red', 'purple', 'deep-purple', 'indigo', 'blue', 'light-blue', 'cyan', 'orange',
                     'teal', 'green', 'light-green', 'lime', 'yellow', 'amber', 'orange', 'deep-orange', 'brown',
                     'grey', 'blue-grey'], value='pink')
select2 = ui.select([i for i in range(14)])


def new_theme(the_dict, the_df):
    global theme_df
    if the_df.height == 0:
        the_df = pl.DataFrame({k: pl.Series(dtype=pl.Utf8) for k in the_dict.keys()})
    if len(the_df) == 0:
        new_row_df = pl.DataFrame([the_dict])
        the_df = the_df.vstack(new_row_df)
    for column_name, new_value in the_dict.items():
        if column_name in the_df.columns:
            the_df = the_df.with_columns(
                pl.lit(new_value).alias(column_name)
            )
    print(the_df)
    return the_df


def update_theme(key,  color, theme_dict):
    key = key.lower()
    theme_dict[key] = color
    return theme_dict


def get_background():
    with open('theme.json', 'r') as file:
        bg = json.load(file)
        print(bg)
        if bg.get("theme") == current_theme:
            theme_bg = bg['background']['bg-color']
        return theme_bg


def toggle_dark_mode(switch_state, _modal):
    _bg_color = modal_colors['bg_color']
    bg_color = f'{dark_bg_color}' if switch_state is True else f'{_bg_color}'
    text_color = f'{dark_text_color}' if switch_state is True else f'{_text_color}'
    _modal = ui.element('modal').classes('rounded-lg shadow-lg').style(
    f'z-index: 666; background-color: {bg_color}; color: {text_color};')
    return _modal


def set_modal_bg(color: str) -> None:
    ui.query('modal').style(replace=f'background-color: {color}')
    modal_colors['bg_color'] = color
    if color is dark_bg_color:
        ui.query('modal').style(replace=f'color: {dark_text_color}')
    else:
        ui.query('modal').style(replace=f'color: {_text_color}')


def generate_bg(bg_style):
    with ui.row().classes('w-full'):
        ui.query('body').style(bg_style)
        # header_vid = ui.video(f'/assets/images/{f}.mp4', loop=True, controls=False).classes('full-width')


def modal_design(modal1, modal2):
    bg = toggle_dark_mode(None, modal1)
    with modal2 and bg:
        ui.color_input(label='rgba', value=f'{_bg_color}',
                       on_change=lambda v:
                       set_modal_bg(v.value)).bind_value(lambda v: bg.style(replace=f'background-color: {v.value}'))
        ui.label('Dark Color').classes('text-2xl')
        ui.color_input(label='rgba', value=f'{dark_bg_color}').bind_value(
            lambda v: set_modal_bg(v.value))
        with ui.row().classes('w-full items-center px-4'):
            ui.label('Modal Text Color').classes('text-2xl')
            ui.color_input(label='rgba', value=f'{_text_color}').bind_value(
                lambda v: ui.query('modal').style(f'color: {v.value}'))
            ui.label('Dark Text Color').classes('text-2xl')
            ui.color_input(label='rgba', value=f'{dark_text_color}').bind_value(
                lambda v: ui.query('modal').style(f'color: {v.value}'))


def call_sub_table(modal1, modal2):
    with modal2:
        # Without a new modal the modal will not close
        bg = toggle_dark_mode(not dark.value, modal2)
    with modal1 and bg:
        ui.icon('close').classes('absolute top-2 left-2 cursor-pointer').on(
            'click', lambda: modal2.remove(bg)).style('z-index: 1000;')
        modal1.style(replace='max-width: 80%;')
        bg.style(
            'min-width: 70%; z-index: 999; position: fixed; top: 10%; '
            'left: 59%; transform: translate(-50%, -50%);')
        sub_table()
