import datetime
import polars as pl
from nicegui import ui

app_name = 'NiceGUI'

thumbnail_images = ['https://picsum.photos/id/684/640/360',
                    'https://picsum.photos/id/684/640/360',
                    'https://picsum.photos/id/684/640/360']

title_texts = ['List of Titles', 'Blog Post Titles', 'More Really Long Post Titles']

post_card_text = ['post-md-text-Lorem ipsum dolor sit amet,',
                  'consectetur adipiscing elit Nullam euismod',
                  'nisl eget aliquam lacinia,']

titles = {'Post1 hhahahahahahaha': f'{title_texts[0]}', 'Post2': f'{title_texts[1]}', 'Post3': f'{title_texts[2]}'}
blog_cards = {'Post1': f'{post_card_text[0]}', 'Post2': f'{post_card_text[1]}', 'Post3': f'{post_card_text[2]}'}

post_date = datetime.datetime.now()

# Create a list of (title, image, post) pairs
post_data = [{'Title': title, 'Image': image, 'Post': post} for title, image, post in zip(titles, thumbnail_images,
                                                                                          blog_cards)]

# Create a Polars DataFrame
df = pl.DataFrame(post_data)

# Save the DataFrame as a JSON file
df.write_json('posts.json')

bg_class = 'bg-white'
card_aspect_ratio = 'aspect-video'
card_shadow = 'shadow-lg'
card_border_radius = 'rounded-lg'
card_size = 'w-full h-full'
card_style = 'text-center'
card_row = 'row-span-1'
card_col = 'col-span-1'
row_size = 'w-full, h-full'
title_text = 'text-5xl'
card_text = 'text-xl'
post_text_color = 'text-violet-600'
post_sig = f'Posted by {app_name} on ' + post_date.strftime('%B %d, %Y')


def post_preview():
    with ui.row().classes('w-full wrap mt-4'):
        auth_card = ui.card()
        for title, image, post in zip(titles, thumbnail_images, blog_cards):
            with ui.column().classes('w-full'):
                with auth_card.classes(f'{bg_class} {card_aspect_ratio} {card_shadow} {card_border_radius} '
                                       f'{card_size} {card_style} {card_row} {card_col}'):

                    # this row makes the width of the column
                    with ui.row().classes('w-full'):
                        ui.label(title).classes(f'{title_text}')
                    with ui.row().classes('w-full'):
                        ui.label(post_sig).classes(f'{card_text}')

                    with ui.row().classes('w-full h-full'):
                        ui.image(image).classes('w-full h-full')


def post_list():
    with ui.row().classes('w-full wrap flex mt-4'):
        for title, image, post in zip(titles, thumbnail_images, blog_cards):
            with ui.column().classes('xs-col-12 sm-col-12 md-col-6 lg-col-6 xl-col-6'):
                with ui.card().classes(f'{bg_class} {card_aspect_ratio} {card_shadow} {card_border_radius} '
                                       f'{card_size} {card_style} {card_row} {card_col}'):
                    ui.image(image).classes('w-full h-full')
                    with ui.column().classes('w-full h-full'):
                        with ui.row().classes('w-full h-full'):
                            with ui.column().classes('w-full h-full'):
                                with ui.card().classes('w-full h-full'):
                                    with ui.row().classes('w-full h-full'):
                                        with ui.column().classes('w-full h-full'):
                                            ui.label(title).classes(f'{title_text} {post_text_color}')
                                            ui.label(post).classes(f'{card_text} {post_text_color}')
                                            ui.label(post_sig).classes(f'{card_text} {post_text_color}')



