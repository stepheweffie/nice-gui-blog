import asyncio
from nicegui import ui, events
import httpx
from typing import Optional

api = httpx.AsyncClient()
running_query: Optional[asyncio.Task] = None


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
                .props('autofocus clearable rounded outlined item-aligned input-class="ml-3"') \
                .classes('fit transition-all mb-5')

            # Create a row for the search results
            with ui.scroll_area().classes('h-96 w-96').style('margin-top: -30px; margin-left: -10px;'):
                results = ui.column().classes('full-width')