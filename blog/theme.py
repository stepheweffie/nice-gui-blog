from contextlib import contextmanager
from nicegui import ui


def menu() -> None:
    ui.link('Home', '/').classes(replace='text-white')
    ui.link('A', '/a').classes(replace='text-white')
    ui.link('B', '/b').classes(replace='text-white')
    ui.link('C', '/c').classes(replace='text-white')


@contextmanager
def page_frame(navtitle: str):
    """Custom page frame to share the same styling and behavior across pages"""
    ui.colors(primary='#6E93D6', secondary='#53B689', accent='#111B1E', positive='#53B689')
    with ui.header().classes('justify-between text-white'):
        ui.label('Modularization Example').classes('font-bold')
    with ui.column().classes('absolute-center items-center'):
        yield
