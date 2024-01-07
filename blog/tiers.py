from nicegui import ui, app
from models import Post


def main_tiers_list(sub_tier):
    tier_posts = []
    with app.storage.user as session:
        if sub_tier == 1:
            tier_posts = session.query(Post).filter(
                Post.is_visible_to_subscribers is True,
                tier_posts.append([Post.title, Post.content])
            ).all()
        if sub_tier == 2:
            tier_posts = session.query(Post).filter(
                Post.is_visible_to_subscribers_with_tier_2 is True,
                tier_posts.append([Post.title, Post.content])
            ).all()
        if sub_tier == 3:
            tier_posts = session.query(Post).filter(
                Post.is_visible_to_subscribers_with_tier_3 is True,
                tier_posts.append([Post.title, Post.content])
            ).all()

    ui.label(f'Tier {sub_tier}').classes('text-h3')
    with ui.row():
        with ui.column():
            with ui.scroll_area():
                [ui.label(f'{title[0]}').classes('text-h3') for title in [tier_posts]]


