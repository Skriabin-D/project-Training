import logging #УДАЛИТЬ ПОТОМ

import asyncio
from aiogram import Bot, Dispatcher
from config import API_TOKEN
from app.handlers import router
from app.database.models import async_main

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)
    await async_main()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')