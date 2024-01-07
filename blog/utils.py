from nicegui import ui, events, app
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
import json
import polars as pl
load_dotenv()

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'svg', 'pdf', 'jpeg', 'gif', 'mp4', 'mov', 'mp3', 'wav', 'txt', 'md', 'html'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def open_media(file, url):
    media = Path('media')
    media.mkdir(exist_ok=True)
    r = requests.get(f'{url}')
    (media / f'{file}').write_bytes(r.content)
    app.add_media_files('/my_videos', media)
    ui.video(f'/my_videos/{file}')


async def handle_upload(args: events.UploadEventArguments):
    if allowed_file(args.name):
        file_path = 'uploads/' + args.name
        with open(file_path, 'wb') as f:
            f.write(args.content.read())
        ui.notify(f'File uploaded: {args.name}')
        # TODO determine file type for tag
        ui.code(f'<img src="{file_path}">', language='html')
    else:
        ui.notify('File format not allowed', level='error')
    # await upload.run_method('reset')


async def handle_html_templates() -> None:
    templates = os.listdir('/assets/html')
    chosen = ui.select(options=templates, value=templates[0])
    await chosen.value()
    with open(f'/assets/html/{chosen.value}', 'r') as f:
        html = f.read()
    ui.code(html, language='html')


# Read the HTML content from the file
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def save_file(content, file_name,  file_type):
    # Determine the file extension based on the selected file type
    file_extension = ''
    if file_type == 'Text (.txt)':
        file_extension = 'txt'
    elif file_type == 'Markdown (.md)':
        file_extension = 'md'
    elif file_type == 'HTML (.html)':
        file_extension = 'html'

    # Save the content to a file
    with open(f'{file_name}.{file_extension}', 'w', encoding='utf-8') as file:
        file.write(content)
    ui.notify(f'File saved as saved_file.{file_extension}')


# Add the Vue template as a slot
def add_html_template(file):
    template_content = read_file(file)
    html = ui.html(template_content)
    return html


def is_light_color(hex_color):
    # Convert hex color to RGB
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    # Calculate luminance
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    # print(luminance)
    # If luminance is greater than 0.5, it's a light color, else it's dark
    return luminance > 0.5


def to_serializable(data):
    if isinstance(data, pl.Series):
        print(data)
        return data.to_list()
    return data


def prepare_dict_for_json(theme_dict):
    return {key: to_serializable(value) for key, value in theme_dict.items()}