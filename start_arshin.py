import asyncio
from aiogram import Bot, Dispatcher
from app.arshin import router as arshin_router
import config

arshin = Dispatcher()
arshin_bot = Bot(config.TG_API_KEY_1)
arshin.include_router(arshin_router)


async def main():
    await arshin.start_polling(arshin_bot)


asyncio.run(main())
