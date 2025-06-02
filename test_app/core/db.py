"""db connection settings"""

from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from test_app.core.config import Settings

settings = Settings()


class PreBase:
    """_summary_

    Returns:
        _type_: _description_
    """

    @declared_attr
    def __tablename__(cls):  # pylint: disable=E0213
        # Именем таблицы будет название модели в нижнем регистре.
        return cls.__name__.lower()  # pylint: disable=E1101

    # Во все таблицы будет добавлено поле ID.
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)
engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
