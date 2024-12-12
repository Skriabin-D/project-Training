from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    '''
        Базовый класс для всех моделей в базе данных.
    '''
    pass

class User(Base):
    '''
        Модель - таблица users в базе данных. Наследуется от базового класса

        Атрибуты:
            id (int): Уникальный идентификатор пользователя в базе данных. Является первичным ключом.
            tg_id (int): Идентификатор пользователя в Telegram. Используется для поиска и идентификации пользователя.
            time (datetime): Время, указывающее срок действия абонемента пользователя.
    '''
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger)
    time = mapped_column(DateTime)

async def async_main():
    '''
    Асинхронная функция для создания всех таблиц в базе данных, используя SQLAlchemy.

    Возвращает:
        None
    '''
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)