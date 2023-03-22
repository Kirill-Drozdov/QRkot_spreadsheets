from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    """"Базовый класс для всех моделей приложения."""
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


class DonationProjectBase:
    """"Базовый класс для моделей проекта и пожертвования."""
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    close_date = Column(DateTime,)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.DATABASE_URL)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
