from nicegui import ui, events
import os
# from PIL import Image
from collections import Counter
from utils import allowed_file
cnt_theme = Counter()

add = ui.button('', icon='add').classes('text-md').style('margin-bottom: 280px;' 'margin-left: 10px;' 
                                                         'margin-top: -15px;')


def post_create_media():
    # Media Files Expansion
    with ui.expansion('Media Files', icon='image').classes('w-full'):
        ui.label('Add Media Files').classes('text-2xl')
        with ui.row().classes('flex w-full'):
            ui.label('Upload Files').classes('m-3 mr-40 text-2xl')
            with ui.column().classes('w-full'):
                # from utils import handle_upload
                with ui.scroll_area().classes('border'):
                    upload = ui.upload(label='Choose a file', auto_upload=True, on_upload=handle_upload)
                    ui.label('Tags for Media').classes('m-3 text-2xl')


def theme_editor(cc, v, vals):
    with ui.element('div').classes('columns-2'):
        theme_picker = ui.row().classes('justify-start mx-auto')
        palette_picker = ui.row().classes('justify-start mx-auto')
        with ui.column().classes('col-6'):
            with theme_picker:
                color_input = ui.color_input(f'', value=v, on_change=lambda e: update_card_color(e))
                color_input.classes('text-xl mb-0 ml-2')
                ui.label(f'{cc}').classes('text-2xl').style('display: block;'
                                                            'width: 120px;'
                                                            'flex-wrap: wrap;'
                                                          )
        with ui.column().classes('col-6'):
            with palette_picker:
                with ui.element('div').classes('full-width').style('display: block;'
                                                                   'height: 88px;'
                                                                   'flex-wrap: wrap;'
                                                                   'align-content: center;'):
                    color_card = ui.card().style(f'background-color: {v};'
                                                 ).classes('mb-0')

        def update_card_color(e):
            # vals refreshes with the page for a preview of the theme even in Settings drawer
            new_color = e.value
            color_card.style(f'background-color: {new_color};')
            vals[cc] = new_color
            return vals


def remove_picker_palette(counter):
    counter['themes'] -= 1
    return counter


def revert_picker_palette(counter):
    counter['themes'] = 0
    return counter


def apply_picker_palette(counter):
    counter['themes'] = 0
    return counter


def palette_generator(counter):
    theme_col = ui.column().classes('col-12 mt-7')
    with theme_col:
        color_card = ui.card().classes('pb-0 pt-0 mt-5 border-[3px] border-white')
        if counter['themes'] == 1:
            color_card.style('margin-left: 30px; margin-right: 30px;')
        if counter['themes'] == 2:
            color_card.style('margin-right: 20px; margin-left: 20px; margin-top: 30px;')
        if counter['themes'] > 2:
            theme_col.classes('m-78')
        with color_card:
            with ui.row().classes('items-center justify-between mt-3 mb-0'):
                with ui.column().classes('mt-0 mb-0 ml-3'):
                    primary_div = ui.element('div').classes('bg-primary').style('display: block; margin-left: -15px; '
                                                                                'margin-bottom: -10px; '
                                                                                'padding: 50px;')
                    secondary_div = ui.element('div').classes('bg-secondary').style('display: block; '
                                                                                    'margin-left: -15px; '
                                                                                    'margin-top: -4px;   '
                                                                                    'padding: 50px;')
                with ui.column().classes('mt-0'):
                    accent_div = ui.element('div').classes('bg-accent').style('display: block; margin-left: -15px; '
                                                                              'margin-bottom: -10px;'
                                                                              'padding: 50px;')
                    positive_div = ui.element('div').classes('bg-positive').style('display: flex; margin-left: -15px; '
                                                                                  'margin-top: -4px;'
                                                                                  'padding: 50px;')
                with ui.column().classes('mt-0'):
                    negative_div = ui.element('div').classes('p-12 bg-negative').style('display: block; '
                                                                                       'margin-left: -15px; '
                                                                                       'margin-bottom: -10px;'
                                                                                       'padding: 50px;')
                    info_div = ui.element('div').classes('p-12 bg-info').style('display: block; margin-left: -15px; '
                                                                               'margin-top: -4px;'
                                                                               'padding: 50px;')
                with ui.column().classes('mt-0'):
                    warning_div = ui.element('div').classes('p-12 bg-warning').style('display: block; '
                                                                                     'margin-left: -15px; '
                                                                                     'margin-bottom: -10px;'
                                                                                     'padding: 50px;')
                    dark_div = ui.element('div').classes('p-12 bg-dark').style('display: block; margin-left: -15px; '
                                                                               'margin-top: -4px;'
                                                                               'padding: 50px; ')

            with ui.row().classes('pl-0').style('margin-top: -15px;'):
                name_theme = ui.input(placeholder='Name Theme').classes('w-48')
                select_class = ui.select(['primary', 'secondary', 'accent', 'positive', 'negative', 'info',
                                          'warning', 'dark'], value='primary').classes('w-28')

                theme_select_btn = ui.button('', icon='menu').classes(
                    'text-lg ml-1 mr-0 mt-2 mb-2 bg-accent')
                with theme_select_btn:
                    with ui.menu().style('display: flex;'
                                         'max-width: 100%;'
                                         'flex-wrap: wrap;'
                                         ):
                        ui.menu_item('Save Theme', on_click=color_card.update()).classes('w-1/2')
                        # ui.separator()
                        # ui.menu_item('Add Theme')  # Click add button
                        ui.separator()
                        ui.menu_item('Apply Theme', on_click=apply_picker_palette(cnt_theme)).classes('w-1/2')
                        ui.separator()
                        ui.menu_item('Revert Theme', on_click=revert_picker_palette(cnt_theme)).classes('w-1/2')
                        ui.separator()
                        ui.menu_item('Close Theme', on_click=remove_picker_palette(cnt_theme)).classes('w-1/2')

            theme_select_btn.on('click', lambda: add_border(color_card))

            def add_border(card):
                with card:
                    new_border = '3px solid yellow'
                    card.style(f'border: {new_border};')


def add_picker_palette():
    open_themes = 'themes'
    cnt_theme[open_themes] += 1
    palette_generator(cnt_theme)
    return cnt_theme


def theme_edit():
    global add
    with ui.element('div').classes('col-12').style('display: flex;'
                                                   'max-width: 100%;'
                                                   'flex-wrap: wrap;'
                                                  ):

        palette_picker = ui.column().classes('col-6 mr-4').style('border: 0px solid black;')
        with palette_picker:
            add_picker_palette()
            add.on('click', add_picker_palette)


def load__theme(values):
    with ui.row().classes('w-full px-4'):
        ui.button('Load Theme', on_click=lambda: load_theme(d=values)).classes('text-2xl')

    def load_theme(d):
        print(d)
        pass


def generate(theme_name):
    # use the theme_name to conjur related moods and palettes
    pass


def apply_revert_theme(values):
    with ui.row():
        ui.button('Apply Theme', on_click=lambda: apply_theme(d=values)).classes('text-2xl')
        ui.button('Revert Theme', on_click=lambda: revert_theme(d=values)).classes('text-2xl')

    def apply_theme(d):
        pass

    def revert_theme(d):
        print(d)
        pass


def dict_update(d, theme):
    # get the theme by name and populate the d.update
    d.update()


def dict_default(d):
    # get the default dict theme
    pass


def get_file_type(file_path):
    _, ext = os.path.splitext(file_path)
    return ext.lower()


def build_html_tag(file_path):
    file_type = get_file_type(file_path)
    if file_type in ['.jpg', '.jpeg', '.png', '.gif', 'svg']:
        return f'<img src="{file_path}" />'
    elif file_type in ['.mp4', '.webm', '.mov']:
        return f'<video controls><source src="{file_path}"'
    elif file_type in ['.wav', '.mp3']:
        return f'<audio src=f"{file_type}">'
    elif file_type in ['.md', '.html', '.txt']:
        with open(file_path, 'rb') as file:
            file_string = file.read
        return f'<div>"{file_string}"</div>'
    else:
        return 'Unsupported file type'


async def handle_upload(args: events.UploadEventArguments):
    if allowed_file(args.name):
        file_path = 'uploads/' + args.name
        with open(file_path, 'wb') as f:
            f.write(args.content.read())
        ui.notify(f'File uploaded: {args.name}')
        html_tag = build_html_tag(file_path)
        ui.code(html_tag, language='html')

    else:
        ui.notify('File format not allowed', level='error')


def assets_expansion():
    with ui.expansion('Edit Assets', icon='code').classes('full-width mb-8'):
        ui.label('Asset Files').classes('text-2xl')
        with ui.tabs().classes('w-full') as tabs:
            one = ui.tab('HTML')
            two = ui.tab('CSS')
            three = ui.tab('JS')
            templates = os.listdir('static/html')
            css_templates = os.listdir('static/css')
            js_templates = os.listdir('static/js')

        with ui.tab_panels(tabs, value=three).classes('full-width'):
            with ui.tab_panel(one).style(replace='max-width: 100%'):
                with ui.row().classes('w-full items-center px-4').style(
                        replace='max-width: 1000px'):
                    chosen = ui.select(options=js_templates, value=js_templates[0]) \
                        .style('width: 50%;')
                    # ui.button('Edit JS', on_click=lambda: ui.open(editor_page,
                    #                                              new_tab=True))
                    # add_code = ui.button('Add To Post', on_click=lambda:
                    # edit_post(chosen.value))

                    with open(f'static/js/{chosen.value}', 'r') as f:
                        js = f.read()
                    code = ui.code(js, language='js').style(
                        replace='max-width: 100%; min-height: 300px;')

