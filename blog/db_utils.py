from models import User, Base
from models import Post
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import relationship

DATABASE_URL = 'sqlite+aiosqlite:///blog.db'  # Update with your DB URL
async_engine = create_async_engine(DATABASE_URL, echo=True)
# Asynchronous session maker
async_session = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
User.posts = relationship("Post", order_by=Post.id, back_populates="user")
Post.user = relationship("User", back_populates="posts")


async def init_db() -> None:
    # Create the database tables
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    await async_engine.dispose()
