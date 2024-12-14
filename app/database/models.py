'''
Файл, содержащий в себе таблицу в базе данных.
'''
from sqlalchemy import BigInteger, DateTime
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
    '''
    __tablename__ = 'users'
    '''
    Название таблицы
    '''
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    '''
    ID пользователя в таблице
    '''
    tg_id = mapped_column(BigInteger)
    '''
    Телеграмм id пользователя
    '''
    time = mapped_column(DateTime)
    '''
    Время, в течение которого будет действителен абонемент
    '''
async def async_main():
    '''
    Асинхронная функция для создания всех таблиц в базе данных, используя SQLAlchemy.

    Возвращает:
        None
    '''
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)