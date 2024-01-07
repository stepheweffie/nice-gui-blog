from post_list_settings import BlogCard, BlogTitle, BlogText
import datetime
import polars as pl
import asyncio
from typing import Optional
import httpx
from nicegui import events, ui, app, Client
from models import Subscriber
from db_utils import async_session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

api = httpx.AsyncClient()
running_query: Optional[asyncio.Task] = None
app_name = 'The Blog'
brand_name = 'My Brand'
terms = 'Terms of Service'
privacy = 'Privacy Policy'

thumbnail_images = ['https://picsum.photos/id/684/640/360',
                    'https://picsum.photos/id/684/640/360',
                    'https://picsum.photos/id/684/640/360']

title_texts = ['List of Titles', 'Blog Post Titles', 'More Really Long Post Titles']

post_card_text = ['post-md-text-Lorem ipsum dolor sit amet,',
                  'consectetur adipiscing elit Nullam euismod',
                  'nisl eget aliquam lacinia,']

titles = {'Post1': f'{title_texts[0]}', 'Post2': f'{title_texts[1]}', 'Post3': f'{title_texts[2]}'}
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


def make_search_tab(search_tab: ui.tab_panel) -> None:
    with search_tab:
        ui.label('Search Posts').classes('text-xl h-full')
        with ui.column().classes('w-full h-full'):
            async def search(e: events.ValueChangeEventArguments) -> None:
                '''Search for posts as you type.'''

                global running_query
                if e.value == '':  # Check if the search bar is empty
                    results.clear()
                    return
                if running_query:
                    running_query.cancel()  # cancel the previous query; happens when you type fast
                # store the http coroutine in a task so we can cancel it later if needed
                results.clear()
                running_query = asyncio.create_task(
                    api.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={e.value}'))
                response = await running_query
                if response.text == '':
                    return
                with results:  # enter the context of the the results row
                    for drink in response.json()[
                                     'drinks'] or []:  # iterate over the response data of the api
                        with ui.image(drink['strDrinkThumb']).classes('w-64'):
                            ui.label(drink['strDrink']).classes(
                                'absolute-bottom text-subtitle2 text-center')
                running_query = None

            # Create a search field
            search_field = ui.input(on_change=search) \
                .props('autofocus clearable outlined rounded item-aligned input-class="ml-3"') \
                .classes('fit transition-all')
            # Create a row for the search results
            with ui.scroll_area().classes('h-96 w-96').style('margin-top: -30px; margin-left: -10px;'):
                results = ui.column().classes('full-width')


async def main_page(client: Client) -> None:
    authenticated = app.storage.user.get('authenticated')
    # A Scrollable Area of The Latest Posts
    if authenticated:
        ui.label(f'{brand_name}').classes('text-5xl text-center')
        ui.label(f'{app_name}').classes('text-3xl text-center')
    with ui.row().classes(f'w-full h-screen'):
        if authenticated:
            auth_card = ui.card().classes('w-full h-full')
        else:
            auth_card = ui.card().classes('w-1/2 h-full')
        with auth_card:
            with ui.scroll_area().classes('w-full h-full'):
                i = 0
                # Create a list of (title, post) pairs from the blog_cards_text dictionary
                post_card = BlogCard()
                # Display Titles, Image Cards, Signature, and Associate with Posts
                for title, image, post in zip(titles, thumbnail_images, blog_cards):
                    with post_card:
                        # post_title = BlogTitle() \
                        #    .bind_text_from(titles, title, backward=lambda: f'{title}')
                        # bind_from(self_obj=post_title, self_name='blog_titles',
                        #          other_obj=titles, other_name=title,
                        #           backward=lambda one_to_many: f'{title_text}')
                        post_card.classes(f'{card_style} {card_size} {card_aspect_ratio} {card_border_radius}')
                        ui.image(image)
                        with ui.card_section():
                            ui.label(post_sig)
                        with ui.expansion("Expand Article").classes(f'{card_text}'):
                            _text = BlogText().classes(bg_class) \
                                .bind_text_from(blog_cards, post, backward=lambda post=post: f'{post}')
                            _text.classes(f'{card_text} {post_text_color}')
                    i += 1

        # A Title and Tab Column
        if not authenticated:
            with ui.column():
                ui.label(f'{brand_name}').classes('text-5xl text-center')
                ui.label(f'{app_name}').classes('text-3xl text-center')
                subscribed = app.storage.user.get('subscribed')
                print('user authenticated', authenticated)
                print('user subscribed', subscribed)
                print('user email', app.storage.user.get('email'))

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
                                subscriber.verify_subscriber(signup_password, signup_code)
                                await session.commit()
                            except IntegrityError:
                                pass
                            app.storage.user.update('authenticated', True)
                            ui.notify('Login Successful', color='positive')
                            await session.rollback()
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
                                if subscriber.verified is False:  # change to True for production
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

