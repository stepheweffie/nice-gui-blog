from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import bcrypt
import datetime
import random
from nicegui import ui
Base = declarative_base()
default_colors = {
                'primary': '#1976d2',
                'secondary': '#26A69A',
                'accent': '#9C27B0',
                'positive': '#21BA45',
                'negative': '#C10015',
                'info': '#31CCEC',
                'warning': '#F2C037',
                'dark': '#1d1d1d',
}


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=False, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=True)
    hash = Column(String(255), nullable=True)
    created_on = Column(DateTime, nullable=False)
    verified = Column(Boolean, default=False, nullable=True)
    is_admin = Column(Boolean, default=False, nullable=True)

    def set_password(self, password):
        self.hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.hash.encode('utf-8'))

    def create_user(self, name, email, password, is_admin=False):
        self.name = name
        self.email = email
        self.set_password(password)
        self.is_admin = is_admin
        self.created_on = datetime.datetime.now()

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")


class Post(Base):
    __tablename__ = 'posts'
    id= Column(Integer, primary_key=True)
    title = Column(String(255), unique=False, nullable=False)
    author = Column(String(255), unique=False, nullable=False)
    content = Column(String)
    markdown = Column(String)
    json = Column(JSON)
    created_on = Column(DateTime)
    edited_on = Column(DateTime)
    published_on = Column(DateTime)
    unpublished_on = Column(DateTime)
    deleted_on = Column(DateTime)
    user = relationship("User", back_populates="posts")
    user_id = Column(Integer, ForeignKey('users.id'))
    is_published = Column(Boolean, default=False, nullable=False)
    is_unpublished = Column(Boolean, default=False, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    is_draft = Column(Boolean, default=True, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    is_visible_to_admins = Column(Boolean, default=False, nullable=False)
    is_visible_to_users = Column(Boolean, default=False, nullable=False)
    is_visible_to_visitors = Column(Boolean, default=False, nullable=False)
    is_visible_to_subscribers = Column(Boolean, default=False, nullable=False)
    is_visible_to_subscribers_with_tier_2 = Column(Boolean, default=False, nullable=False)
    is_visible_to_subscribers_with_tier_3 = Column(Boolean, default=False, nullable=False)

    def create_post(self, title, user, content, draft):
        self.title = title
        self.author = user
        self.content = content
        self.is_draft = draft
        self.created_on = datetime.datetime.now()

    def edit_post(self, title, content, draft):
        self.title = title
        self.content = content
        self.is_draft = draft
        self.edited_on = datetime.datetime.now()

    def publish_post(self, featured):
        self.is_published = True
        self.is_draft = False
        self.is_featured = featured
        self.published_on = datetime.datetime.now()

    def unpublish_post(self):
        self.is_published = False
        self.is_draft = True

    def delete_post(self):
        self.is_published = False
        self.is_draft = False
        self.is_deleted = True
        self.is_visible_to_visitors = False
        self.is_visible_to_subscribers = False
        self.is_visible_to_admins = False
        self.deleted_on = datetime.datetime.now()

    def make_visible(self, admins, users, visitors, subscribers, tier_1, tier_2, tier_3):
        self.is_visible_to_admins = admins
        self.is_visible_to_users = users
        self.is_visible_to_visitors = visitors
        self.is_visible_to_subscribers = subscribers
        self.is_visible_to_subscribers_with_tier_1 = tier_1
        self.is_visible_to_subscribers_with_tier_2 = tier_2
        self.is_visible_to_subscribers_with_tier_3 = tier_3


class Theme(Base):
    __tablename__ = 'themes'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    created_on = Column(DateTime)
    primary = Column(String(7), unique=False, nullable=False)
    secondary = Column(String(7), unique=False, nullable=False)
    accent = Column(String(7), unique=False, nullable=False)
    info = Column(String(7), unique=False, nullable=False)
    negative = Column(String(7), unique=False, nullable=False)
    positive = Column(String(7), unique=False, nullable=False)
    warning = Column(String(7), unique=False, nullable=False)
    dark = Column(String(7), unique=False, nullable=False)

    def save_theme(self, name, primary, secondary, accent, info, negative, positive, warning, dark):
        self.name = name
        self.created_on = datetime.datetime.now()
        self.primary = primary
        self.secondary = secondary
        self.accent = accent
        self.info = info
        self.negative = negative
        self.positive = positive
        self.warning = warning
        self.dark = dark

        def apply_theme():
            ui.colors(primary=primary)
            ui.colors(secondary=secondary)
            ui.colors(accent=accent)
            ui.colors(info=info)
            ui.colors(negative=negative)
            ui.colors(positive=positive)
            ui.colors(warning=warning)
            ui.colors(dark=dark)

        apply_theme()

    def revert_theme(self):
        ui.colors(**default_colors)


class Subscriber(Base):
    __tablename__ = 'subscribers'
    id= Column(Integer, primary_key=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    email = Column(String, nullable=False)
    verified = Column(Boolean, nullable=True)
    is_admin = Column(Boolean, nullable=True)
    code = Column(String(255), nullable=True)
    password = Column(String(255), nullable=True)
    hash = Column(String(255), nullable=True)
    created_on = Column(DateTime, nullable=False)
    tier = Column(Integer, nullable=False)

    def set_password(self, password):
        self.hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self._password_hash.encode('utf-8'))

    def create_subscriber(self, email, tier):
        self.email = email
        self.verified = False
        self.is_admin = False
        self.created_on = datetime.datetime.now()
        self.tier = tier
        self.code = random.randint(100000, 999999)
        self.set_password(str(self.code))

    def verify_subscriber(self, password, code):
        self.check_password(code)
        self.set_password(password)
        self.verified = True

    def update_username(self, username):
        self.username = username

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

