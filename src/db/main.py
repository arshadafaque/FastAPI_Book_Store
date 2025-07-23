from sqlmodel import text,SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine,create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import config

engine: AsyncEngine = create_async_engine(
    url=config.DATABASE_URL,
    echo=True,
    future=True
)

async def get_db():
    async with engine.begin() as conn:
        from src.books.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,  
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session

