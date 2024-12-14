'''
Файл для запуска бота.
'''
import logging

import asyncio
from aiogram import Bot, Dispatcher
from config import API_TOKEN
from app.handlers import router
from app.database.models import async_main

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def main():
    '''
    Основная асинхронная функция для запуска бота.

    Действия:
        - Вызывает асинхронную функцию async_main, которая выполняет начальную настройку.
        - Включает router для обработки сообщений.
        - Запускает процесс опроса (polling) с использованием диспетчера dp.

    Возвращает:
        None
    '''
    await async_main()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')