# app/database.py
from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config import settings

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=True,
    future=True,
)

# Create async session factory
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database sessions"""
    async with async_session() as session:
        yield session


async def create_db_and_tables():
    """Create all tables in the database"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db():
    """Close database connections"""
    await engine.dispose()

