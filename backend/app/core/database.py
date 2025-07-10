from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

from app.core.config import settings


class Base(DeclarativeBase, MappedAsDataclass):
    pass


DATABASE_URL = f"{settings.POSTGRES_ASYNC_PREFIX}{settings.POSTGRES_URI}"

async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)

local_session = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


async def async_get_db():
    async with local_session() as db:
        yield db
