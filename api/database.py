# api/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import AsyncAdaptedQueuePool

from config import DataBase

engine = create_async_engine(
    DataBase.DATABASE_URL,
    echo=False,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=20,
    max_overflow=30
)

AsyncSessionLocal = AsyncSession(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()


async def get_db():
    """Асинхронная зависимость для получения сессии."""
    async with AsyncSessionLocal as session:
        yield session
