'''
Файл, содержащий в себе запросы в базу данных: добавление, удаление пользователя и получение информации о нем.
'''
from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select
from datetime import datetime, timedelta

async def set_user(tg_id, time):
    '''
        Асинхронная функция для добавления пользователя в базу данных

        Аргументы:
            tg_id (int): Идентификатор пользователя в Telegram.
            time (int): Количество дней, через которое истечет действие абонемента пользователя

        Действия:
            - Проверяет на наличие пользователя в базе данных
            - Если пользователя нет, создает его

        Возвращаемое значение:
            None
    '''
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, time = datetime.utcnow() + timedelta(30*int(time))))
            await session.commit()

async def get_info(tg_id):
    '''
        Асинхронная функция для получения оставшегося времени действия абонемента пользователя.

        Аргументы:
            tg_id (int): Идентификатор пользователя в Telegram.

        Действия:
            - Делает запрос в базу данных
            - Если находит пользователя по tg_id, выводит оставшееся время абонемента

        Возвращает:
            Оставшееся время абонемента
    '''
    async with async_session() as session:
        data = await session.scalar(select(User).where(User.tg_id == tg_id))
        if data:
            remaining_time = (data.time - datetime.utcnow()).days
            return remaining_time

async def del_user(tg_id):
    '''
    Асинхронная функция для удаления пользователя из базы данных по его tg_id.

    Аргументы:
        tg_id (int): Идентификатор пользователя в Telegram.

    Действия:
         Делает запрос в базу данных и удаляет пользователя по его tg_id
    '''
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        await session.delete(user)
        await session.commit()