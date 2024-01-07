#!/usr/bin/env python3
from typing import Optional, cast
from typing_extensions import Self
from nicegui import ui
from nicegui.binding import BindableProperty


class BlogCard(ui.card):
    blog_cards_images = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_blog_cards_images_change(value)
    )
    blog_card_aspect = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_blog_card_aspect_change(value)
    )
    blog_card_shadow = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_blog_card_shadow_change(value)
    )
    blog_card_size = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_blog_card_size_change(value)
    )
    blog_card_style = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_blog_card_style_change(value)
    )
    blog_card_row = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_blog_card_row_change(value)
    )
    blog_card_col = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_blog_card_col_change(value)
    )

    def __init__(self) -> None:
        super().__init__()
        self.blog_cards_images: Optional[list] = None
        self.blog_card_aspect: Optional[str] = None
        self.blog_card_shadow: Optional[str] = None
        self.blog_card_size: Optional[str] = None
        self.blog_card_style: Optional[str] = None
        self.blog_card_row: Optional[str] = None
        self.blog_card_col: Optional[str] = None

    def _handle_blog_cards_images_change(self, blog_cards_images: str) -> None:
        """Update the classes of the label when the button property changes."""
        self._classes = [c for c in self._classes if not c.startswith('bg-')]
        self._classes.append(blog_cards_images)
        self.update()

    def _handle_blog_card_aspect_change(self, blog_card_aspect: str) -> None:
        """Update the classes of the label when the button property changes."""
        self._classes = [c for c in self._classes if not c.startswith('aspect-')]
        self._classes.append(blog_card_aspect)
        self.update()

    def _handle_blog_card_shadow_change(self, blog_card_shadow: str) -> None:
        """Update the classes of the label when the button property changes."""
        self._classes = [c for c in self._classes if not c.startswith('shadow-', 'drop-shadow-')]
        self._classes.append(blog_card_shadow)
        self.update()

    def _handle_blog_card_size_change(self, blog_card_size: str) -> None:
        """Update the classes of the label when the button property changes."""
        self._classes = [c for c in self._classes if not c.startswith('w-', 'h-')]
        self._classes.append(blog_card_size)
        self.update()

    def _handle_blog_card_style_change(self, blog_card_style: str) -> None:
        """Update the classes of the label when the button property changes."""
        self._classes = [c for c in self._classes if not c.startswith('border-', 'rounded-')]
        self._classes.append(blog_card_style)
        self.update()

    def _handle_blog_card_row_change(self, blog_card_row: str) -> None:
        """Update the classes of the label when the button property changes."""
        self._classes = [c for c in self._classes if not c.startswith('row-')]
        self._classes.append(blog_card_row)
        self.update()

    def _handle_blog_card_col_change(self, blog_card_col: str) -> None:
        """Update the classes of the label when the button property changes."""
        self._classes = [c for c in self._classes if not c.startswith('columns-')]
        self._classes.append(blog_card_col)
        self.update()


class BlogImage(ui.image):

    background = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_background_change(value)
    )
    background_image = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_background_image_change(value)
    )

    def __init__(self, text: str = '') -> None:
        super().__init__(text)
        self.background: Optional[str] = None
        self.background_image: Optional[str] = None

    def _handle_background_change(self, background: str) -> None:
        """Update the classes of the label when the background property changes."""
        self._classes = [c for c in self._classes if not c.startswith('bg-',)]
        self._classes.append(background)
        self.update()

    def _handle_background_image_change(self, background_image: str) -> None:
        """Update the classes of the label when the background_image property changes."""
        self._classes = [c for c in self._classes if not c.startswith('gradient-to-', 'bg-')]
        self._classes.append(background_image)
        self.update()


class BlogTitle(ui.label):
    blog_titles = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_blog_title_change(value)
    )

    def __init__(self, text: str = '') -> None:
        super().__init__(text)
        self.blog_titles: Optional[list] = None

    def _handle_blog_title_change(self, blog_titles: str) -> None:
        """Update the classes of the label when the button property changes."""
        self._classes = [c for c in self._classes if not c.startswith('text-')]
        self._classes.append(blog_titles)
        self.update()


class BlogText(ui.label):
    # This class variable defines what happens when the background property changes.

    blog_card_text = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_text_change(value)
    )
    blog_card_sig = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_blog_signature_change(value)
    )
    header_texts = BindableProperty(
        on_change=lambda sender, value: cast(Self, sender)._handle_header_text_change(value)
    )

    def __init__(self, text: str = '') -> None:
        super().__init__(text)
        self.blog_card_text: Optional[list] = None
        self.header_texts: Optional[list] = None
        self.blog_card_sig: Optional[str] = None

    def _handle_blog_card_text_change(self, blog_card_text: str) -> None:
        """Update the classes of the label when the button property changes."""
        self._classes = [c for c in self._classes if not c.startswith('bg-', 'text-', 'font-')]
        self._classes.append(blog_card_text)
        self.update()

    def _handle_header_text_change(self, header_texts: str) -> None:
        """Update the classes of the label when the button property changes."""
        self._classes = [c for c in self._classes if not c.startswith('text-', 'font-')]
        self._classes.append(header_texts)
        self.update()

    def _handle_blog_signature_change(self, blog_card_sig: str) -> None:
        """Update the classes of the label when the button property changes."""
        self._classes = [c for c in self._classes if not c.startswith('text-', 'font-')]
        self._classes.append(blog_card_sig)
        self.update()

